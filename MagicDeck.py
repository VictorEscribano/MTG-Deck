import json
import os
import requests
from PIL import Image
from io import BytesIO

class MagicDeck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.lands = {
            "Plains": 0,
            "Island": 0,
            "Swamp": 0,
            "Mountain": 0,
            "Forest": 0
        }

        # Create the directory if it does not exist
        if not os.path.exists(f"Decks/{self.name}"):
            os.makedirs(f"Decks/{self.name}")

    
    def add_card(self, card_name):
        # Make a request to the Scryfall API to search for the card
        response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}")
        if response.status_code != 200:
            print(f"Error: Card '{card_name}' not found")
            return

        # Parse the JSON response
        card_data = json.loads(response.content)

        # Add the card to the deck
        self.cards.append(card_data)

    def add_lands(self, lands):
        # Update the land counts
        for land_type, count in lands.items():
            if land_type in self.lands:
                self.lands[land_type] += count

    def save_card_data(self):
        # Create a dictionary with the card names and counts
        card_counts = {}
        for card in self.cards:
            name = card.get("name")
            count = card_counts.get(name, 0) + 1
            card_counts[name] = count

        # Create a list of card data dictionaries
        card_data = []
        for card in self.cards:
            data = {
                "id": card.get("id"),
                "name": card.get("name"),
                "mana_cost": card.get("mana_cost"),
                "type_line": card.get("type_line"),
                "oracle_text": card.get("oracle_text"),
                "count": card_counts.get(card.get("name"), 0)
            }
            card_data.append(data)
            self.save_image(card.get("name"))

        # Save the card data to a JSON file
        with open(f"Decks/{self.name}/cards.json", "w") as file:
            json.dump(card_data, file, indent=4)

    def save_land_data(self):
        # Create a dictionary with the land counts
        land_counts = {}
        for land_type, count in self.lands.items():
            land_counts[land_type] = count

        # Save the land counts to a JSON file
        with open(f"Decks/{self.name}/lands.json", "w") as file:
            json.dump(land_counts, file, indent=4)


    def save_image(self, card_name):
        # Find the card in the deck
        card = None
        for c in self.cards:
            if c.get("name") == card_name:
                card = c
                break
        
        if not card:
            print(f"Error: Card '{card_name}' not found in the deck")
            return
        
        # Make a request to the Scryfall API to get the image URL
        image_url = card.get("image_uris", {}).get("normal")
        if not image_url:
            print(f"Error: Image URL not found for card '{card_name}'")
            return
        
        # Download the image and save it to a file
        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"Error: Failed to download image for card '{card_name}'")
            return
        
        image = Image.open(BytesIO(response.content))
        os.makedirs(f"Decks/{self.name}/card_images", exist_ok=True)
        image.save(f"Decks/{self.name}/card_images/{card_name}.png")
        print(f"Image saved as 'Decks/{self.name}/card_images/{card_name}.png'")

    def load_deck(self, name):
        path = 'Decks/'+name+'/cards.json'
        with open(path, 'r') as f:
            cards_deck = json.load(f)
        return cards_deck

    def load_lands(name):
        path = 'Decks/'+name+'/lands.json'
        with open(path, 'r') as f:
            lands_deck = json.load(f)
        return lands_deck

    def get_deck_names():
        deck_names = []
        #get the name of all the folders in Decks/ and append them to deck_names
        for folder in os.listdir("Decks/"):
            if os.path.isdir(os.path.join("Decks/", folder)):
                deck_names.append(folder)
        return deck_names


    def generate_image(self):
        # Get the card images
        card_images = {}
        for card in self.cards:
            image_url = card.get("image_uris", {}).get("normal")
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    mana_cost = card.get("cmc")
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
