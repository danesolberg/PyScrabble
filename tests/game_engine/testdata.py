from collections import namedtuple

from pyscrabble.game_engine.board import Board
from pyscrabble.game_engine.square import Square
from pyscrabble.game_engine.tile import Tile

AdjacentSquareTestCase = namedtuple("AdjacentSquareTestCase", ["test_case", "above", "below", "left", "right"])
BOARD_CASES_ADJACENT_SQUARES = [
    AdjacentSquareTestCase(Square((5, 5)), Square((5, 4)), Square((5, 6)), Square((4, 5)), Square((6, 5))),
    AdjacentSquareTestCase(Square((0, 0)), Board.OFF_BOARD_SQUARE, Square((0, 1)), Board.OFF_BOARD_SQUARE, Square((1, 0))),
    AdjacentSquareTestCase(Square((14, 14)), Square((14, 13)), Board.OFF_BOARD_SQUARE, Square((13, 14)), Board.OFF_BOARD_SQUARE)
]

BOARD_CASES_INVALID_SQUARES = [
    (-1, 0), (-1, -1), (-1, 1), (0, -1), (-999, 0), (0, -999), (5, 5), (3, 12),
    (Board.BOARD_DIMENSIONS, Board.BOARD_DIMENSIONS), (Board.BOARD_DIMENSIONS + 1, Board.BOARD_DIMENSIONS + 1),
    (Board.BOARD_DIMENSIONS, Board.BOARD_DIMENSIONS + 1), (Board.BOARD_DIMENSIONS + 1, Board.BOARD_DIMENSIONS),
    (Board.BOARD_DIMENSIONS - 1, Board.BOARD_DIMENSIONS - 1),
    (Board.BOARD_DIMENSIONS, Board.BOARD_DIMENSIONS - 1), (Board.BOARD_DIMENSIONS - 1, Board.BOARD_DIMENSIONS)
]

MockTurn = namedtuple("MockTurn", ["rack", "primary_word", "secondary_words", "square", "direction", "score", "word_placement"])
GAME_MOCK_TURNS = [
    MockTurn(  # starting word
        [Tile("B"), Tile("O"), Tile("A"), Tile("T"), Tile("E"), Tile("E"), Tile("E")],
        "BOAT", [],
        (7, 6), "r", 12,
        [(Square((7, 6)), Tile("B")), (Square((7, 7)), Tile("O")), (Square((7, 8)), Tile("A")),
         (Square((7, 9)), Tile("T"))]),
    MockTurn(  # TLS
        [Tile("S"), Tile("T"), Tile("A"), Tile("L"), Tile("E"), Tile("A"), Tile("A")],
        "STALE", [],
        (6, 9), "d", 7,
        [(Square((6, 9)), Tile("S")), (Square((7, 9), Tile("T")), Tile("T")), (Square((8, 9)), Tile("A")),
         (Square((9, 9)), Tile("L")), (Square((10, 9)), Tile("E"))]),
    MockTurn(  # DWS, secondary word, and blank tile
        [Tile("R"), Tile("_"), Tile("I"), Tile("N"), Tile("E"), Tile("E"), Tile("E")],
        "RAIN", ["STALER"],
        (11, 9), "r", 12,
        [(Square((11, 9)), Tile("R")), (Square((11, 10)), Tile("A")), (Square((11, 11)), Tile("I")),
         (Square((11, 12)), Tile("N"))]),
    MockTurn(  # DLS and two secondary words
        [Tile("H"), Tile("A"), Tile("T"), Tile("F"), Tile("G"), Tile("A"), Tile("A")],
        "HAT", ["AB", "TO"],
        (6, 5), "r", 14,
        [(Square((6, 5)), Tile("H")), (Square((6, 6)), Tile("A")), (Square((6, 7)), Tile("T"))]),
    MockTurn(  # that's a bingo
        [Tile("S"), Tile("H"), Tile("U"), Tile("N"), Tile("T"), Tile("I"), Tile("G")],
        "SHUNTING", [],
        (5, 12), "d", 84,
        [(Square((5, 12)), Tile("S")), (Square((6, 12)), Tile("H")), (Square((7, 12)), Tile("U")),
         (Square((8, 12)), Tile("N")), (Square((9, 12)), Tile("T")), (Square((10, 12)), Tile("I")),
         (Square((11, 12), Tile("N")), Tile("N")), (Square((12, 12)), Tile("G"))])
]