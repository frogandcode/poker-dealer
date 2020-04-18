import os
from slack import WebClient

from poker import *

class PokerDealer:
    def __init__(self, players):
        self.players = players
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

class SlackDealer(PokerDealer):
    SLACK_SUITS = {
        '♣': ':clubs:',
        '♦': ':diamonds:',
        '♥': ':hearts:',
        '♠': ':spades:'
    }

    def __init__(self, players):
        super().__init__(players)

        token = os.environ.get('SLACK_API_TOKEN')
        if not token:
            print('Please set the environment variable: SLACK_API_TOKEN')

        self.client = WebClient(token)

    def display_card(self, card):
        return f'{card.rank} {self.SLACK_SUITS[card.suit]}'

    def display_cards(self, cards):
        return '    '.join(list(map(lambda card: self.display_card(card), cards)))

    def post(self, message):
        self.client.chat_postMessage(channel='house', text=message)

    def display_hands(self):
        self.post('*NEW GAME*')
        self.post('---------- Player hands ----------')
        for player in self.game.players:
            self.post(f'{player.name}\n{self.display_cards(self.game.hands[player])}')

    def display_the_flop(self):
        self.post('---------- The Flop ----------')
        self.post(self.display_cards(self.game.community_cards))

    def display_the_turn(self):
        self.post('---------- The Turn ----------')
        self.post(self.display_cards(self.game.community_cards))

    def display_the_river(self):
        self.post('---------- The River ----------')
        self.post(self.display_cards(self.game.community_cards))

    def simulate(self):
        # Play all 4 stages of a game
        for i in range(4):
            self.deal()
