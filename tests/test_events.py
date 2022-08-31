from src.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestEvents(TestCase):
    event = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.event_name = f'test_event_{uuid.uuid1()}'


    def test_get_event(self):
        self.assertEqual(self.client.get('events', 'test_event').name, 'test_event')

    def test_create_and_delete_event(self):
        event = self.client.create('events', {'name': self.event_name})
        self.assertIsNotNone(event)
        self.assertTrue(self.client.delete('events', event.id))
