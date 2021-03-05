from collections import Counter

from pyscrabble.game_engine.tile import Tile


class Rack:
    FULL_RACK_TILE_COUNT = 7

    def __init__(self, bag):
        self.rack = []
        self.bag = bag
        self.initialize_rack()

    def initialize_rack(self):
        for _ in range(Rack.FULL_RACK_TILE_COUNT):
            self.add_tile_to_rack()

    def add_tile_to_rack(self):
        self.rack.append(self.bag.take_tile_from_bag())
        return self

    def remove_tile_from_rack(self, tile):
        self.rack.remove(tile)
        return tile

    def remove_letter_from_rack(self, letter):
        if not isinstance(letter, str):
            raise ValueError("Letter must be a string.")
        blanks = []
        for tile in self.rack:
            if tile.get_is_blank():
                blanks.append(tile)
            elif letter == tile.get_letter():
                self.rack.remove(tile)
                return tile
        for tile in blanks:
            self.rack.remove(tile)
            return tile

        raise ValueError('Letter not in rack')

    def refill_tiles_in_rack(self):
        while len(self.rack) < 7 and len(self.bag) > 0:
            self.add_tile_to_rack()

    def get_rack_str(self):
        return ''.join(tile.get_letter() for tile in self.rack)

    def get_rack_arr(self):
        return self.rack

    def unmet_letter_requirement(self, req_letters):
        req = Counter(req_letters)
        has = Counter(list(self.get_rack_str()))
        missing = []
        for letter, cnt in req.items():
            met = has.get(letter, 0)
            while met < cnt and has.get(Tile.BLANK_SYMBOL, 0) > 0:
                met += 1
                has[Tile.BLANK_SYMBOL] -= 1

            if met < cnt:
                missing.extend([letter] * (cnt - met))
        return missing

    def __len__(self):
        return len(self.rack)

    def __getitem__(self, item):
        return self.rack[item]

    def __iter__(self):
        return iter(self.rack)

    def __contains__(self, item):
        return item in self.rack
