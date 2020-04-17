import random

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
    def __init__(self, player_count):
        # TODO: Validate player_count
        self.player_count = player_count
        self.hands = {}
        self.community_cards = []
        self.deck = Deck()
        self.deck.shuffle()

    def deal(self):
        if not self.hands:
            self.deal_hands()
        elif not self.community_cards:
            self.deal_flop()
        elif len(self.community_cards) < 5:
            self.deal_community()
        else:
            raise Exception("Game over, all cards have been dealt.")

    def deal_hands(self):
        for player in range(self.player_count):
            self.hands[player] = []
            # Deal two "hole" cards
            for i in range(2):
                self.hands[player].append(self.deck.deal())

    def deal_flop(self):
        for i in range(3):
            self.deal_community()

    def deal_community(self):
        self.community_cards.append(self.deck.deal())

    @classmethod
    def simulate(cls, player_count):
        game = cls(player_count)

        print('Let’s play poker!')

        # Deal hole cards
        game.deal()
        print()
        print('Dealing player hands ...')
        for player in range(player_count):
            print(f'Player {player + 1}: {Card.join(game.hands[player])}')

        # Deal the flop
        game.deal()
        print()
        print('Dealing the flop ...')
        print(f'Community cards: {Card.join(game.community_cards)}')

        # Deal the turn
        game.deal()
        print()
        print('Dealing the turn ...')
        print(game.community_cards[-1])
        print(f'Community cards: {Card.join(game.community_cards)}')

        # Deal the river
        game.deal()
        print()
        print('Dealing the river ...')
        print(game.community_cards[-1])
        print(f'Community cards: {Card.join(game.community_cards)}')

        print()
        print('Who won?!')
