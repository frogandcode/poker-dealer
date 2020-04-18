import random

class Player:
    def __init__(self, name):
        self.name = name

class Card:
    SUITS = ['♣', '♦', '♥', '♠']
    RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self, rank, suit):
        # TODO: Validate rank and suit
        self.rank = rank
        self.suit = suit

    @staticmethod
    def join(cards):
        return ' '.join(map(lambda card: str(card), cards))

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return f'{type(self)}: {self.__str__()}'

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str(list(map(lambda card: str(card), self.cards)))

    def __repr__(self):
        return f'{type(self)}: {self.__str__()}'

class Game:
    def __init__(self, players):
        # TODO: Validate players list
        self.players = players
        self.hands = {}
        self.community_cards = []
        self.deck = Deck()
        self.deck.shuffle()

    @property
    def stage(self):
        if not self.hands:
            return 'start'
        elif not self.community_cards:
            return 'hands'
        elif len(self.community_cards) == 3:
            return 'flop'
        elif len(self.community_cards) == 4:
            return 'turn'
        else:
            return 'river'

    def deal(self):
        stage = self.stage

        if stage == 'start':
            self.deal_hands()
        elif stage == 'hands':
            self.deal_flop()
        elif stage in ['flop', 'turn']:
            self.deal_community()
        else:
            raise Exception("Game over, all cards have been dealt. Start a new game.")

        return self.stage

    def deal_hands(self):
        for player in self.players:
            self.hands[player] = []
            # Deal two "hole" cards
            for i in range(2):
                self.hands[player].append(self.deck.deal())

    def deal_flop(self):
        for i in range(3):
            self.deal_community()

    def deal_community(self):
        self.community_cards.append(self.deck.deal())

class Dealer:
    def __init__(self, players):
        # TODO: Validate players list
        self.players = []
        for player in players:
            self.players.append(Player(name=player))
        self.game = Game(self.players)

    def deal(self):
        # Dealing is over if we’ve reached the river
        if self.game.stage == 'river':
            self.game = Game(self.players)

        stage = self.game.deal()

        if stage == 'flop':
            self.display_the_flop()
        elif stage == 'turn':
            self.display_the_turn()
        elif stage == 'river':
            self.display_the_river()
        else:
            self.display_hands()

    def display_hands(self):
        print('NEW GAME')
        print()
        print('Player Hands')
        for player in self.game.players:
            print()
            print(player.name)
            print(Card.join(self.game.hands[player]))

    def display_the_flop(self):
        print()
        print('The Flop')
        print(Card.join(self.game.community_cards))

    def display_the_turn(self):
        print()
        print('The Turn')
        print(Card.join(self.game.community_cards))

    def display_the_river(self):
        print()
        print('The River')
        print(Card.join(self.game.community_cards))

    def simulate(self):
        # Play all 4 stages of a game
        for i in range(4):
            self.deal()
