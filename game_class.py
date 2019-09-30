import random
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.money = 2
        self.life = 2
        self.isalive = True

    def use_steal(self, player):
        ''' Use captain ability on someone'''
        self.money += 2
        player.money -= 2
        print(f"{self.name} stole 2 gold from {player.name}")
        print(f"{player.name} lost 2 gold")

    @staticmethod
    def print_cards(cards):
        ctr = 1
        for card in cards:
            print(f"{ctr}. {card.name}")
            ctr += 1

    def use_ambassador(self, two_cards):
        ''' choose 1 or 2 cards from self.cards + two_cards'''
        pool = self.cards + two_cards
        self.print_cards(pool)
        self.cards = []
        for ctr in range(self.life):
            self.cards.append(pool[int(input(f"Choose card number {ctr+1}: "))-1])
        print(f"{self.name} switched their cards")
        
    def use_duke(self):
        print(f"{self.name} taxed 3 as a Duke!")
        self.money += 3

    def use_contessa(self, player):
        print(f"{self.name} saved {player.name}")

    def use_assasin(self, player):
        print(f"{self.name} assasinated {player.name}")
        player.kill_card()

    def take_income(self):
        self.money += 1
        print(f"{self.name} earned 1 gold as income")

    def take_foreign_aid(self):
        self.money += 2
        print(f"{self.name} earned 2 gold as Foreign Aid!")

    def contest(self, card_type, player):
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

    def kill_card(self, card):
        """ Kills a card that player has """
        assert card in self.cards
        self.cards.remove(card)

    def get_blocks(self):
        """ returns a list of blocks the player has based on their cards """
        return [block for card in self.cards if card.blocks for block in card.blocks]


# Card classes
class Ambassador:
    def __init__(self):
        self.name = 'Ambassador'
        self.is_owned = False
        self.blocks = ['Steal']

class Assassin:
    def __init__(self):
        self.name = 'Assassin'
        self.is_owned = False
        self.blocks = None

class Contessa:
    def __init__(self):
        self.name = 'Contessa'
        self.is_owned = False
        self.blocks = ['Assassin']

class Duke:
    def __init__(self):
        self.name = 'Duke'
        self.is_owned = False
        self.blocks = ['Foreign Aid']

class Captain:
    def __init__(self):
        self.name = 'Captain'
        self.is_owned = False
        self.blocks = ['Steal']

class Game:
    def __init__(self):
        self.card_repeat = 3
        self.deck = []
        self.players = [] 

    def fill_deck(self):
        """ Fills the deck with cards of each class """
        self.deck += [Ambassador()  for i in range(self.card_repeat)]
        self.deck += [Assassin() for i in range(self.card_repeat)]
        self.deck += [Contessa() for i in range(self.card_repeat)]
        self.deck += [Duke() for i in range(self.card_repeat)]
        self.deck += [Captain() for i in range(self.card_repeat)]
        random.shuffle(self.deck)

    def create_player(self):
        """ Creates players who want to play the game """
        for num in range(int(input("Enter number of players playing: "))):
            self.players.append(Player(input("Enter your name: ")))

    def give_cards(self, player):
        for player in self.players:
            player.cards.append(self.deck.pop(random.randint(0, len(self.deck))))
            player.cards.append(self.deck.pop(random.randint(0, len(self.deck))))