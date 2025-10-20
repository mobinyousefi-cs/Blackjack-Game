#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: utils.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Utility helpers: Ace evaluation, safe imports, simple memoization.

Usage:
python -c "from blackjack.utils import best_ace_total; print(best_ace_total([1,11], 10))"

Notes:
- Standalone helpers to keep game.py focused.
===================================================================
"""

from __future__ import annotations
from functools import lru_cache
from typing import Iterable


def best_ace_total(base: int, aces: int) -> int:
    """Return the best hand value given a base (non-ace sum) and ace count.

    Aces can be 1 or 11; pick the highest <= 21.
    """
    # Start with all aces as 1
    total = base + aces
    # Upgrade some aces to 11 where possible (+10 each)
    for _ in range(aces):
        if total + 10 <= 21:
            total += 10
        else:
            break
    return total


@lru_cache(maxsize=None)
def suit_symbol(suit: str) -> str:
    mapping = {
        "hearts": "♥",
        "diamonds": "♦",
        "clubs": "♣",
        "spades": "♠",
    }
    return mapping.get(suit, "?")