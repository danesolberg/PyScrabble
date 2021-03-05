import unittest

from pyscrabble.game_engine.game import Game
from pyscrabble.game_engine.word import Word
from tests.game_engine.testdata import GAME_MOCK_TURNS


class TestCase(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.game = Game()
        cls.game.add_player("player1", True)
        cls.game.add_player("player2", True)
        cls.played_words = []

        for mock_turn in GAME_MOCK_TURNS:
            cls.game.get_next_player()
            cls.game.turn += 1

            cls.game.get_current_player().rack.rack = mock_turn.rack[:]
            word = Word(cls.game, mock_turn.primary_word, mock_turn.square, mock_turn.direction)
            # word = cls.game.gen_computer_word()
            cls.played_words.append(word)
            # print(cls.game.get_current_player().get_rack())
            cls.game.place_move(word)
            # print(cls.game.board.visual_repr())

    def test_score_accumulation(self):
        if self.game.players[0].name == "player1":
            player1, player2 = self.game.players[0], self.game.players[1]
        else:
            player1, player2 = self.game.players[1], self.game.players[0]

        assert player1.score == sum(GAME_MOCK_TURNS[i].score for i in range(0, len(GAME_MOCK_TURNS), 2))
        assert player2.score == sum(GAME_MOCK_TURNS[i].score for i in range(1, len(GAME_MOCK_TURNS), 2))

    def test_computer_player(self):
        game = Game()
        game.add_player("player1", True)
        game.add_player("player2", False)
        assert game.players[0].is_computer() is True
        assert game.players[1].is_computer() is False
