from random import shuffle
from .tile import Tile


class Bag:
    BAG_TILE_PROPERTIES = {
        'A': {'score': 1,'count': 9},
        'B': {'score': 3,'count': 2},
        'C': {'score': 3,'count': 2},
        'D': {'score': 2,'count': 4},
        'E': {'score': 1,'count': 12},
        'F': {'score': 4,'count': 2},
        'G': {'score': 2,'count': 3},
        'H': {'score': 4,'count': 2},
        'I': {'score': 1,'count': 9},
        'J': {'score': 8,'count': 1},
        'K': {'score': 5,'count': 1},
        'L': {'score': 1,'count': 4},
        'M': {'score': 3,'count': 2},
        'N': {'score': 1,'count': 6},
        'O': {'score': 1,'count': 8},
        'P': {'score': 3,'count': 2},
        'Q': {'score': 10,'count': 1},
        'R': {'score': 1,'count': 6},
        'S': {'score': 1,'count': 4},
        'T': {'score': 1,'count': 6},
        'U': {'score': 1,'count': 4},
        'V': {'score': 4,'count': 2},
        'W': {'score': 4,'count': 2},
        'X': {'score': 8,'count': 1},
        'Y': {'score': 4,'count': 2},
        'Z': {'score': 10,'count': 1},
        '_': {'score': 0,'count': 2}
    }

    def __init__(self):
        self.bag = []
        self.initialize_bag()

    def add_tile_to_bag(self, tile):
        self.bag.append(tile)

    def initialize_bag(self):
        for letter in self.BAG_TILE_PROPERTIES.items():
            for _ in range(letter[1]['count']):
                self.add_tile_to_bag(Tile(letter[0],letter[1]['score']))
        shuffle(self.bag)

    def take_tile_from_bag(self):
        return self.bag.pop()

    def get_bag_tile_count(self):
        return len(self.bag)