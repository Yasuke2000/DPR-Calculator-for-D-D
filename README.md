# D&D DPR Calculator

A small web application for computing expected damage per round (DPR) for Dungeons & Dragons 5e attacks.  
It also reports the chance of hitting at least once across multiple attacks.

## Features
- Probability calculations with advantage or disadvantage
- Critical hit range support
- Chance to hit at least once across several attacks
- Simple Flask web interface
- Ability score roller (4d6 drop lowest)
- Random Tarokka card draw for Curse of Strahd
- Barovian encounter generator
- Random NPC name generator

## Getting Started
Install dependencies and run the development server:

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in a browser and fill out the form.

## Running tests
The core DPR logic is covered by unit tests.  Run them with:

```bash
pytest
```

## License
This project is licensed under the terms of the MIT license.
