from collections import namedtuple


class Square:
    Coord = namedtuple('Coord', ['y','x'])

    def __init__(self,coord):
        self.tile = None
        self.text = ' '
        self.multiplier = None
        self.coord = Square.Coord(coord[0],coord[1])
        self.in_bounds = None

        self.set_bounds()

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

    def set_bounds(self):
        if 0 <= self.coord.x <= 14 and 0 <= self.coord.y <= 14:
            self.in_bounds = True
        else:
            self.in_bounds = False

    def set_text(self, text):
        self.text = text

    def set_multiplier(self, multiplier):
        if multiplier in ['DLS','TLS','DWS','TWS']:
            self.multiplier = multiplier

    def set_tile(self, tile):
        self.tile = tile

    def transpose_square(self):
        self.coord = Square.Coord(self.coord.x, self.coord.y)

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
        else:
            return True