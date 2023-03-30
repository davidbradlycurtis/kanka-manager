from src.kankamanager.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestItems(TestCase):
    item = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.item_name = f'test_item_{uuid.uuid1()}'


    def test_get_item(self):
        self.assertEqual(self.client.get('items', 'test_item').name, 'test_item')

    def test_create_and_delete_item(self):
        item = self.client.create('items', {'name': self.item_name})
        self.assertIsNotNone(item)
        self.assertTrue(self.client.delete('items', item.id))
