import random
from typing import List
from .card import Card

class Deck:
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALUES = {
        "A": 11,
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 10, "Q": 10, "K": 10
    }

    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        self.cards = []
        for rank in self.RANKS:
            self.cards.append(Card(rank=rank, value=self.VALUES[rank]))
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        if not self.cards:
            self.reset()
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards) 