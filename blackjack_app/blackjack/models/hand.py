from typing import List
from .card import Card

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_value(self) -> int:
        value = 0
        aces = 0

        for card in self.cards:
            if card.is_ace:
                aces += 1
            value += card.value

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21

    def is_bust(self) -> bool:
        return self.get_value() > 21

    def __str__(self) -> str:
        return " ".join(str(card) for card in self.cards) 