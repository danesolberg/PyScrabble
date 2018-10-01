from collections import Counter

class Rack:
    FULL_RACK_TILE_COUNT = 7

    def __init__(self, bag):
        self.rack = []
        self.bag = bag
        self.initialize_rack()

    def add_tile_to_rack(self):
        self.rack.append(self.bag.take_tile_from_bag())
        return self

    def initialize_rack(self):
        for _ in range(Rack.FULL_RACK_TILE_COUNT):
            self.add_tile_to_rack()

    def remove_tile_from_rack(self, tile):
        self.rack.remove(tile)
        return self

    def remove_letter_from_rack(self, letter):
        for tile in self.rack:
            if letter == tile.get_letter():
                self.rack.remove(tile)
                return self
        for tile in self.rack:
            if tile.get_is_blank():
                self.rack.remove(tile)
                return self
        raise ValueError('Letter not in rack')

    def get_rack_tile_count(self):
        return len(self.rack)

    def refill_tiles_in_rack(self):
        while self.get_rack_tile_count() < 7 and self.bag.get_bag_tile_count() > 0:
            self.add_tile_to_rack()

    def get_rack_str(self):
        return ', '.join(str(tile.get_letter()) for tile in self.rack)

    def get_rack_arr(self):
        return self.rack

    def unmet_letter_requirement(self, req_letters):
        req = Counter(req_letters)
        has = Counter(list(self.get_rack_str()))
        missing = []
        for letter, cnt in req.items():
            met = has.get(letter, 0)
            while met < cnt and has.get('_', 0) > 0:
                met += 1
                has['_'] -= 1

            if met < cnt:
                missing.extend([letter] * (cnt - met))
        return missing