import unittest
from unittest import mock
from io import StringIO
from src import game_logic
from src import card_info


class TestGameLogic(unittest.TestCase):
    @mock.patch('builtins.input', side_effect=['3', 'human', 'human', 'human'])
    def test_game_setup_valid_input(self, mocked_input):
        with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            unshuffled_deck = card_info.card_list
            players, deck, discard_deck = game_logic.game_setup(test_deck=unshuffled_deck)
            player1_private_hand_5 = {'active_color': 'None',
                                      'card_type': 'House',
                                      'colors_available': ['None'],
                                      'name': 'House',
                                      'value': 3}
            player3_private_hand_5 = {'active_color': 'None',
                                      'card_type': 'Money',
                                      'colors_available': ['None'],
                                      'name': '$2',
                                      'value': 2}
            output = mock_stdout.getvalue().strip()
            self.assertEqual(len(players), 3)
            self.assertEqual(len(deck), 91)
            self.assertEqual(len(discard_deck), 0)
            self.assertEqual(players[0]['public_hand'], [])
            self.assertEqual(players[0]['private_hand'][4], player1_private_hand_5)
            self.assertEqual(players[2]['private_hand'][4], player3_private_hand_5)
            self.assertEqual(players[0]['move_count'], 0)

    @mock.patch('builtins.input', side_effect=['invalid', '4', 'human', 'human', 'human', 'human'])
    def test_game_setup_invalid_non_integer_input(self, mocked_input):
        with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            players, deck, discard_deck = game_logic.game_setup()
            output = mock_stdout.getvalue().strip()
            self.assertIn("Please enter a valid integer.", output)
            self.assertEqual(len(players), 4)
            self.assertEqual(len(deck), 86)
            self.assertEqual(len(discard_deck), 0)

    @mock.patch('builtins.input', side_effect=['7', '0', '1', '6', '5', 'bot', 'bot', 'bot', 'bot', 'bot'])
    def test_game_setup_invalid_input_out_of_range(self, mocked_input):
        with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            players, deck, discard_deck = game_logic.game_setup()
            output = mock_stdout.getvalue().strip()
            self.assertIn("Please enter a number between 2 and 5.", output)
            self.assertEqual(len(players), 5)
            self.assertEqual(len(deck), 81)



if __name__ == '__main__':
    unittest.main()
