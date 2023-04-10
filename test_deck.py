from MagicDeck import *

# Create a new deck called "My Deck"
deck = MagicDeck("Toxico Zombie")

# Add some cards to the deck
deck.add_card("nim toxico")
deck.add_card("segador de sheoldred")
deck.add_card("cosechar las tumbamarinas")
deck.add_card("levantamuertos")
deck.add_card("purgar las tumbas")
deck.add_card("Necrofago ciego")
deck.add_card("gato negro")
deck.add_card("necrofago de la tumbanefasta")
deck.add_card("necrofago aristocrata")
deck.add_card("necrofago del matadero")
deck.add_card("desliz tragico")
deck.add_card("sed de sorin")

# Add some lands to the deck
deck.add_lands({"Swamp": 8, "Island": 0, "Forest": 0})

# Save the deck to a file
deck.save_card_data()
deck.save_land_data()

deck.generate_image()