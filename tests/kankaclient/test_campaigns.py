from src.kankamanager.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest

class TestCampaigns(TestCase):
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)

    def test_get_members(self):
        self.assertIsNotNone(self.client.campaigns.get_members())
