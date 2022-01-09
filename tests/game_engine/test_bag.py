import unittest

from pyscrabble.game_engine.bag import Bag
from pyscrabble.game_engine.tile import Tile

TILE_COUNT = 100
TILE_FACE_VALUE = 187


class TestBag(unittest.TestCase):
    def test_size(self):
        assert sum(c for _, c in Bag.BAG_TILE_COUNTS.items()) == len(Bag()) == TILE_COUNT

    def test_face_value(self):
        assert sum(Tile.TILE_SCORES[l.upper()] * c for l, c in Bag.BAG_TILE_COUNTS.items()) == \
               sum(tile.score for tile in Bag()) == TILE_FACE_VALUE

    def test_initialization(self):
        bag1 = Bag()
        bag2 = Bag()
        bag2.bag = []
        bag2._initialize_bag()

        assert len(bag1) == len(bag2)

    def test_tile_addition(self):
        bag = Bag()
        bag.add_tile_to_bag(Tile("A"))
        assert len(bag) == TILE_COUNT + 1

    def test_tile_removal(self):
        bag = Bag()
        removals = 25
        for _ in range(removals):
            bag.take_tile_from_bag()
        assert len(bag) == TILE_COUNT - removals

    def test_empty(self):
        bag = Bag()
        for _ in range(TILE_COUNT):
            bag.take_tile_from_bag()
        assert len(bag) == 0

    def test_shuffle(self):
        # rare chance of this failing due to nature of random shuffling
        assert hash("".join(tile.letter for tile in Bag())) != hash("".join(tile.letter if tile.letter else tile.BLANK_SYMBOL for tile in Bag()))
