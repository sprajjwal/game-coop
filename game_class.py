import random
import os
class Player:
    turn_function_names = {
        1: 'take_income',
        2: 'take_foreign_aid',
        3: 'use_duke',
        4: 'use_captain',
        5: 'use_assassin',
        6: 'use_ambassador',
        7: 'print_cards'
    }

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.money = 2
        self.life = 2
        self.isalive = True

    def use_captain(self, player):
        ''' Use captain ability on someone, can be blocked  by 
        ambassador or othe captains '''
        self.money += 2
        player.money -= 2
        print(f"{self.name} stole 2 gold from {player.name}")
        print(f"{player.name} lost 2 gold")
        return 1

    @staticmethod
    def print_cards(cards):
        """ Print all the cards being passed """
        ctr = 1
        for card in cards:
            print(f"{ctr}. {card.name}")
            ctr += 1

    def use_ambassador(self, two_cards):
        ''' choose 1 or 2 cards from self.cards + two_cards'''
        pool = self.cards + two_cards
        self.cards = []
        for ctr in range(self.life):
            print("Yourch choices are: ")
            self.print_cards(pool)
            self.cards.append(pool.pop(int(input(f"Choose card number {ctr+1}: "))-1))
        print(f"{self.name} switched their cards")
        return pool
        
    def use_duke(self):
        """ Uses Duke's ability and collects 3 gold """
        print(f"{self.name} taxed 3 as a Duke!")
        self.money += 3

    def use_contessa(self, player):
        """ Use Contessa's ability and save someone from getting Assasinated """
        print(f"{self.name} saved {player.name}")

    def use_assassin(self, player):
        """ Use Assassin's ability and kill someone's influence """
        print(f"{self.name} assasinated {player.name}")
        Player.print_cards(player.cards)
        choice = int(input("Which card do you want to kill?: "))
        print(f"Killing {player.cards[choice-1].name}")
        del player.cards[choice-1]
        print(len(player.cards))
        return 1

    def take_income(self):
        """ Take one gold, can't be blocked """
        self.money += 1
        print(f"{self.name} earned 1 gold as income")

    def take_foreign_aid(self):
        """ Take 2 gold, can be blocked by Duke """
        self.money += 2
        print(f"{self.name} earned 2 gold as Foreign Aid!")

    def contest(self, card_type, player):
        if self.name == player.name:
            return -1
        ''' check if player was bs'ing and didn't have card_type '''
        for card in player.cards:
            if card_type == card:
                return False
        return True

    def switch_card(self, card, deck):
        """ return card to the deck and get back another random card"""
        assert card in self.cards
        deck.append(card)
        self.cards[self.cards.index(card)] = deck.pop(random.randint(0, len(deck)-1))

    def get_blocks(self):
        """ returns a list of blocks the player has based on their cards """
        return [block for card in self.cards for block in card.blocks]



# Card classes

class Influence:
    """ Main game class class that is inherited by all influence types """
    def __init__(self, name, blocks=None):
        self.name = name
        self.is_owned = False
        if blocks == None:
            self.blocks = []
        else:
            self.blocks = blocks

    def __repr__(self):
        return f"{self.name}(blocks={self.blocks})"

class Ambassador(Influence):
    def __init__(self):
        super().__init__('Ambassador', ['Steal'])

class Assassin(Influence):
    def __init__(self):
        super().__init__('Assassin')

class Contessa(Influence):
    def __init__(self):
        super().__init__('Contessa', ['Assasin'])

class Duke(Influence):
    def __init__(self):
        super().__init__('Duke', ['Foreign Aid'])
class Captain(Influence):
    def __init__(self):
        super().__init__('Captain', ['Steal'])

class Game:
    turn_options = { # shows all posible actions a person can take
        1: "Take Income",
        2: "Take Foreign Aid",
        3: "Use Duke's ability", 
        4: "Use steal as Captain",
        5: "Assassinate someone as assassin",
        6: "Switch cards as Ambassador",
        7: "Show my cards"
    }
    def __init__(self, num_players):
        self.card_repeat = 3
        self.deck = []
        self.players = [] 
        self.alive_players = num_players

    def fill_deck(self):
        """ Fills the deck with cards of each class """
        for Influence in [Ambassador, Assassin, Contessa, Captain, Duke]:
            self.deck += [Influence()  for i in range(self.card_repeat)]
        random.shuffle(self.deck)

    def create_players(self):
        """ Creates players who want to play the game """
        for num in range(self.alive_players):
            self.players.append(Player(input(f"Enter your name player {num+1}: ")))

    def draw_card(self):
        return self.deck.pop(random.randrange(len(self.deck)))

    def deal_cards(self):
        for player in self.players:
            player.cards.extend([self.draw_card(), self.draw_card()])

    def add_player(self, player):
        self.players.append(player)
    
    def is_playing(self):
        ct = 0
        for player in self.players:
            if len(player.cards) > 0:
                ct += 1
        return ct > 1

    def show_players_get_input(self, not_show = None):
        print("- - - " * 7)
        ctr = 1
        players=[]
        for player in self.players:
            if  player.name != not_show:
                print(f"{ctr}. {player.name}")
                players.append(player)
                ctr += 1
        against = int(input("Enter user number to use ability on: ")) -1
        return self.players.index(players[against])

    @staticmethod
    def show_turn_options(player):
        print(f"Your turn {player.name}! You have {player.money} gold. Your options are:")
        for num, action in Game.turn_options.items():
            print(f"{num}. {action}")

    def choose_action(self, player):
        # 
        turn_option = int(input("Which action do you want to make?: "))
        return turn_option

    def stop_assassination(self, assassin, victim):
        block = input("Does anyone want to use contessa?(Y/N) ")
        if block in "Yy":
            self.players[contessa_index].use_contessa(victim)
            return True
        else:
            return False

        

    def take_turn(self, player):
        os.system('clear')
        Game.show_turn_options(player)
        while True:
            print("- - - " * 7)
            turn_option = self.choose_action(player)
            if turn_option in range(1, 4):
                turn_function = getattr(player, Player.turn_function_names[turn_option])
                turn_function()
                break
            elif turn_option in range(4, 8): # functions that need arguments
                if turn_option == 4: # Steal
                        index = self.show_players_get_input(player.name)
                        if self.players[index].money < 2:
                            print(f"{self.players[index].name} doesn't have enough money. Try again!")
                        else:
                            turn_function = getattr(player, Player.turn_function_names[turn_option])
                            turn_function(self.players[index])
                            break
                elif turn_option == 5: # assassinate, requires atleast 3 gold
                    if player.money < 3:
                        print("Not enough gold, use a different ability")
                    else:
                        turn_function = getattr(player, Player.turn_function_names[turn_option])
                        index = self.show_players_get_input(player.name)
                        if not self.stop_assassination(player, self.players[index]):
                            turn_function(self.players[index])
                        break
                elif turn_option == 6: # switching cards
                    two_cards = []
                    two_cards.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
                    two_cards.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
                    turn_function = getattr(player, Player.turn_function_names[turn_option])
                    self.deck += turn_function(two_cards)
                    random.shuffle(self.deck)
                    break
                elif turn_option == 7: # showing cards
                    Player.print_cards(player.cards)
            else:
                print("Incorrect input!")

    def get_winner(self):
        for player in self.players:
            if player.cards:
                return player

