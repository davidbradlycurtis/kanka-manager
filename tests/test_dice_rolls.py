from src.kankaclient.client import KankaClient
from unittest import mock, TestCase
import os, pytest, uuid, time

class TestDiceRolls(TestCase):
    character = None
    def setUp(self):
        config = {
            'campaign': os.getenv('CAMPAIGN'),
            'campaign_dir': os.getenv('CAMPAIGN_DIR'),
            'token': os.getenv('TOKEN'),
            'throttle': os.getenv('TOKEN')
        }
        self.client = KankaClient(config)
        self.dice_name = f'test_dice_roll_{uuid.uuid1()}'


    def test_get_dice_roll(self):
        self.assertEqual(self.client.get('dice', 'test_dice_roll').name, 'test_dice_roll')

    def test_create_and_delete_dice_roll(self):
        dice_roll = self.client.create('dice', {'name': self.dice_name, 'parameters': '3d6'})
        self.assertIsNotNone(dice_roll)
        self.assertTrue(self.client.delete('dice', dice_roll.id))
