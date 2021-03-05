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
            cls.played_words.append(word)
            cls.game.place_move(word)

    def test_word_scores(self):
        for i, mock_turn in enumerate(GAME_MOCK_TURNS):
            assert mock_turn.score == self.played_words[i].score

    def test_secondary_words(self):
        for i, mock_turn in enumerate(GAME_MOCK_TURNS):
            assert set(mock_turn.secondary_words) == \
                   set("".join(tile.get_letter() for _, tile in swp) for swp in
                       self.played_words[i].secondary_word_placements)

    def test_word_squares(self):
        for i, mock_turn in enumerate(GAME_MOCK_TURNS):
            for j, placement in enumerate(mock_turn.word_placement):
                square, _ = placement
                assert square == self.played_words[i].squares[j]

    def test_word_placement(self):
        for i, mock_turn in enumerate(GAME_MOCK_TURNS):
            for j, placement in enumerate(mock_turn.word_placement):
                square, tile = placement
                square.set_tile(tile)
                assert square, tile == self.played_words[i].word_placement[j]

    def test_required_letters(self):
        for i, mock_turn in enumerate(GAME_MOCK_TURNS):
            required_letters = []
            for square, tile in mock_turn.word_placement:
                if not square.get_tile():
                    required_letters.append(tile.get_letter())
            assert required_letters == self.played_words[i].get_required_letters()
