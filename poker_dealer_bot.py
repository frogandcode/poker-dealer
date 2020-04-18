import os
from slack import WebClient

from poker import *

class SlackDealer:
    SLACK_SUITS = {
        '♣': ':clubs:',
        '♦': ':diamonds:',
        '♥': ':hearts:',
        '♠': ':spades:'
    }

    def __init__(self, player_count):
        self.client = WebClient(os.environ.get('SLACK_API_TOKEN'))
        self.game = Game(player_count)

    def display_card(self, card):
        return f'{card.rank} {self.SLACK_SUITS[card.suit]}'

    def display_cards(self, cards):
        return '    '.join(list(map(lambda card: self.display_card(card), cards)))

    def post(self, message):
        self.client.chat_postMessage(channel='house', text=message)

    def play(self):
        self.post('Let’s play poker!')

        self.post('––––– Player hands –––––')
        self.game.deal()
        for player in range(self.game.player_count):
            self.post(f'Player {player + 1}\n{self.display_cards(self.game.hands[player])}')

        self.post('––––– The Flop –––––')
        self.game.deal()
        self.post(self.display_cards(self.game.community_cards))

        self.post('––––– The Turn –––––')
        self.game.deal()
        self.post(self.display_cards(self.game.community_cards))

        self.post('––––– The River –––––')
        self.game.deal()
        self.post(self.display_cards(self.game.community_cards))
