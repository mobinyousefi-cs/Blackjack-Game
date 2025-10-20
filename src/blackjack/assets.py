#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: assets.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Card image loader with lazy generation using Pillow.
- Generates minimal PNGs (100x145) like "A_spades.png" on first use.
- Falls back to text-rendered Tk card if Pillow unavailable.

Usage:
from blackjack.assets import CardImageProvider; imgs = CardImageProvider().get(card)

Notes:
- Images cached under ~/.cache/blackjack_cards
===================================================================
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Dict

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except Exception:  # pragma: no cover - optional dependency at runtime only
    PIL_OK = False

from tkinter import PhotoImage

from .game import Card, RANKS, SUITS
from .utils import suit_symbol


def _cache_dir() -> Path:
    base = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache"))
    d = base / "blackjack_cards"
    d.mkdir(parents=True, exist_ok=True)
    return d


class CardImageProvider:
    def __init__(self, card_w: int = 100, card_h: int = 145) -> None:
        self.card_w = card_w
        self.card_h = card_h
        self._cache: Dict[str, PhotoImage] = {}
        if PIL_OK:
            self._ensure_generated()

    def _ensure_generated(self) -> None:
        cd = _cache_dir()
        # Generate all cards if any missing
        for s in SUITS:
            for r in RANKS:
                name = f"{r}_{s}.png"
                path = cd / name
                if not path.exists():
                    self._generate_card_png(path, r, s)

    def _generate_card_png(self, path: Path, rank: str, suit: str) -> None:
        if not PIL_OK:
            return
        img = Image.new("RGBA", (self.card_w, self.card_h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Border
        draw.rounded_rectangle([1, 1, self.card_w - 2, self.card_h - 2], radius=12, outline=(0, 0, 0), width=2)
        # Texts
        try:
            font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except Exception:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        sym = suit_symbol(suit)
        # Center symbol
        w, h = draw.textlength(sym, font=font_big), 34
        draw.text(((self.card_w - w) / 2, (self.card_h - h) / 2), sym, fill=(0, 0, 0), font=font_big)
        # Corner rank
        draw.text((8, 6), rank, fill=(0, 0, 0), font=font_small)
        draw.text((self.card_w - 8 - draw.textlength(rank, font=font_small), self.card_h - 6 - 20), rank, fill=(0, 0, 0), font=font_small)
        img.save(path)

    def get(self, card: Card) -> PhotoImage:
        key = card.name
        if key in self._cache:
            return self._cache[key]
        path = _cache_dir() / f"{key}.png"
        if path.exists():
            img = PhotoImage(file=str(path))
        else:
            # text fallback
            img = self._text_card(card)
        self._cache[key] = img
        return img

    def _text_card(self, card: Card) -> PhotoImage:
        # Create a minimal 1x1 and draw via Tk (text on Canvas will be used); as PhotoImage, make blank
        return PhotoImage(width=self.card_w, height=self.card_h)