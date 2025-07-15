import os
import shutil
import unittest
from unittest.mock import patch

from MTGDeck import MagicDeck


# Simple fake data to avoid network requests
CARD_FIXTURES = {
    "test card": {
        "name": "Test Card",
        "printed_name": "Test Card",
        "oracle_text": "Some oracle text",
        "printed_text": "Some printed text",
        "image_uris": {"normal": "http://example.com/test.png"},
        "mana_cost": "{1}{B}",
        "cmc": 2.0,
        "type_line": "Creature — Test",
        "power": "2",
        "toughness": "2",
        "keywords": [],
        "prices": {"eur": "0.10", "usd": "0.20"},
    },
    "swamp": {
        "name": "Swamp",
        "printed_name": "Swamp",
        "oracle_text": "",
        "printed_text": "",
        "image_uris": {"normal": "http://example.com/swamp.png"},
        "mana_cost": "",
        "cmc": 0.0,
        "type_line": "Basic Land — Swamp",
        "power": None,
        "toughness": None,
        "keywords": [],
        "prices": {"eur": "0.00", "usd": "0.00"},
    },
}


def fake_get_api_data(self, card_name):
    return CARD_FIXTURES[card_name.lower()]


class TestMagicDeck(unittest.TestCase):
    def setUp(self):
        self.deck_name = "unit_test"
        self.deck_path = os.path.join("Decks", self.deck_name)
        os.makedirs(os.path.join(self.deck_path, "card_images"), exist_ok=True)
        self.deck = MagicDeck(self.deck_name)

    def tearDown(self):
        shutil.rmtree(self.deck_path, ignore_errors=True)

    @patch.object(MagicDeck, "get_api_data", fake_get_api_data)
    def test_add_card(self):
        self.deck.add_card("Test Card", 2, save_card_image=False)
        self.assertEqual(len(self.deck.cards), 1)
        self.assertEqual(self.deck.cards[0]["name"], "Test Card")
        self.assertEqual(self.deck.cards[0]["count"], 2)

    @patch.object(MagicDeck, "get_api_data", fake_get_api_data)
    @patch("builtins.print")
    def test_remove_card(self, mock_print, mock_get):
        self.deck.add_card("Test Card", 2, save_card_image=False)
        self.deck.remove_card("Test Card", 1)
        self.assertEqual(self.deck.cards[0]["count"], 1)
        # Removing the last copy should remove the card entirely
        self.deck.remove_card("Test Card", 1)
        self.assertEqual(len(self.deck.cards), 0)

    @patch("builtins.print")
    @patch.object(MagicDeck, "get_api_data", fake_get_api_data)
    def test_generate_image_no_files(self, mock_get, mock_print):
        self.deck.add_card("Test Card", 1, save_card_image=False)
        result = self.deck.generate_image()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

