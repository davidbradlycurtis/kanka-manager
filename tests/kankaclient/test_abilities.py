from src.kankamanager.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestAbilities(TestCase):
    ability = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.ability_name = f'test_ability_{uuid.uuid1()}'


    def test_get_ability(self):
        self.assertEqual(self.client.get('abilities', 'test_ability').name, 'test_ability')

    def test_create_and_delete_ability(self):
        ability = self.client.create('abilities', {'name': self.ability_name})
        self.assertIsNotNone(ability)
        self.assertTrue(self.client.delete('abilities', ability.id))
