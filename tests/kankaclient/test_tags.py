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

    def test_get_tag(self):
        self.assertEqual(self.client.get('tags', 'test_parent_tag').name, 'test_parent_tag')
