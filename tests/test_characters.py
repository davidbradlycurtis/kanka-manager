from src.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest

class TestCharacters(TestCase):
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)

    def test_get_character(self):
        self.assertEqual(self.client.get('characters', 'test_character').name, 'test_character')
