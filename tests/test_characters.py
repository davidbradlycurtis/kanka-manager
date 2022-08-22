from src.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestCharacters(TestCase):
    character = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.character_name = f'test_character_{uuid.uuid1()}'


    def test_get_character(self):
        self.assertEqual(self.client.get('characters', 'test_character').name, 'test_character')

    def test_create_and_delete_character(self):
        character = self.client.create('characters', {'name': self.character_name})
        self.assertIsNotNone(character)
        self.assertTrue(self.client.delete('characters', character.id))
