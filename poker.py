import random

class Card:
    SUITS = ['♣', '♦', '♥', '♠']
    RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

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
