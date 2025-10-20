#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
Project: Blackjack (Tkinter)
File: main.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi)
Created: 2025-10-20
Updated: 2025-10-20
License: MIT License (see LICENSE file for details)
===================================================================

Description:
Tkinter GUI for Blackjack with controls (New, Hit, Stand, Shuffle, Quit).

Usage:
python -m blackjack

Notes:
- Uses CardImageProvider to display cards; falls back to drawn rectangles if assets missing.
===================================================================
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox

from .game import GameState, Card
from .assets import CardImageProvider
from .utils import suit_symbol

CARD_W, CARD_H = 100, 145


class BlackjackApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Blackjack — Mobin Yousefi")
        self.resizable(False, False)
        self.state = GameState()
        self.images = CardImageProvider(card_w=CARD_W, card_h=CARD_H)

        self._build_ui()
        self._new_game()

    # --- UI Construction -------------------------------------------------
    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.grid(sticky="nsew")

        # Dealer & Player frames
        self.dealer_frame = ttk.LabelFrame(root, text="Dealer", padding=10)
        self.dealer_frame.grid(row=0, column=0, sticky="ew")
        self.player_frame = ttk.LabelFrame(root, text="Player", padding=10)
        self.player_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        # Canvas for cards
        self.dealer_canvas = tk.Canvas(self.dealer_frame, width=520, height=CARD_H + 16, bg="#0a0a0a")
        self.dealer_canvas.pack()
        self.player_canvas = tk.Canvas(self.player_frame, width=520, height=CARD_H + 16, bg="#0a0a0a")
        self.player_canvas.pack()

        # Info bar
        info = ttk.Frame(root)
        info.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.status_var = tk.StringVar(value="Welcome to Blackjack!")
        ttk.Label(info, textvariable=self.status_var).pack(side=tk.LEFT)
        self.deck_var = tk.StringVar(value="Deck: 52")
        ttk.Label(info, textvariable=self.deck_var).pack(side=tk.RIGHT)

        # Controls
        controls = ttk.Frame(root)
        controls.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.btn_new = ttk.Button(controls, text="New Game", command=self._new_game)
        self.btn_hit = ttk.Button(controls, text="Hit", command=self._hit)
        self.btn_stand = ttk.Button(controls, text="Stand", command=self._stand)
        self.btn_shuffle = ttk.Button(controls, text="Shuffle", command=self._shuffle)
        self.btn_quit = ttk.Button(controls, text="Quit", command=self.destroy)
        for i, b in enumerate([self.btn_new, self.btn_hit, self.btn_stand, self.btn_shuffle, self.btn_quit]):
            b.grid(row=0, column=i, padx=4)

        # Style
        self._apply_theme()

    def _apply_theme(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

    # --- Game actions ----------------------------------------------------
    def _new_game(self) -> None:
        self.state.new_round()
        self._update_status("New round: try to reach 21 without busting.")
        self._refresh()

    def _hit(self) -> None:
        if not self.state.in_round:
            return
        self.state.hit()
        if self.state.outcome == "dealer":
            self._update_status("Bust! Dealer wins.")
        self._refresh()

    def _stand(self) -> None:
        if not self.state.in_round:
            return
        if self.state.player_hand.value <= 11:
            messagebox.showinfo("Stand", "You can stand only when your total > 11.")
            return
        self.state.stand()
        self._announce_outcome()
        self._refresh()

    def _shuffle(self) -> None:
        self.state.deck.shuffle()
        self._update_status("Deck shuffled.")
        self._refresh()

    # --- Helpers ---------------------------------------------------------
    def _refresh(self) -> None:
        # Update deck counter
        self.deck_var.set(f"Deck: {self.state.deck.remaining()}")
        # Draw cards
        self._draw_hand(self.dealer_canvas, self.state.dealer_hand.cards, hide_first=self.state.in_round)
        self._draw_hand(self.player_canvas, self.state.player_hand.cards, hide_first=False)
        # Enable/disable controls
        can_play = self.state.in_round
        self.btn_hit.configure(state=tk.NORMAL if can_play else tk.DISABLED)
        self.btn_stand.configure(state=tk.NORMAL if can_play else tk.DISABLED)

    def _draw_hand(self, canvas: tk.Canvas, cards: list[Card], hide_first: bool) -> None:
        canvas.delete("all")
        x, y = 10, 8
        for idx, card in enumerate(cards):
            if idx == 0 and hide_first:
                self._draw_back(canvas, x, y)
            else:
                self._draw_card(canvas, x, y, card)
            x += CARD_W + 12
        # Totals
        if not hide_first:
            total = sum(c.value for c in cards if c.rank != "A")
            # We show dynamic total via game state; optional overlay could be added

    def _draw_card(self, canvas: tk.Canvas, x: int, y: int, card: Card) -> None:
        img = self.images.get(card)
        if img.width() > 1 and img.height() > 1:  # actual image loaded
            canvas.create_image(x, y, image=img, anchor=tk.NW)
        else:
            # Text fallback (no Pillow): draw a simple card
            r = 12
            canvas.create_rectangle(x, y, x + CARD_W, y + CARD_H, outline="white", width=2, radius=r)
            canvas.create_text(x + 14, y + 14, text=card.rank, anchor=tk.NW, fill="white", font=("Segoe UI", 12, "bold"))
            canvas.create_text(x + CARD_W / 2, y + CARD_H / 2, text=suit_symbol(card.suit), fill="white", font=("Segoe UI", 20, "bold"))

    def _draw_back(self, canvas: tk.Canvas, x: int, y: int) -> None:
        r = 12
        canvas.create_rectangle(x, y, x + CARD_W, y + CARD_H, outline="white", width=2, radius=r)
        canvas.create_rectangle(x + 6, y + 6, x + CARD_W - 6, y + CARD_H - 6, outline="white")
        canvas.create_text(x + CARD_W / 2, y + CARD_H / 2, text="★", fill="white", font=("Segoe UI", 24))

    def _update_status(self, msg: str) -> None:
        self.status_var.set(msg)

    def _announce_outcome(self) -> None:
        outcome = self.state.outcome
        if outcome == "player":
            self._update_status("You win! 🎉")
        elif outcome == "dealer":
            self._update_status("Dealer wins.")
        else:
            self._update_status("Push (tie).")


def main() -> None:
    app = BlackjackApp()
    app.mainloop()


if __name__ == "__main__":
    main()