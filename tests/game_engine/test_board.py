import unittest

from pyscrabble.game_engine.board import Board, Adjacent_Squares
from pyscrabble.game_engine.exceptions import CoordinateError
from pyscrabble.game_engine.game import Game
from pyscrabble.game_engine.tile import Tile
from pyscrabble.game_engine.word import Word
from tests.game_engine.testdata import BOARD_CASES_ADJACENT_SQUARES, BOARD_CASES_INVALID_SQUARES, GAME_MOCK_TURNS


class TestBoard(unittest.TestCase):
    @staticmethod
    def setup_game():
        game = Game()
        game.add_player("player1", True)
        game.add_player("player2", True)
        game.get_next_player()
        game.turn += 1
        return game

    def test_size(self):
        board = Board()
        assert len(board) == Board.BOARD_DIMENSIONS
        assert all(len(row) == Board.BOARD_DIMENSIONS for row in board)

    def test_premium_squares(self):
        board = Board()
        for multipler, coords in Board.PREMIUM_SQUARES.items():
            for coord in coords:
                assert board[coord[0]][coord[1]].multiplier == multipler

    def test_get_square(self):
        board = Board()
        for i in range(15):
            for j in range(15):
                assert board[i][j] is board.get_square((i, j))

    def test_get_invalid_square(self):
        board = Board()

        for case in BOARD_CASES_INVALID_SQUARES:
            try:
                board.get_square(case)
                return False
            except CoordinateError:
                pass
        return True

    def test_transpose(self):
        board1 = Board()
        board1[2][10].set_tile(Tile("A"))
        board2 = Board()
        board2.board = board1.board[:]

        board2.transpose_board()
        assert board2 != board1

        board2.transpose_board()
        assert board2.board == board1.board

    def test_adjacent_squares(self):
        board = Board()

        for case in BOARD_CASES_ADJACENT_SQUARES:
            assert board.get_adjacent_squares(case.test_case) == \
                   Adjacent_Squares(case.left, case.right, case.above, case.below)

    def test_place_tiles(self):
        game = self.setup_game()
        mock_turn = GAME_MOCK_TURNS[0]
        game.get_current_player().rack.rack = mock_turn.rack[:]
        move = Word(game, mock_turn.primary_word, mock_turn.square, mock_turn.direction)

        for square in move.squares:
            assert game.board.get_square(square.get_coord()).is_empty()

        game.place_move(move)

        for i, letter in enumerate(move.word):
            assert game.board.get_square(move.squares[i].get_coord()).get_tile().get_letter() == letter

    def test_reset_last_played(self):
        game = self.setup_game()
        mock_turn = GAME_MOCK_TURNS[0]
        game.get_current_player().rack.rack = mock_turn.rack[:]
        move = Word(game, mock_turn.primary_word, mock_turn.square, mock_turn.direction)
        game.place_move(move)

        game.board.reset_last_play_cue()

        for row in game.board.board:
            for square in row:
                if square.tile:
                    assert square.tile.last_played is False
