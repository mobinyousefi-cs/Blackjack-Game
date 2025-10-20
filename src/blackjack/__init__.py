#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: __init__.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Package init. Exposes public API and module metadata.

Usage:
python -m blackjack

Notes:
- Follows src/ layout for clean imports.
===================================================================
"""

from .game import Card, Deck, Hand, GameState

__all__ = ["Card", "Deck", "Hand", "GameState"]
__version__ = "0.1.0"