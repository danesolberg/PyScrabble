from collections import namedtuple


Coord = namedtuple('Coord', ['y', 'x'])


class Square:
    BOARD_DIMENSIONS = 15

    def __init__(self, coord, tile=None):
        self.tile = tile
        self.text = ' '
        self.multiplier = None
        self.coord = Coord(coord[0], coord[1])
        self.in_bounds = None

        self._set_bounds()

    def __repr__(self):
        if self.tile:
            covered = 'not empty'
            desc = self.tile.get_letter()
        else:
            covered = 'empty'
            desc = self.text
        if self.multiplier:
            mult = self.multiplier
        else:
            mult = 'N/A'
        return '<__main__.Square ' + str(tuple(self.coord)) + ' [' + covered + '] (' + desc + ') {' + mult + '} >'

    def visual_repr(self):
        if self.tile:
            return ' ' + self.tile.get_visual_repr() + ' '
        else:
            if len(self.text) == 3:
                return self.text
            elif len(self.text) == 1:
                return ' ' + self.text + ' '
            else:
                return '###'

    def _set_bounds(self):
        if 0 <= self.coord.x < Square.BOARD_DIMENSIONS and 0 <= self.coord.y < Square.BOARD_DIMENSIONS:
            self.in_bounds = True
        else:
            self.in_bounds = False

    def set_text(self, text):
        self.text = text

    def set_multiplier(self, multiplier):
        if multiplier in ['DLS', 'TLS', 'DWS', 'TWS']:
            self.multiplier = multiplier

    def set_tile(self, tile):
        self.tile = tile

    def transpose_square(self):
        self.coord = Coord(self.coord.x, self.coord.y)

    def get_text(self):
        return self.text

    def get_multiplier(self):
        return self.multiplier

    def get_tile(self):
        return self.tile

    def get_coord(self):
        return self.coord

    def is_in_bounds(self):
        return self.in_bounds

    def is_empty(self):
        if self.tile:
            return False
        return True

    def __eq__(self, other):
        return isinstance(other, Square) and self.coord == other.coord

    def __hash__(self):
        return id(self)
