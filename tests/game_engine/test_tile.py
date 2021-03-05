import unittest
import string

from pyscrabble.game_engine.tile import Tile


class TestTile(unittest.TestCase):
    def test_is_blank(self):
        letter = Tile.BLANK_SYMBOL
        tile = Tile(letter)
        assert tile.get_is_blank() is True and tile.get_letter() is Tile.BLANK_SYMBOL

    def test_is_not_blank(self):
        letter = "A"
        tile = Tile(letter)
        assert tile.get_is_blank() is False

    def test_score(self):
        for letter in string.ascii_uppercase:
            tile = Tile(letter)
            assert tile.get_score() == Tile.TILE_SCORES[letter]

    def test_get_letter(self):
        tile = Tile(Tile.BLANK_SYMBOL)
        assert tile.get_letter() is Tile.BLANK_SYMBOL
        tile._set_letter("z")
        assert tile.get_letter() == "Z"
        tile = Tile("a")
        assert tile.get_letter() == "A"

    def test_set_number(self):
        try:
            Tile("0")
        except ValueError:
            return True
        return False



