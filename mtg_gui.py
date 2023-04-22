#import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs.dialogs import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
import shutil

from MTGDeck import MagicDeck

class MTGDeckGUI:
    def __init__(self, root):
        self.root = root
        self.height = 720
        self.width = 1280
        self.root.geometry(f"{self.width}x{self.height}")


        self.deck = None
        self.deck_image = None
        self.current_deck_name = ''
        self.canvas_plot = None
        self.deck_image_label = None

        #LABEL FRAMES:
        # create a label frame to hold images, plots, etc.
        self.label_frame = tk.LabelFrame(
            self.root, 
            text="Deck Image", 
            width=int(self.width*0.50), 
            height=int(self.height*0.75)
        )
        self.label_frame.place(x=int(self.width*0.50), y=150, width=int(self.width*0.49), height=int(self.height*0.75))

        #frame tho select plots, images, synergies, etc.
        self.frame_2 = tk.LabelFrame(
            self.root, 
            text="Select Display"
        )
        self.frame_2.place(x=int(self.width*0.50), y=10, width=int(self.width*0.49), height=110)

        #frame tho select plots, images, synergies, etc.
        self.frame1 = tk.LabelFrame(
            self.root, 
            text="Deck Lab"
        )
        self.frame1.place(x=10, y=10, width=int(self.width*0.45), height=110)


        #Create Deck button
        self.create_deck_button = tk.Button(
            self.frame1, 
            width=10 ,
            text="Create Deck", 
            bootstyle='success, outline' ,
            command=self.create_deck
        )
        self.create_deck_button.place(relx=0.01, y=5)

        #Create Deck label
        self.deck_name_entry = tk.Entry(self.frame1)
        self.deck_name_entry.place(x=115, y=5, relwidth=0.48)

        #import deck button
        self.create_deck_button = tk.Button(
            self.frame1, 
            width=12 ,
            text="Import Deck", 
            bootstyle='outline' ,
            command=self.import_deck
        )
        self.create_deck_button.place(relx=0.69, y=5)



        #add card button
        self.add_card_button = tk.Button(
            self.frame1, 
            width=10, 
            text="Add Card", 
            command=self.add_card2deck
        )
        self.add_card_button.place(relx=0.01, y=45)
        
        #card name label
        self.card_name_entry = tk.Entry(self.frame1)
        self.card_name_entry.place(x=115, y=45, relwidth=0.48)

        #number of cards selector
        self.card_number_var = tk.StringVar(self.frame1)
        self.card_number_var.set("0")
        self.card_number_dropdown = tk.OptionMenu(
            self.frame1, 
            self.card_number_var, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
        )
        self.card_number_dropdown.place(relx=0.69, y=45)

        #eliminate card (trash):
        trash_img = PhotoImage(file="icons/trash.png")
        self.remove_card_button = tk.Button(
            self.frame1, 
            width=10, 
            image=trash_img, 
            text='Remove', 
            command=self.remove_card
        )
        self.remove_card_button.place(relx=0.8, y=45)
        


        # #Deck info table
        # self.cards_label = tk.Label(self.root, text="Deck Info:", font=('default', 16))
        # self.cards_label.place(x=10, y=110)

        #Deck table initialization:
        coldata = [
            {"text": "Nº", "stretch": True, 'width':int(self.width*0.02)},
            {"text": "Name", "stretch": True, 'width':int(self.width*0.11)},
            {"text": "Atack", "stretch": True, 'width':int(self.width*0.04)},
            {"text": "Defense", "stretch": True, 'width':int(self.width*0.05)},
            {"text": "Description", "stretch": True, 'width':int(self.width*0.15), 'minwidth':int(self.width*0.023)}
        ]
        rowdata = [
        ]

    
        self.deck_table = Tableview(
            master=self.root,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            pagesize=30,
            searchable=True,
            bootstyle=PRIMARY,
            autofit=True
        )
        self.deck_table.place(x=10, y=150, width=int(self.width*0.45), height=self.height*0.95 )

        
        
        #add image deck button
        self.add_image_button = tk.Button(
            self.frame_2, 
            bootstyle="outline",
            width=15, 
            text="Show deck image", 
            command=self.show_deck_image
        )
        self.add_image_button.place(relx=0.15, rely=0.5, anchor="center")

        #add plot deck button
        self.add_plot_button = tk.Button(
            self.frame_2, 
            bootstyle="outline",
            width=15, 
            text="Show mana plot", 
            command=self.show_mana_curve
        )
        self.add_plot_button.place(relx=0.5, rely=0.5, anchor="center")

        #add plot synergy button
        self.add_syn_button = tk.Button(
            self.frame_2, 
            bootstyle="outline",
            width=15, 
            text="Show synergies", 
            command=self.show_mana_curve
        )
        self.add_syn_button.place(relx=0.85, rely=0.5, anchor="center")
        
        # Bind the <Configure> event of self.root to a function that sets the height of self.deck_table
        self.root.bind("<Configure>", self.on_window_resize)



    def on_window_resize(self, event):
        # Get the current height of self.root and set the height of self.deck_table accordingly
        self.height = self.root.winfo_height() 
        self.width = self.root.winfo_width()
        self.update_sizes()     
        #print(self.height)

    def update_sizes(self):
        #Update lable frames:
        self.label_frame.place(x=int(self.width*0.50), y=150, width=int(self.width*0.49), height=int(self.height*0.75))
        self.frame_2.place(x=int(self.width*0.50), y=10, width=int(self.width*0.49), height=110)
        self.frame1.place(x=10, y=10, width=int(self.width*0.45), height=110)

        #update component sizes
        self.deck_table.place(x=10, y=150, width=(self.width*0.45), height=self.height*0.76 )
        #self.add_image_button.place(x=self.width*0.65, y=self.height*0.0277)

        #Update plot size        
        if self.canvas_plot and self.canvas_plot.get_tk_widget():
            self.canvas_plot.get_tk_widget().place(x=0, y=0, width=self.label_frame.winfo_width(), height=self.label_frame.winfo_height())


    def create_directory(self):
        os.makedirs(f"Decks/{self.deck_name}")
        self.deck = MagicDeck(self.deck_name)


    def create_deck(self):
        self.deck_name = self.deck_name_entry.get()
        # Create the directory if it does not exist
        if not os.path.exists(f"Decks/{self.deck_name}"):
            self.create_directory()
        else:
            answer = Messagebox.yesno('This deck already exists. Do you want to remove it and create a new one?', alert=True, parent=self.root)
            if answer == 'No':
                pass
            else:
                shutil.rmtree(f"Decks/{self.deck_name}")
                self.create_directory()


    def import_deck(self):
        self.deck_name = self.deck_name_entry.get()
        if self.deck_name == self.current_deck_name:
            answer = Messagebox.show_error('This Deck is already imported. Try another.')
        else:
            self.current_deck_name = self.deck_name
            self.deck = MagicDeck(self.deck_name)
            self.deck.load_deck()
            self.update_values()


    def add_card2deck(self):
        #self.deck_table.insert_row('Name', ['Marzale LLC', 26])
        name_of_card = self.card_name_entry.get()
        repeated_cards = int(self.card_number_var.get())
        if repeated_cards < 1:
            Messagebox.show_error('Please select more than one card.')
        else:
            if not self.deck.add_card(name_of_card, repeated_cards):
                Messagebox.show_error('Card not found.')
                self.card_name_entry.delete(0, 'end')
            else:
                self.card_name_entry.delete(0, 'end')

        # print('Se han añadido {} {}'.format(repeated_cards, name_of_card))
        # print(self.deck.cards[0])
        self.update_values()

    def remove_card(self):
        name_of_card = self.card_name_entry.get()
        repeated_cards = int(self.card_number_var.get())
        if repeated_cards < 1:
            Messagebox.show_error('Please select more than one card.')
        else:
            self.deck.remove_card(name_of_card, repeated_cards)

        self.update_values()

    def save_deck(self):
        pass

    def update_values(self):
        self.deck_table.delete_rows()
        for card in self.deck.cards:
            #si card.get("name") es una tierra el nombre será el card.get("type_line")
            if card.get("name") is not None: 
                self.deck_table.insert_row('end', [card.get("count"), card.get("name") , str(card.get("power")), str(card.get("toughness")), str(card.get("printed_text"))])
            else:
                print('No se detecta el nombre de {}'.format(card.get("name")))
                self.deck_table.insert_row('end', [card.get("count"), card.get("type_line") , str(card.get("power")), str(card.get("toughness")), str(card.get("printed_text"))])
        self.deck_table.reset_table()
        self.show_mana_curve()
        #self.show_deck_image()

    def show_mana_curve(self):
        #remove previous canvas
        if self.canvas_plot:
            self.canvas_plot.get_tk_widget().destroy()

        self.empty_frame(self.label_frame)
        
        # generate the plot
        self.mana_plot = self.deck.generate_mana_curve(style='bmh', show_lands=True)

        # set the figure properties
        self.mana_plot.set_size_inches(3, 5)
        self.mana_plot.tight_layout()
        self.mana_plot.subplots_adjust(top=0.9, bottom=0.2, left=0.2, right=0.9)

        # show plot on tk window
        self.canvas_plot = FigureCanvasTkAgg(self.mana_plot, master=self.label_frame)
        self.canvas_plot.draw()
        self.canvas_plot.get_tk_widget().place(x=0, y=0, width=self.label_frame.winfo_width(), height=self.label_frame.winfo_height())


                       
    def show_deck_image(self):
        if self.deck_image_label:
            self.deck_image_label.destroy()

        # if the label_frame is not empty, remove the content
        if self.label_frame.winfo_children():
            for child in self.label_frame.winfo_children():
                child.destroy()

        # generate the image
        self.deck_image = self.deck.generate_image()

        # resize the image if needed
        width = self.label_frame.winfo_width()
        height = int(self.deck_image.height * width / self.deck_image.width)
        self.deck_image = self.deck_image.resize((width, height))

        # create a PhotoImage object from the deck image
        photo_image = ImageTk.PhotoImage(self.deck_image)

        # create a label widget to display the image
        self.deck_image_label = tk.Label(self.label_frame, image=photo_image)
        self.deck_image_label.image = photo_image

        # place the label widget at the bottom of the plot
        self.deck_image_label.place(x=0, y=0, width=self.deck_image.width, height=self.deck_image.height)




    def empty_frame(self, frame_name):
        if frame_name.winfo_children():
            for child in frame_name.winfo_children():
                child.destroy()
                 

        

if __name__ == "__main__":
    root = tk.Window(themename="superhero", alpha=0.98, resizable=[640, 480], iconphoto='icons/red.png', title='MTG Deck Builder')
    mtg_deck_gui = MTGDeckGUI(root)
    root.mainloop()
