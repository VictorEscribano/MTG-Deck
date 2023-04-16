from MTGDeck import *

# Create a new deck called "My Deck"
deck = MagicDeck("Example_Deck")

# Add some cards to the deck
deck.add_card("nim toxico", 2)
deck.add_card("segador de sheoldred", 1)
deck.add_card("cosechar las tumbamarinas", 1)
deck.add_card("levantamuertos", 1)
deck.add_card("purgar las tumbas", 1)
deck.add_card("Necrofago ciego", 1)
deck.add_card("gato negro", 1)
deck.add_card("necrofago de la tumbanefasta", 1)
deck.add_card("necrofago aristocrata", 1)
deck.add_card("necrofago del matadero", 1)
deck.add_card("desliz tragico", 1)
deck.add_card("sed de sorin", 1)
deck.add_card("Swamp", 8)

deck.remove_card('Nim tóxico')

deck.save_deck()

deck.generate_image()

