from tkinter import *
import os
from PIL import ImageTk, Image
from MagicDeck import MagicDeck


class DeckViewer:
    def __init__(self, master):
        self.master = master
        self.current_deck = None
        self.current_lands = None
        self.current_image = None
        self.deck_name = ''

        # Set up initial screen with options to create or select a deck
        self.init_screen()

    def init_screen(self):
        self.master.title("Deck Viewer")

        # Create label and entry for entering new deck name
        new_deck_label = Label(self.master, text="Create New Deck:")
        new_deck_label.pack()
        self.new_deck_entry = Entry(self.master)
        self.new_deck_entry.pack()

        # Create listbox for selecting existing deck
        existing_deck_label = Label(self.master, text="Select Existing Deck:")
        existing_deck_label.pack()
        self.deck_listbox = Listbox(self.master)
        self.deck_listbox.pack()

        # Add existing decks to listbox
        self.load_existing_decks()

        # Add buttons for creating new deck and selecting existing deck
        create_button = Button(self.master, text="Create Deck", command=self.create_deck)
        create_button.pack()
        select_button = Button(self.master, text="Select Deck", command=self.select_deck)
        select_button.pack()

    def create_deck(self):
        self.deck_name = self.new_deck_entry.get()
        deck = MagicDeck(name=self.deck_name)
        self.deck_listbox.insert(END, self.deck_name)
        deck_creator = DeckCreator(self.master, deck)

    def select_deck(self):
        self.deck_name = self.deck_listbox.get(self.deck_listbox.curselection())
        print(self.deck_name)
        self.deck = MagicDeck(self.deck_name)
        self.current_deck = self.deck.load_deck(self.deck_name)
        self.display_deck()

    def select_lands(self):
        self.deck_name = self.deck_listbox.get(self.deck_listbox.curselection())
        self.current_lands = MagicDeck.load_lands(self.deck_name)

    def display_deck(self):
        # Create new window to display deck
        deck_window = Toplevel(self.master)
        deck_window.title("Deck: {}".format(self.deck_name))

        # Create label for displaying card names
        self.card_label = Label(deck_window, text="")
        self.card_label.pack()

        # Create canvas for displaying deck image
        canvas_width = 800
        canvas_height = 600
        self.canvas = Canvas(deck_window, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # read the image
        try: 
            combined_image = Image.open("Decks\{}\deck.png".format(self.deck_name))
        except:
            print('Image does not exist creating one')
            #TODO

        # Resize combined image to fit on canvas
        canvas_ratio = canvas_width / canvas_height
        image_ratio = combined_image.width / combined_image.height
        if canvas_ratio > image_ratio:
            # Canvas is wider than image, resize to canvas height
            new_height = int(canvas_height * 0.9)
            new_width = int(new_height * image_ratio)
        else:
            # Canvas is taller than image, resize to canvas width
            new_width = int(canvas_width * 0.9)
            new_height = int(new_width / image_ratio)
        combined_image = combined_image.resize((new_width, new_height), Image.ANTIALIAS)

        # Display deck image on canvas
        self.image_tk = ImageTk.PhotoImage(combined_image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # Display mana icons
        mana_counts = self.current_deck.count_mana()
        mana_types = ["White", "Blue", "Black", "Red", "Green"]
        for i, mana_type in enumerate(mana_types):
            icon_path = "icons/{}.png".format(mana_type.lower())
            icon_image = Image.open(icon_path).resize((50,50), Image.ANTIALIAS)
            icon_tk = ImageTk.PhotoImage(icon_image)
            mana_label = Label(deck_window, image=icon_tk, text="{}: {}".format(mana_type, mana_counts[i]))
            mana_label.image = mana_label.pack(side=LEFT, padx=10)
            mana_label.image = icon_tk  # keep a reference to the image to avoid garbage collection



    def load_existing_decks(self):
        # Load existing decks from saved file and add to listbox
        decks = MagicDeck.get_deck_names()
        for deck_name in decks:
            self.deck_listbox.insert(END, deck_name)

    def update_display(self):
        # Clear current display and update with current deck
        self.card_label.config(text="")
        self.canvas.delete("all")
        card_images = []
        for card in self.current_deck.cards:
            image = Image.open(card.image_path)
            card_images.append(image)
        self.current_image = Image.new('RGB', (800, 600))
        x_offset = 0
        for card_image in card_images:
            self.current_image.paste(card_image, (x_offset, 0))
            x_offset += card_image.size[0]
        self.image_tk = ImageTk.PhotoImage(self.current_image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # Update mana counts
        mana_counts = self.current_deck.count_mana()
        mana_types = ["White", "Blue", "Black", "Red", "Green"]
        for i, mana_type in enumerate(mana_types):
            mana_label = self.mana_labels[i]
            mana_label.config(text="{}: {}".format(mana_type, mana_counts[i]))

    def add_card(self, card):
        self.current_deck.add_card(card)
        self.update_display()

    def remove_card(self, card):
        self.current_deck.remove_card(card)
        self.update_display()




class DeckCreator:

    def __init__(self, master, deck):
        self.master = master
        self.deck = deck
        self.root = Tk()
        self.root.title("Crear nuevo mazo")

        self.card_entries = []
        self.land_entries = {}
        self.deck_name_entry = None

        # Deck name label and entry
        deck_name_label = Label(self.root, text="Nombre del mazo:")
        deck_name_label.grid(row=0, column=0)
        self.deck_name_entry = Entry(self.root)
        self.deck_name_entry.grid(row=0, column=1)

        # Card entries
        card_label = Label(self.root, text="Cartas:")
        card_label.grid(row=1, column=0)
        self.add_card_entry()

        # Land entries
        land_label = Label(self.root, text="Tierras:")
        land_label.grid(row=2, column=0)
        self.add_land_entry("Plains")
        self.add_land_entry("Island")
        self.add_land_entry("Swamp")
        self.add_land_entry("Mountain")
        self.add_land_entry("Forest")

        # Submit button
        submit_button = Button(self.root, text="Crear mazo", command=self.create_deck)
        submit_button.grid(row=4, column=0)

        self.root.mainloop()

    def add_card_entry(self):
        card_entry = Entry(self.root)
        card_entry.grid(row=len(self.card_entries) + 1, column=1)
        self.card_entries.append(card_entry)

    def add_land_entry(self, land_name):
        land_label = Label(self.root, text=land_name)
        land_label.grid(row=len(self.land_entries) + 3, column=0)
        land_entry = Entry(self.root)
        land_entry.grid(row=len(self.land_entries) + 3, column=1)
        self.land_entries[land_name] = land_entry

    def create_deck(self):
        deck_name = self.deck_name_entry.get()
        deck = MagicDeck(name=deck_name)

        # Add cards to deck
        for card_entry in self.card_entries:
            card_name = card_entry.get().strip()
            if card_name:
                deck.add_card(card_name)

        # Add lands to deck
        lands = {}
        for land_name, land_entry in self.land_entries.items():
            land_count = land_entry.get().strip()
            if land_count:
                lands[land_name] = int(land_count)
        deck.add_lands(lands)

        deck.save_card_data()
        deck.save_land_data()
        deck.generate_image()

        self.root.destroy()


           
# Create main window
root = Tk()

# Create DeckViewer object and run main loop
deck_viewer = DeckViewer(root)
root.mainloop()