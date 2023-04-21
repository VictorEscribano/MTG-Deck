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

![GUI](https://github.com/VictorEscribano/MTG-Deck/blob/main/Graphic%20Material/GUI.PNG)




## Results

This will output 2 .json files, one for the cards related to creatures, artifacts, spells, etc. and other json for the lands.
Also a .png of the card balance will be created.
Here we can see a Jumpstart Golem deck and apreciate the balance of mana cost:

![Mana curve](https://github.com/VictorEscribano/MTG-Deck/blob/main/Decks/Jumpstart%20de%20Golems/deck.png)

The same with this Toxic/Zombie jumpstart Deck:
![Mana curve](https://github.com/VictorEscribano/MTG-Deck/blob/main/Decks/Toxico%20Zombie/deck.png)

On the other hand this Triton jumpstart Deck is not balanced as it has too few low mana cost cards and too many mid cost ones:
![Mana curve](https://github.com/VictorEscribano/MTG-Deck/blob/main/Decks/Tritones/deck.png)




## Future work

This tool is still in development, and there are several possible improvements and extensions that could be added in the future. Some ideas include:

- Adding support for different output formats (e.g. CSV, Excel, LaTeX).
- Implementing more sophisticated analysis of the deck's mana curve (e.g. calculating the average mana cost, detecting color imbalances).
- Integrating with online MTG databases to automatically fetch card information and prices.
- Adding support for other deck formats (e.g. Commander, Limited).
