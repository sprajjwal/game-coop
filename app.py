from game_class import *
import time

if __name__ == '__main__':
    while True:
        num_players = input("How many people are playing? ")
        if num_players.isdigit():
            num_players = int(num_players)
            break
    game = Game(num_players)
    game.create_players()
    game.fill_deck()
    game.deal_cards()

    while True:
        for player in game.players:
            if len(player.cards) > 0:
                game.take_turn(player)
                time.sleep(1)
                if not game.is_playing():
                    print("Game over")
                    print(f"{self.get_winner().name}won!")
                    exit()


