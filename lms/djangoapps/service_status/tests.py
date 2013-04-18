"""Test for async task service status"""

from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
import json
import celery.exceptions

class CeleryConfigTest(unittest.TestCase):
    """Test that we can get celery running locally"""

    def setUp(self):
        """Create a django test client"""
        self.client = Client()
        self.ping_url = reverse('status.service.celery')

    def test_ping(self):
        """Try pinging celery.
        
        By default, the test settings use CELERY_ALWAYS_EAGER=True,
        which causes celery to run tasks and return the results
        immediately."""

        # Access the service status page, whcih starts a delayed
        # asynchronous task
        response = self.client.get(self.ping_url)

        # HTTP response should be successful
        self.assertEqual(response.status_code, 200)

        # Expect to get a JSON-serialized dict with
        # task and time information 
        result_dict = json.loads(response.content)

        # We should get a "pong" message back
        self.assertEqual(result_dict['value'], "pong")

        # We don't know the other dict values exactly,
        # but we can assert that they take the right form
        self.assertTrue(isinstance(result_dict['task_id'], unicode))
        self.assertTrue(isinstance(result_dict['time'], float))
        self.assertTrue(result_dict['time'] > 0.0)
