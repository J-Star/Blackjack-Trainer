import random

DEFAULT_BALANCE = 100

class Card():
    
    SUITS = ["Klaveren", "Ruiten", "Harten", "Schoppen"]
    RANKS = [None, "Aas", "2", "3", "4", "5", "6", "7", \
             "8", "9", "10", "Boer", "Vrouw", "Koning"]
    VALUES = {"Aas": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, \
              "8": 8, "9": 9, "10": 10, "Boer": 10, "Vrouw": 10, "Koning": 10}
    SHORT_NAMES = {"Aas": "A", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", \
              "8": "8", "9": "9", "10": "10", "Boer": "J", "Vrouw": "Q", "Koning": "K"}

    def __init__(self, suit=0, rank=1):
        #integers suit and rank
        #suits: 0=Klaveren, 1=Ruiten, 2=Harten, 3=Schoppen
        #ranks: 1=Aas, 2=2, 3=3,..., 10=10, 11=Boer, 12=Vrouw, 13=Koning
        self.suit = suit
        self.rank = rank
        self.name = Card.RANKS[self.rank]
        self.value = Card.VALUES[Card.RANKS[self.rank]]
        self.short_name = Card.SHORT_NAMES[Card.RANKS[self.rank]]

    def __str__(self):
        return "%s %s" % (Card.SUITS[self.suit], \
                          Card.RANKS[self.rank])


class Deck():

    def __init__(self, num_decks=6):
        self.cards = []
        for deck in range(num_decks):
            for suit in range(4):
                for rank in range(1, 14):
                    card = Card(suit, rank)
                    self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res) + "\n"

    def pop_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):

    def __init__(self):
        self.cards = []

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card.short_name))
        return ', '.join(res)

    def get_score(self):
        num_aces = sum(card.name == "Aas" for card in self.cards)
        score = sum(card.value for card in self.cards)
        if score <= 10 and num_aces >= 1:
            score += 10
        return score
    
    def get_size(self):
        return len(self.cards)
        

class Player():

    def __init__(self, name, balance=DEFAULT_BALANCE):
        self.hand = Hand()
        self.name = name
        self.balance = balance
        self.current_bet = 0
        self.valid_moves = []
        self.best_move = None

    def __str__(self):
        return "%s: %i\n%s" % (self.name, self.hand.get_score(), str(self.hand))

    def hit(self, card):
        self.hand.add_card(card)

    def is_busted(self):
        return self.hand.get_score() > 21

    def update_valid_moves(self):
        value = self.hand.get_score()

        if value == 21 and self.hand.get_size() == 2:
            self.valid_moves = ["Blackjack"]
        elif value == 21 and self.hand.get_size() > 2:
            self.valid_moves = ["21"]
        elif self.is_busted():
            self.valid_moves = []
        

    def update_best_move(self):


class Dealer(Player):

    def __init__(self):
        self.hand = Hand()

    def __str__(self):
        return "Dealer: %i\n%s" % (self.hand.get_score(), str(self.hand))

    def hit(self, card):
        self.hand.add_card(card)

    def is_busted(self):
        return self.hand.get_score() > 21


class Game():

    def __init__(self, num_decks=6, num_players=1):
        self.num_decks = num_decks
        self.num_players = num_players
        #Keep track of where each player sits
        self.positions = []
        for i in range(num_players):
            self.positions.append(Player())
        self.deck = Deck(num_decks)
        self.dealer = Dealer

    def play(self):
        while True:
            #Nieuwe deck als de helft gebruikt is.
            if len(self.deck)< int(52*self.num_decks*0.5):
                self.deck = Deck(self.num_decks)
                
            ## hit
            Player().hit(self.deck.pop_card())

            
        
blackjack = Game()
blackjack.play()
