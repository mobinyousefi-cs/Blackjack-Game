#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: game.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Core game domain: Card, Deck, Hand, and GameState with rules:
- Standard 52-card deck
- Ace = 1/11, J/Q/K = 10
- Dealer hits until 17 or more

Usage:
python -c "from blackjack.game import GameState; g=GameState(); g.new_round(); print(g.player_hand.value)"

Notes:
- Pure logic, UI-agnostic and testable.
===================================================================
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import List, Tuple

from .utils import best_ace_total

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["hearts", "diamonds", "clubs", "spades"]


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def name(self) -> str:
        return f"{self.rank}_{self.suit}"

    @property
    def value(self) -> int:
        if self.rank in {"J", "Q", "K"}:
            return 10
        if self.rank == "A":
            return 1
        return int(self.rank)


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = [Card(r, s) for s in SUITS for r in RANKS]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            # Recreate fresh deck if exhausted
            self.__init__()
        return self.cards.pop()

    def remaining(self) -> int:
        return len(self.cards)


class Hand:
    def __init__(self) -> None:
        self.cards: List[Card] = []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def value(self) -> int:
        base = sum(c.value for c in self.cards if c.rank != "A")
        aces = sum(1 for c in self.cards if c.rank == "A")
        return best_ace_total(base, aces)

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value == 21

    def is_bust(self) -> bool:
        return self.value > 21


@dataclass
class GameState:
    deck: Deck = field(default_factory=Deck)
    player_hand: Hand = field(default_factory=Hand)
    dealer_hand: Hand = field(default_factory=Hand)
    in_round: bool = False
    outcome: str | None = None  # "player", "dealer", "push"

    def reset(self) -> None:
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.in_round = False
        self.outcome = None

    def new_round(self) -> None:
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        # Ensure sufficient cards
        if self.deck.remaining() < 10:
            self.deck = Deck()
        # Initial deal
        self.player_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())
        self.player_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())
        self.in_round = True
        self.outcome = None

    def hit(self) -> None:
        if not self.in_round:
            return
        self.player_hand.add(self.deck.draw())
        if self.player_hand.is_bust():
            self.outcome = "dealer"
            self.in_round = False

    def stand(self) -> None:
        if not self.in_round:
            return
        # Dealer plays to 17+
        while self.dealer_hand.value < 17:
            self.dealer_hand.add(self.deck.draw())
        self.in_round = False
        self.outcome = self._compare()

    def _compare(self) -> str:
        if self.player_hand.is_bust():
            return "dealer"
        if self.dealer_hand.is_bust():
            return "player"
        pv, dv = self.player_hand.value, self.dealer_hand.value
        if pv > dv:
            return "player"
        if dv > pv:
            return "dealer"
        return "push"