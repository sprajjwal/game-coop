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
        self.is_alive = True

    @staticmethod
    def print_cards(cards):
        """ Print all the cards being passed """
        print("Your cards are: ")
        ctr = 1
        for card in cards:
            print(f"{ctr}. {card.name}")
            ctr += 1

    def take_income(self):
        """ Take one gold, can't be blocked """
        self.money += 1
        print(f"{self.name} earned 1 gold as income.")

    def take_foreign_aid(self):
        """ Take 2 gold, can be blocked by Duke """
        self.money += 2
        print(f"{self.name} earned 2 gold as Foreign Aid!")
        
    def use_duke(self):
        """ Uses Duke's ability and collects 3 gold """
        print(f"{self.name} taxed 3 as a Duke!")
        self.money += 3

    def use_captain(self, player):
        ''' Use captain ability on someone, can be blocked  by 
        ambassador or othe captains '''
        self.money += 2
        player.money -= 2
        print(f"{self.name} stole 2 gold from {player.name}.")
        print(f"{player.name} lost 2 gold.")
        return 1

    def use_ambassador(self, two_cards):
        ''' choose 1 or 2 cards from self.cards + two_cards'''
        pool = self.cards + two_cards
        self.cards = []
        for ctr in range(self.life):
            print("Your choices are: ")
            self.print_cards(pool)
            self.cards.append(pool.pop(int(input(f"Choose card number {ctr+1}: "))-1))
        print(f"{self.name} switched their cards")
        return pool

    def use_assassin(self, player):
        """ Use Assassin's ability and kill someone's influence """
        print(f"{self.name} assasinated {player.name}.")
        Player.print_cards(player.cards)
        choice = int(input("Which card do you want to kill?: "))
        print(f"Killing {player.cards[choice-1].name}.")
        del player.cards[choice-1]
        player.life -= 1
        return 1

    def use_contessa(self, player):
        """ Use Contessa's ability and save someone from getting Assasinated """
        print(f"{self.name} saved {player.name}.")

    def contest(self, card_type, deck):
        ''' check if player was bs'ing and didn't have card_type '''
        for card in self.cards:
            if card_type == card.name:
                self.switch_card(card, deck)
                return True
        return False

    def switch_card(self, card, deck):
        """ return card to the deck and get back another random card"""
        assert card in self.cards
        deck.append(card)
        self.cards[self.cards.index(card)] = deck.pop(random.randint(0, len(deck)-1))

    def get_blocks(self):
        """ returns a list of blocks the player has based on their cards """
        return [block for card in self.cards for block in card.blocks]

    def kill_card(self, card_name):
        """ Kills a card that player has """
        for card in self.cards:
            if card.name == card_name:
                del card
                player.life -= 1
                return 1
        self.check_hp()
        return 0

    def loose_life(self):
        """Processes the i/o for a player to choose which card to kill"""
        if self.life == 1:
            print(f"You only had {self.cards[0].name}.")
            print(f"Killing {self.cards[0].name}.")
            self.cards = []
            self.life = 0
            self.isalive = False
        else:
            self.print_cards(self.cards)
            ind = int(input(f"Enter the card number to kill {self.name}: ")) - 1
            print(f"Killing {self.cards[ind].name}.")
            del self.cards[ind]
            self.life -= 1
        self.check_hp()
        return 1

    def check_hp(self):
        """Sets is_alive to false if life == 0"""
        if self.life == 0:
            self.is_alive = False
# Card classes

class Influence:
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
    game_classes = { # holds class name based on action
        3: 'Duke',
        4: 'Captain',
        5: 'Assassin',
        6: 'Ambassador',
    }
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
        self.card_repeat = round((num_players*2 +7)/5)
        self.deck = []
        self.players = [] 
        self.alive_players = num_players

    def fill_deck(self):
        """ Fills the deck with cards of each class and then shuffles it. """
        for Influence in [Ambassador, Assassin, Contessa, Captain, Duke]:
            self.deck += [Influence()  for i in range(self.card_repeat)]
        random.shuffle(self.deck)

    def create_players(self):
        """ Creates players who want to play the game """
        for num in range(self.alive_players):
            self.players.append(Player(input(f"Enter your name player {num+1}: ").capitalize()))

    def draw_card(self):
        """Gets a card from the deck. """
        return self.deck.pop(random.randrange(len(self.deck)))

    def deal_cards(self):
        """ Gives cards to each player """
        for player in self.players:
            player.cards.extend([self.draw_card(), self.draw_card()])
    
    def is_playing(self):
        """Returns false if only one player is left with cards, if more, returns true"""
        ct = 0
        for player in self.players:
            if player.is_alive:
                ct += 1
        return ct > 1

    def show_players_get_input(self, task, not_show = None):
        """ shows all the player other than not_show and asks which player wants to do the task.
        returns index of the player in self.players"""
        print("- - - " * 7)
        ctr = 1
        players=[]
        while True:
            for player in self.players:
                if  player.name != not_show and player.is_alive:
                    print(f"{ctr}. {player.name}")
                    players.append(player)
                    ctr += 1
            against = input(f"Enter user number {task}: ")
            if against.isdigit():
                against = int(against) - 1
                break
        return self.players.index(players[against])

    @staticmethod
    def show_turn_options(player):
        """Shows player's name, gold and all the options available to them from turn_options."""
        print(f"Your turn {player.name}! You have {player.money} gold. Your options are:")
        for num, action in Game.turn_options.items():
            print(f"{num}. {action}")

    def choose_action(self, player): 
        """ Input validation on action a player can make """
        while True:
            turn_option = input("Which action do you want to make?: ")
            if turn_option.isdigit():
                turn_option = int(turn_option)
                if turn_option > 0 and turn_option <= 7 :
                    return int(turn_option)

    def stop_assassination(self, assassin, victim):
        """Prompts players to use contessa, if someone uses contessa, return True
        else, returns false """
        block = input("Does anyone want to use contessa?(Y/N) ")
        if block in "Yy":
            contessa_index = self.show_players_get_input("who wants to use contessa",assassin, victim)
            is_contest = self.contest_action(self.players[contessa_index], "Contessa")
            if is_contest == -1 or not is_contest:
                self.players[contessa_index].use_contessa(victim)
                return True
            else:
                return False
        else:
            return False

    def take_turn(self, player):
        """ has the logic for all the actions, contest during a players turn"""
        os.system('clear')
        Game.show_turn_options(player)
        while True:
            print("- - - " * 7)
            turn_option = self.choose_action(player)
            if turn_option in range(1, 4):
                turn_function = getattr(player, Player.turn_function_names[turn_option])
                if turn_option == 3:
                    contest_val = self.contest_action(player, Game.game_classes[turn_option])
                    if contest_val == False:
                        print(f"Executing Duke's ability.")
                        turn_function()
                    break
                else:
                    print(f"Executing {Game.turn_options[turn_option]}.")
                    turn_function()
                    break
            elif turn_option in range(4, 8): # functions that need arguments
                if turn_option == 4: # Steal
                        index = self.show_players_get_input("to steal from", player.name)
                        contest_val = self.contest_action(player, Game.game_classes[turn_option])
                        if self.players[index].money < 2:
                            print(f"{self.players[index].name} doesn't have enough money. Try again!")
                        elif contest_val == False:
                            turn_function = getattr(player, Player.turn_function_names[turn_option])
                            print(f"Executing steal on {self.players[index].name}.")
                            turn_function(self.players[index])
                            break
                        else: # contest successful
                            break
                elif turn_option == 5: # assassinate, requires atleast 3 gold
                    if player.money < 3:
                        print("Not enough gold, use a different ability.")
                    else:
                        turn_function = getattr(player, Player.turn_function_names[turn_option])
                        index = self.show_players_get_input("to assassinate", player.name)
                        contest_val = self.contest_action(player, Game.game_classes[turn_option])
                        if contest_val == False:
                            print(f"{player.name} did have {Game.game_classes[turn_option]}.")
                            if not self.stop_assassination(player, self.players[index]):
                                print(f"Executing assassination on {self.players[index].name}.")
                                turn_function(self.players[index])
                        break
                elif turn_option == 6: # switching cards
                    contest_val = self.contest_action(player, Game.game_classes[turn_option])
                    if contest_val == False:
                        print(f"Executing ambassador's ability.")
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
        """ Gets the player who has atleast 1 card alive """
        for player in self.players:
            if player.is_alive:
                return player

    def contest_action(self, player, card_name):
        """ processes logic for player having card_name
        asks, who wants to contest, if no one contests, returns false
        if player has card, returns false
        if player doesn't have card, returns True """
        while True:
            is_contest = input("Does anyone want to contest?(Y/N): ")
            if is_contest in "YyNn":
                break
        if is_contest in "Nn":
            return False
        else: # in "Yy
            contester_index = self.show_players_get_input("who wants to contest", player.name)
            contester = self.players[contester_index]
            has_card = player.contest(card_name, self.deck)
            print("- - - " * 7)
            if has_card:
                print(f"You failed the contest {contester.name}. {player.name} has {card_name}.")
                contester.loose_life()
                return False
            else:
                print(f"You failed the contest {player.name}.You didn't have {card_name}.")
                player.loose_life()
                return True