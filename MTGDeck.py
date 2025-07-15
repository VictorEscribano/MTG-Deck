import json
import os
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

class MagicDeck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.card_images_PATH = f"Decks/{self.name}/card_images/"

    def get_api_data(self, card_name):
        response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}")
        if response.status_code != 200:
            print(f"Error: Card '{card_name}' not found")
            return
        
        data = json.loads(response.content)
        return data
    
    def add_card(self, card_name, num, save_card_image=True):
                
        data = self.get_api_data(card_name)
        
        if data.get("printed_name") ==  None:
            namesito = data.get("name")
            descrip = data.get("oracle_text")
        else:
            namesito = data.get("printed_name")
            descrip = data.get("printed_text")

        #load the desired data in a json
        card_data = {
                "url": data['image_uris']['small'],
                "name": namesito,
                "mana_cost": data.get("mana_cost"),
                "cmc": data.get("cmc"),
                "type_line": data.get("type_line"),
                "power": data.get("power"),
                "toughness": data.get("toughness"),
                "keywords": data.get("keywords"),
                "printed_text": descrip,
                "count": num
            }
        
        #check if the card data is allready on the self.cards:
        for card in self.cards:
            if card.get('name') == card_data.get('name'):
                card['count'] += num
                self.save_deck()
                return True
                
    
        self.cards.append(card_data)

        #save the image:
        if save_card_image == True:
            image_url = data['image_uris']['small']

            # Download the image and save it to a file
            response = requests.get(image_url)
            if response.status_code != 200:
                print(f"Error: Failed to download image for card '{card_name}'")
                return False
            
            image = Image.open(BytesIO(response.content))
            os.makedirs(self.card_images_PATH, exist_ok=True)
            
            image.save(f"{self.card_images_PATH}{card_name}.png")
            #print(f"Image saved as '{self.card_images_PATH}{card_name}.png'")

        self.save_deck()
        
        return True

    def remove_card(self, card_name ,num):
        data = self.get_api_data(card_name)
        
        if data.get("printed_name") ==  None:
            card_name = data.get("name")
        else:
            card_name = data.get("printed_name")

        for card in self.cards:
            if card.get("name") == card_name or card_name in card.get("type_line"):
                print('Removing {}...'.format(card.get("name")))
                if card.get("count") > 1:
                    card["count"] -= num
                else:
                    self.cards.remove(card)
                return

    def count_cards(self, card_name):
        print(self.cards)
        for card in self.cards:
            print(card.get("name"))
            if card.get("name") == card_name:
                return card.get("count")
            else:
                return 0

    def how_many_cards(self):
        total = 0
        for card in self.cards:
            total += card.get("count")
        return total

    def save_deck(self):
        with open(f"Decks/{self.name}/deck_cards.json", "w") as file:
            json.dump(self.cards, file, indent=4)

    def generate_mana_curve(self, style='dark_background', show_lands = True):
        self.mana_curve = {}  
        for card in self.cards:
            mana_cost = int(card.get("cmc"))
            type_line = card.get('type_line')
            if 'Basic Land' in type_line and show_lands:
                mana_cost = card.get('name')
            if mana_cost not in self.mana_curve:
                self.mana_curve[mana_cost] = 0
            self.mana_curve[mana_cost] += card.get("count")
        #ordenalo de menos a mas a menos mana cost
        if show_lands: 
            sorted_items = sorted(self.mana_curve.items(), key=lambda x: (isinstance(x[0], str), x[0]))
            self.mana_curve = dict(sorted_items)
        print(self.mana_curve) 
        
        fig, ax = plt.subplots()
        plt.style.use(style)
        # Create a bar plot of the mana curve
        x = np.arange(len(self.mana_curve))
        y = list(self.mana_curve.values())
        ax.bar(x, y, align="center")
        ax.set_xticks(x)
        ax.set_xticklabels(list(self.mana_curve.keys()))
        ax.set_xlabel("Mana Cost")
        ax.set_ylabel("Number of Cards")
        ax.set_title("Mana Curve")

        return fig

    def _parse_subtypes(self, type_line):
        """Extract creature or card subtypes from a type line."""
        if not type_line:
            return set()
        if '—' in type_line:
            subtype_part = type_line.split('—', 1)[1]
        elif '-' in type_line:
            subtype_part = type_line.split('-', 1)[1]
        else:
            return set()
        # Remove punctuation and split into words
        cleaned = subtype_part.replace(',', ' ').replace('\u2014', ' ')
        return set([s for s in cleaned.split() if s])

    def compute_synergy_matrix(self):
        """Return a matrix with pairwise subtype similarities between cards."""
        names = [card.get('name') for card in self.cards]
        subtypes = [self._parse_subtypes(card.get('type_line')) for card in self.cards]
        n = len(names)
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                union = subtypes[i] | subtypes[j]
                score = len(subtypes[i] & subtypes[j]) / len(union) if union else 0
                matrix[i][j] = matrix[j][i] = score
        return matrix, names

    def generate_synergy_plot(self):
        """Generate a heatmap showing card synergies."""
        matrix, names = self.compute_synergy_matrix()
        fig, ax = plt.subplots()
        cax = ax.imshow(matrix, cmap='YlGnBu', vmin=0, vmax=1)
        ax.set_xticks(range(len(names)))
        ax.set_yticks(range(len(names)))
        ax.set_xticklabels(names, rotation=90, fontsize=6)
        ax.set_yticklabels(names, fontsize=6)
        fig.colorbar(cax, ax=ax, label='Synergy')
        ax.set_title('Card Synergy')
        fig.tight_layout()
        return fig

    def generate_image(self):
        # Get the card images
        card_images = {}
        for card in self.cards:
            if "Basic Land" in card.get('type_line'):
                repeated_cards = 1
            else:
                repeated_cards = card.get('count')
            image_url = card.get("url")
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            mana_cost = card.get("cmc")
            for i in range(repeated_cards):
                if mana_cost not in card_images:
                    card_images[mana_cost] = []
                card_images[mana_cost].append(image)

        # Combine the card images into a single image
        if card_images:
            card_width, card_height = card_images[min(card_images.keys(), default=0)][0].size
            image_width = card_width * len(card_images)
            image_height = card_height * max([len(images) for images in card_images.values()])

            # Combine card images with the same mana cost vertically
            combined_images = []
            for mana_cost in sorted(card_images.keys()):
                images = card_images[mana_cost]
                if len(images) > 1:
                    combined_images.append(self.combine_images(images, "vertical"))
                else:
                    combined_images.append(images[0])

            # Combine all card images horizontally
            combined_image = self.combine_images(combined_images, "horizontal")

            # Save the combined image
            combined_image.save(f"Decks/{self.name}/deck.png")
        else:
            print("Error: No card images found")

        return combined_image

    def combine_images(self, images, orientation, width=None):
        if not images:
            return None

        # Resize images to the same width
        if width:
            for i, image in enumerate(images):
                w, h = image.size
                ratio = width / w
                h = int(h * ratio)
                images[i] = image.resize((width, h))

        # Combine images
        widths, heights = zip(*(i.size for i in images))
        if orientation == "horizontal":
            total_width = sum(widths)
            max_height = max(heights)
            combined_image = Image.new("RGBA", (total_width, max_height))
            x_offset = 0
            for image in images:
                combined_image.paste(image, (x_offset, 0))
                x_offset += image.size[0]
        elif orientation == "vertical":
            total_height = sum(heights)
            max_width = max(widths)
            combined_image = Image.new("RGBA", (max_width, total_height))
            y_offset = 0
            for image in images:
                combined_image.paste(image, (0, y_offset))
                y_offset += image.size[1]
        else:
            raise ValueError(f"Invalid orientation: {orientation}")

        return combined_image

    def load_deck(self):
        #load a .json
        with open(f"Decks/{self.name}/deck_cards.json", "r") as file:
            self.cards = json.load(file)

