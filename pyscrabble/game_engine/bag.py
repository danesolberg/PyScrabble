from random import shuffle
from .tile import Tile


class Bag:
    BAG_TILE_COUNTS = {
        'A': 9,
        'B': 2,
        'C': 2,
        'D': 4,
        'E': 12,
        'F': 2,
        'G': 3,
        'H': 2,
        'I': 9,
        'J': 1,
        'K': 1,
        'L': 4,
        'M': 2,
        'N': 6,
        'O': 8,
        'P': 2,
        'Q': 1,
        'R': 6,
        'S': 4,
        'T': 6,
        'U': 4,
        'V': 2,
        'W': 2,
        'X': 1,
        'Y': 2,
        'Z': 1,
        '_': 2
    }

    def __init__(self):
        self.bag = []
        self._initialize_bag()

    def _initialize_bag(self):
        for letter, cnt in self.BAG_TILE_COUNTS.items():
            for _ in range(cnt):
                self.add_tile_to_bag(Tile(letter))
        shuffle(self.bag)

    def add_tile_to_bag(self, tile):
        self.bag.append(tile)

    def take_tile_from_bag(self):
        return self.bag.pop()

    def __len__(self):
        return len(self.bag)

    def __iter__(self):
        return iter(self.bag)