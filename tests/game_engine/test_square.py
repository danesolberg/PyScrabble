import unittest

from pyscrabble.game_engine.square import Square, Coord
from pyscrabble.game_engine.tile import Tile


class TestSquare(unittest.TestCase):
    def test_in_bounds(self):
        test_cases = [
            [(0, 0), True], [(-1, 0), False], [(-1, -1), False], [(-1, 1), False], [(0, -1), False], [(-999, 0), False],
            [(0, -999), False], [(5, 5), True], [(3, 12), True],
            [(Square.BOARD_DIMENSIONS, Square.BOARD_DIMENSIONS), False],
            [(Square.BOARD_DIMENSIONS + 1, Square.BOARD_DIMENSIONS + 1), False],
            [(Square.BOARD_DIMENSIONS, Square.BOARD_DIMENSIONS + 1), False],
            [(Square.BOARD_DIMENSIONS + 1, Square.BOARD_DIMENSIONS), False],
            [(Square.BOARD_DIMENSIONS - 1, Square.BOARD_DIMENSIONS - 1), True],
            [(Square.BOARD_DIMENSIONS, Square.BOARD_DIMENSIONS - 1), False],
            [(Square.BOARD_DIMENSIONS - 1, Square.BOARD_DIMENSIONS), False],
        ]

        assert all(Square(case[0]).in_bounds is case[1] for case in test_cases)

    def test_transpose(self):
        square = Square((3, 10))
        square.transpose_square()
        assert square.coord == Coord(10, 3)

    def test_is_empty(self):
        square = Square((3, 10))
        assert square.is_empty()

        square.set_tile(Tile("A"))
        assert not square.is_empty()
