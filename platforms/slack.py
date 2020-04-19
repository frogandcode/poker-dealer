import os
from slack import WebClient

import poker

class Dealer(poker.Dealer):
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
        message = '*NEW GAME*\n---------- Player hands ----------'
        for player in self.game.players:
            message += f'\n{player.name}\n{self.display_cards(self.game.hands[player])}'

        self.post(message)

    def display_the_flop(self):
        self.display_community_cards('Flop')

    def display_the_turn(self):
        self.display_community_cards('Turn')

    def display_the_river(self):
        self.display_community_cards('River')

    def display_community_cards(self, name):
        message = f'---------- The {name} ----------\n'
        message += self.display_cards(self.game.community_cards)

        self.post(message)

    def simulate(self):
        # Play all 4 stages of a game
        for i in range(4):
            self.deal()
