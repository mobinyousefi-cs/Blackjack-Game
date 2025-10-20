#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: test_game.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Unit tests for core game logic (no GUI).

Usage:
pytest -q

Notes:
- Focus on ace handling and outcome comparisons.
===================================================================
"""

from blackjack.game import Hand, Card, GameState


def test_ace_evaluation():
    h = Hand()
    h.add(Card("A", "spades"))
    h.add(Card("9", "hearts"))
    assert h.value == 20
    h.add(Card("A", "clubs"))
    assert h.value == 21  # 11 + 9 + 1


def test_blackjack_and_bust():
    h = Hand()
    h.add(Card("A", "spades"))
    h.add(Card("K", "hearts"))
    assert h.is_blackjack()
    h2 = Hand()
    for r in ["K", "Q", "2"]:
        h2.add(Card(r, "clubs"))
    assert h2.is_bust()


def test_compare_outcomes():
    g = GameState()
    g.player_hand.cards = [Card("10", "hearts"), Card("9", "spades")]
    g.dealer_hand.cards = [Card("9", "hearts"), Card("9", "clubs")]
    assert g._compare() == "player"
    g.dealer_hand.cards = [Card("10", "hearts"), Card("9", "clubs")]
    assert g._compare() == "push"
    g.dealer_hand.cards = [Card("10", "hearts"), Card("K", "clubs")]
    assert g._compare() == "dealer"