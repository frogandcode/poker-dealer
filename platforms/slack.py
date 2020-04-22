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

    def post(self, player, message):
        self.client.chat_postMessage(channel=player.id, text=message)

    def display_hands(self):
        for player in self.game.players:
            message = '*NEW GAME*\n---------- Your Hand ----------'
            message += f'\n{self.display_cards(self.game.hands[player])}'

            self.post(player=player, message=message)

    def display_the_flop(self):
        for player in self.game.players:
            message = f'---------- The Flop ----------\n'
            message += self.display_cards(self.game.community_cards)

            self.post(player=player, message=message)

    def display_the_turn(self):
        self.display_community_cards('Turn')

    def display_the_river(self):
        self.display_community_cards('River')

    def display_community_cards(self, stage):
        for player in self.game.players:
            message = f'---------- The {stage} ----------\n'
            message += f'{self.display_cards(self.game.community_cards)}    (community)\n\n\n'
            message += f'{self.display_cards(self.game.hands[player])}    (you)'

            self.post(player=player, message=message)

    def display_revealed_hands(self, players):
        message = '---------- Hands Revealed ----------'
        for player in players:
            message += f'\n{self.display_cards(self.game.hands[player])}    ({player.name})\n'

        for player in self.game.players:
            self.post(player=player, message=message)

    def simulate(self):
        # Play all 4 stages of a game
        for i in range(4):
            self.deal()
