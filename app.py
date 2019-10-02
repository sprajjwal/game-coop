from game_class import *

if __name__ == '__main__':
    player1 = Player("Alan")
    player2 = Player("Shashwat")
    game = Game(2)
    game.fill_deck()
    game.add_player(player1)
    game.add_player(player2)
    game.deal_cards()
    # print(player1.cards)
    # Player.print_cards(player1.cards)
    # print(player2.cards)
    # Player.print_cards(player2.cards)
    game.show_players()
    game.show_turn_options(game.players[0])
    print(game.players[0].money)

    while game.is_playing():
        for player in game.players:
            game.take_turn(player)

            

