from src.kankamanager.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest

class TestTags(TestCase):
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)

    def test_get_race(self):
        self.assertEqual(self.client.get('races', 'test_parent_race').name, 'test_parent_race')