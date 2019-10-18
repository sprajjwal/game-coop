from unittest import TestCase, main
from unittest.mock import patch
from game_class import *
import sys

class GameTest(TestCase):
    def setUp(self):
        """ setup before testing any method """
        self.game = Game(3)
        self.game.fill_deck()

        # test players
        self.pl1 = Player("Player 1")
        self.pl2 = Player("Player 2")
        self.pl3 = Player("Player 3")
        
        # adding players to game
        self.game.players.append(self.pl1)
        self.game.players.append(self.pl2)
        self.game.players.append(self.pl3)
        
        self.game.deal_cards() # dealing cards to each player

    def test_draw_cards(self):
        """tests if we are drawing cards properly"""
        card = self.game.draw_card()
        assert card.name in "Duke Assassin Contessa Ambassador Captain"

    def test_is_playing(self):
        """Checks if game should still be running"""
        assert self.game.is_playing() == True

        #kills 1 out of 3 player
        self.game.players[0].is_alive = False
        assert self.game.is_playing() == True

        #kills 2 out of 3 players
        self.game.players[1].is_alive = False
        assert self.game.is_playing() == False

    def test_show_players_get_input(self):
        """Checks if this function returns proper values"""

        # when everyone is accessible
        with patch('builtins.input', return_value='1'):
            index = self.game.show_players_get_input("test")
            assert index == 0

        # if the person checking is at index 0
        with patch('builtins.input', return_value='1'):
            index = self.game.show_players_get_input("test", "Player 1")
            assert index == 1

        #killing the first person 
        self.game.players[0].is_alive = False

        # when the first person in game.players is dead
        with patch('builtins.input', return_value='1'):
            index = self.game.show_players_get_input("test")
            assert index == 1

        
        # if the person checking is at index 1
        with patch('builtins.input', return_value='1'):
            index = self.game.show_players_get_input("test", "Player 2")
            assert index == 2

    def test_show_turn_options(self):
        """Checks turn options """

        self.game.show_turn_options(self.pl1)
        output = sys.stdout.getvalue().strip()
        test_output = """Your turn Player 1! You have 2 gold. Your options are:
1. Take Income
2. Take Foreign Aid
3. Use Duke's ability
4. Use steal as Captain
5. Assassinate someone as assassin
6. Switch cards as Ambassador
7. Show my cards"""
        assert output == test_output
        
    
    def test_choose_action(self):
        """ tests input validation on choose action method"""

        with patch('builtins.input', return_value='1'):
            inp = self.game.choose_action(self.pl1)
            assert inp == 1
        with patch('builtins.input', return_value='3'):
            inp = self.game.choose_action(self.pl1)
            assert inp == 3

    def test_stop_assassination(self):
        """tests return on stop assassination method """

        # no one wants to use contessa
        with patch('builtins.input', return_value='n'):
            inp = self.game.stop_assassination(self.pl1, self.pl2)
            assert inp == False

        # someone wants to use contessa
        # with patch('builtins.input', return_value='y'):
        #     inp = self.game.stop_assassination(self.pl1, self.pl2)
        #     assert inp == False or inp == True

    def test_get_winner(self):
        """Tests if the correct person is winning"""
        self.game.players[0].is_alive = False
        self.game.players[2].is_alive = False
        winner = self.game.get_winner()
        assert winner.name == "Player 2"





if __name__ == "__main__":
    main(buffer=True) # runs with buffer on to capture standard output