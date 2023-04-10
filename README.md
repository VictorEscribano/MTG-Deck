# MTG-Deck
This repository contains a tool for managing and analyzing Magic: The Gathering (MTG) decks. 
With this code, you can load a list of cards from a file and generate a graphical representation of the deck's mana curve, showing the distribution of mana costs across the cards. Additionally, a JSON file is generated with all the card information, including name, mana cost, type, and text.

## Usage

To use this tool, you need to have Python 3 installed on your computer. Once you have Python installed, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. fill the test_deck.py with the names of your cards (avoid symbols)

## Results

This will output 2 .json files, one for the cards related to creatures, artifacts, spells, etc. and other json for the lands.
Also a .png of the card balance will be created:
![Mana curve](https://github.com/VictorEscribano/MTG-Deck/blob/main/Decks/Jumpstart%20de%20Golems/deck.png)

![Mana curve](https://github.com/VictorEscribano/MTG-Deck/blob/main/Decks/Toxico%20Zombie/deck.png)



## Future work

This tool is still in development, and there are several possible improvements and extensions that could be added in the future. Some ideas include:

- Adding support for different output formats (e.g. CSV, Excel, LaTeX).
- Implementing more sophisticated analysis of the deck's mana curve (e.g. calculating the average mana cost, detecting color imbalances).
- Integrating with online MTG databases to automatically fetch card information and prices.
- Adding support for other deck formats (e.g. Commander, Limited).
