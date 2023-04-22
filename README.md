# MTG-Deck
This repository contains a tool for managing and analyzing Magic: The Gathering (MTG) decks. 
With this code, you can create, load and modify Magic The Gathering Decks and generate a graphical representation of the deck's mana curve in order to analyze the balance of your deck. Additionally, a JSON file is generated with all the card information, including name, mana cost, type, text, url, price, etc.

## Usage

Follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Open the GUI. The main functionalities are:
  - Ceate deck with custom name
  - Add/Remove cards to the created Deck (The deck is saved automatically)
  - If you have Decks already created you can load those decks and work with it

The program has a simple and easy to use interface:

![GUI](https://github.com/VictorEscribano/MTG-Deck/blob/main/Graphic%20Material/GUI_image.PNG)


## Future work

This tool is still in development, and there are several possible improvements and extensions that could be added in the future. Some ideas include:

- Adding the image mana cost to the GUI
- Add synergy graph based on the 17Lands API using the GIH (Game in Hand) metric
- Apply dimensionality reduction techniques to see the less relevant cards of the deck.
- Adding support for different output formats (e.g. CSV, Excel, LaTeX).
- Implementing more sophisticated analysis of the deck's mana curve (e.g. calculating the average mana cost, detecting color imbalances).
- Add price curve
- Adding support for other deck formats (e.g. Commander, Limited).
