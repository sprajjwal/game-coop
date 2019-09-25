class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.money = 2
        self.life = 2

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

    def switch_card():
        pass
    

# tester class
class Cards:
    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    card1 = Cards('ambassador')
    card2 = Cards('Duke')
    card3 = Cards('Assasin')
    card4 = Cards('contessa')
    player1 = Player("shaash")
    player2 = Player("shashwat")
    player1.cards.append(card1)
    player1.cards.append(card2)
    player1.print_cards(player1.cards)
    print(player2.contest('ambassador', player1))


