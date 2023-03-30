from src.kankamanager.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestConversations(TestCase):
    conversation = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.conversation_name = f'test_conversation_{uuid.uuid1()}'


    def test_get_conversation(self):
        self.assertEqual(self.client.get('conversations', 'test_conversation').name, 'test_conversation')

    def test_create_and_delete_conversation(self):
        conversation = self.client.create('conversations', {'name': self.conversation_name, 'target_id': 1})
        self.assertIsNotNone(conversation)
        self.assertTrue(self.client.delete('conversations', conversation.id))
