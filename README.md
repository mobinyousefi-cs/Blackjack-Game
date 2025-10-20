# Blackjack (Tkinter)

A clean, testable Blackjack (21) game with a Tkinter GUI. Images are generated at first run—no asset downloads required.

## Features
- Standard 52-card deck, Ace = 1/11, face cards = 10
- Dealer auto-plays on Stand (hits to 17+)
- Buttons: New Game, Hit, Stand (enabled when hand > 11), Shuffle Deck, Quit
- Lightweight asset pipeline using Pillow (fallback to text cards if Pillow missing)
- `src/` layout, tests with `pytest`, CI with Ruff + Black + PyTest

## Install & Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m blackjack
```

## Controls
- **New Game**: Deal 2 cards each
- **Hit**: Draw a card for player
- **Stand**: Lock player, dealer draws to 17+
- **Shuffle**: Reshuffle remaining deck (or reset deck if empty)

## Tests
```bash
pytest -q
```

## Packaging
```bash
pip install build
python -m build
```

## License
MIT