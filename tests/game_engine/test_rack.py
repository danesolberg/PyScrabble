import unittest

from pyscrabble.game_engine.bag import Bag
from pyscrabble.game_engine.rack import Rack
from pyscrabble.game_engine.tile import Tile


class TestRack(unittest.TestCase):
    def test_initialize(self):
        assert len(Rack(Bag())) == Rack.FULL_RACK_TILE_COUNT

    def test_remove_tile(self):
        rack = Rack(Bag())
        rack_copy = rack[:]
        tile1 = rack[0]
        tile4 = rack[3]
        tile7 = rack[6]

        rack.remove_tile_from_rack(tile1)
        rack.remove_tile_from_rack(tile4)
        rack.remove_tile_from_rack(tile7)

        assert [tile1] + rack[:2] + [tile4] + rack[2:] + [tile7] == rack_copy

    def test_remove_letter(self):
        rack = Rack(Bag())
        rack_copy = rack[:]

        letter1 = rack[0].letter
        letter2 = rack[3].letter
        letter3 = rack[6].letter

        tile1 = rack.remove_letter_from_rack(letter1)
        tile4 = rack.remove_letter_from_rack(letter2)
        tile7 = rack.remove_letter_from_rack(letter3)

        assert sorted("".join(map(Tile.get_letter, [tile1] + rack[:2] + [tile4] + rack[2:] + [tile7]))) == \
               sorted(map(Tile.get_letter, rack_copy))

    def test_remove_nonexistent_tile(self):
        rack = Rack(Bag())
        for tile in rack.bag:
            if tile not in rack:
                try:
                    rack.remove_tile_from_rack(tile)
                except ValueError:
                    return True
                return False

    def test_refill(self):
        rack = Rack(Bag())
        rack.refill_tiles_in_rack()
        assert len(rack) == 7

        rack.remove_tile_from_rack(rack[3])
        rack.remove_tile_from_rack(rack[3])
        rack.refill_tiles_in_rack()
        assert len(rack) == 7

    def test_rack_str(self):
        rack = Rack(Bag())
        assert rack.get_rack_str() == "".join(tile.letter for tile in rack)

    def test_rack_arr(self):
        rack = Rack(Bag())
        assert rack.get_rack_arr() == rack.rack

