from MTGDeck import MagicDeck
import time


def main():
    start_time = time.time()
    deck = MagicDeck("testing")
    print(f"Deck initialization time: {time.time() - start_time:.2f}s")

    start_time = time.time()
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
    print(f"Cards adding time: {time.time() - start_time:.2f}s")

    start_time = time.time()
    deck.remove_card('Nim tóxico', 1)
    print(f"Card removing time: {time.time() - start_time:.2f}s")

    start_time = time.time()
    deck.generate_mana_curve(style='dark_background', show_lands=False)
    print(f"Mana curve generation time: {time.time() - start_time:.2f}s")

    start_time = time.time()
    deck.save_deck()
    print(f"Deck saving time: {time.time() - start_time:.2f}s")

    start_time = time.time()
    deck.generate_image()
    print(f"Image generation time: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
