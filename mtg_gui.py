#import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import ttkbootstrap as tk
from ttkbootstrap.constants import *

from MTGDeck import MagicDeck

class MTGDeckGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")

        self.deck_name_label = tk.Label(self.root, text="Deck Name:")
        self.deck_name_label.place(x=10, y=10)

        self.deck_name_entry = tk.Entry(self.root, width=50)
        self.deck_name_entry.place(x=100, y=10)

        self.create_deck_button = tk.Button(self.root, text="Create Deck", command=self.create_deck)
        self.create_deck_button.place(x=400, y=10)

        self.card_name_label = tk.Label(self.root, text="Card Name:")
        self.card_name_label.place(x=10, y=50)

        self.card_name_entry = tk.Entry(self.root, width=50)
        self.card_name_entry.place(x=100, y=50)

        self.card_number_label = tk.Label(self.root, text="Number of Cards:")
        self.card_number_label.place(x=10, y=90)

        self.card_number_var = tk.StringVar(self.root)
        self.card_number_var.set("1")
        self.card_number_dropdown = tk.OptionMenu(self.root, self.card_number_var, "1", "2", "3", "4")
        self.card_number_dropdown.place(x=150, y=90)

        self.add_card_button = tk.Button(self.root, text="Add Card", command=self.add_card)
        self.add_card_button.place(x=400, y=50)

        self.remove_card_button = tk.Button(self.root, text="Remove Card", command=self.remove_card)
        self.remove_card_button.place(x=480, y=50)

        self.cards_label = tk.Label(self.root, text="Cards:")
        self.cards_label.place(x=10, y=130)

        self.cards_box = tk.Combobox(self.root, width=100, height=10)
        self.cards_box.place(x=10, y=150)

        self.save_button = tk.Button(self.root, text="Save Deck", command=self.save_deck)
        self.save_button.place(x=10, y=180)

        self.deck_box = tk.Label(self.root, text="")
        self.deck_box.place(x=10, y=220)

        self.deck = None

    def create_deck(self):
        deck_name = self.deck_name_entry.get()
        self.deck = MagicDeck(deck_name)

    def add_card(self):
        card_name = self.card_name_entry.get()
        card_number = int(self.card_number_var.get())
        for i in range(card_number):
            self.deck.add_card(card_name, card_number)
            self.cards_box.insert(tk.END, card_name)

    def remove_card(self):
        selection = self.cards_box.curselection()
        print(selection)
        card_number = int(self.card_number_var.get())
        print(card_number)
        if selection:
            card_name = self.cards_box.get(selection[0])
            print(card_name)
            count = self.deck.count_cards(card_name)
            print(count)
            if count >= card_number:
                for i in range(card_number):
                    self.deck.remove_card(card_name)
                self.cards_box.delete(selection[0])
                # Remove selected number of cards with the same name from cards_box
                for i in range(card_number):
                    index = self.cards_box.get(0, tk.END).index(card_name)
                    self.cards_box.delete(index)
            else:
                messagebox.showwarning("Warning", f"Cannot remove {card_number} '{card_name}' cards. Only {count} cards available in deck.")


    def save_deck(self):
        deck_image = self.deck.generate_image()
        #mantain the same aspect ratio:
        #deck_image = deck_image.resize((680, 480))
        deck_image_tk = ImageTk.PhotoImage(deck_image)
        self.deck_box.config(image=deck_image_tk)
        self.deck_box.image = deck_image_tk

if __name__ == "__main__":
    root = tk.Window(themename="superhero", alpha=0.95, resizable=[640, 480], iconphoto='icons/red.png', title='MTG Deck Builder')
    mtg_deck_gui = MTGDeckGUI(root)
    root.mainloop()
