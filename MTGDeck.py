import json
import os
import requests
from PIL import Image
from io import BytesIO

class MagicDeck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.card_images_PATH = f"Decks/{self.name}/card_images/"

        # Create the directory if it does not exist
        if not os.path.exists(f"Decks/{self.name}"):
            os.makedirs(f"Decks/{self.name}")

        else:
            print('{} already exists.'.format(f"Decks/{self.name}"))
            input('Do you want to remove the existing one? (y/n)')
            if input == 'y':
                #remove Decks/{self.name}
                os.removedirs(f"Decks/{self.name}")
                os.makedirs(f"Decks/{self.name}")
            else:
                self.load_deck()


    def add_card(self, card_name, num, save_card_image=True):

        response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}")
        if response.status_code != 200:
            print(f"Error: Card '{card_name}' not found")
            return
        
        data = json.loads(response.content)
        print('Adding {}...'.format(data.get("printed_name")))
        #load the desired data in a json
        card_data = {
                "url": data['image_uris']['large'],
                "name": data.get("printed_name"),
                "mana_cost": data.get("mana_cost"),
                "cmc": data.get("cmc"),
                "type_line": data.get("type_line"),
                "power": data.get("power"),
                "toughness": data.get("toughness"),
                "keywords": data.get("keywords"),
                "printed_text": data.get("printed_text"),
                "count": num
            }
        
        #check if the card data is allready on the self.cards:
        for card in self.cards:
            if card.get('name') == card_data.get('name'):
                card['count'] += card_data.get('count')
                return
    
        self.cards.append(card_data)

        #save the image:
        if save_card_image == True:
            large_image_url = data['image_uris']['large']

            # Download the image and save it to a file
            response = requests.get(large_image_url)
            if response.status_code != 200:
                print(f"Error: Failed to download image for card '{card_name}'")
                return
            
            image = Image.open(BytesIO(response.content))
            os.makedirs(self.card_images_PATH, exist_ok=True)
            
            image.save(f"{self.card_images_PATH}{card_name}.png")
            #print(f"Image saved as '{self.card_images_PATH}{card_name}.png'")


    def save_deck(self):
        with open(f"Decks/{self.name}/deck_cards.json", "w") as file:
            json.dump(self.cards, file, indent=4)
            

    def generate_image(self):
        # Get the card images
        card_images = {}
        for card in self.cards:
            if "Basic Land" in card.get('type_line'):
                repeated_cards = 1
            else:
                repeated_cards = card.get('count')
            for i in range(repeated_cards):
                image_url = card.get("url")
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

    def remove_card(self, card_name):
        for card in self.cards:
            if card.get("name") == card_name:
                print('Removing {}...'.format(card.get("name")))
                if card.get("count") > 1:
                    card["count"] -= 1
                else:
                    self.cards.remove(card)
                return


    def load_deck(self):
        #load a .json
        with open(f"Decks/{self.name}/deck_cards.json", "r") as file:
            self.cards = json.load(file)


# deck = MagicDeck("Test")

# # Add some cards to the deck
# deck.add_card("nim toxico", 1)
# deck.add_card("cieno depredador", 2)
# deck.add_card("bosque", 4)
# deck.remove_card('Nim tóxico')


# deck.generate_image()

# deck.save_deck()