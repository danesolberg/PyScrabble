from collections import namedtuple, deque
from operator import itemgetter

from . import gdg
from .board import Board
from .bag import Bag
from .move_generator import MoveGenerator
from .player import Player
from .word import Word
from .exceptions import (NoPossibleMovesException, TurnSkippedException,
                         MissingRequiredLetterError, DictionaryError, MoveError, PlacementError,
                         NonUniquePlayerNameException)


Player_Moves = namedtuple('Player_Moves', ['move_set', 'best_move'])


class Game:
    OUT_OF_TILES_ENDING, OUT_OF_MOVES_ENDING = 1, 0

    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.players = deque()
        self.number_players = 0
        self.turn = 0
        self.skips = 0
        self.current_player = None
        self.all_computer = None
        self.end_state = None
        self.move_generator = MoveGenerator(self)

    def add_player(self, name, is_computer):
        self.number_players += 1
        if any(player for player in self.players if player.get_name() == name):
            raise NonUniquePlayerNameException()
        self.players.append(Player(name, is_computer, self.bag))

    def get_bag(self):
        return self.bag

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def get_next_player(self):
        if len(self.players) == 0:
            return None

        self.current_player = self.players.popleft()
        self.players.append(self.current_player)
        return self.current_player

    def get_player(self, name):
        return next(player for player in self.players if player.get_name() == name)

    def get_all_players(self):
        return self.players

    def skip_turn(self):
        self.skips += 1
        self.board.reset_last_play_cue()
        raise TurnSkippedException

    def get_player_moves(self, specific_square=None):
        move_set = self.move_generator.generate_moves(self.current_player.get_rack().get_rack_arr(), specific_square)

        if len(move_set) > 0:
            best_move = max(move_set, key=itemgetter(3))
            return Player_Moves(move_set, best_move)
        else:
            raise NoPossibleMovesException

    def place_move(self, play):
        player_moves = self.get_player_moves(self.move_generator.find_anchor(play.squares[0], play.direction))
        moves_gen = ((w, p, sq) for w, p, sq, sc in player_moves.move_set)
        if (play.get_word_str(), play.get_squares()[0], play.get_direction()) in moves_gen:
            self.current_player.increase_score(play.get_score())
            self.board.place_tiles_on_board(play)

            for letter in play.get_required_letters():
                self.current_player.rack.remove_letter_from_rack(letter)
        else:
            missing_letters = self.current_player.rack.unmet_letter_requirement(play.get_required_letters())
            if missing_letters:
                raise MissingRequiredLetterError(missing_letters)

            try:
                placement_square = self.board.get_square(play.get_location())
                self.move_generator.find_anchor(placement_square, play.get_direction())
            except PlacementError as e:
                raise e

            if play.word not in gdg:
                raise DictionaryError()

            raise MoveError()

    def gen_computer_word(self):
        try:
            player_moves = self.get_player_moves()
        except NoPossibleMovesException:
            return self.skip_turn()

        # For future non-greedy strategy
        # move_set = player_moves.move_set
        best_move = player_moves.best_move

        word = best_move[0]
        location = best_move[1].get_coord()
        direction = best_move[2]

        play = Word(self, word, location, direction)
        return play

    def get_turn(self):
        return self.turn

    def is_end_state(self):
        if self.skips > self.number_players:
            self.end_state = self.OUT_OF_MOVES_ENDING
            return True
        elif len(self.bag) == 0 and self.current_player and len(self.current_player.rack) == 0:
            self.end_state = self.OUT_OF_TILES_ENDING
            return True
        return False

    def setup_game(self):
        raise NotImplemented()

    def query_player_word(self):
        raise NotImplemented()

    def process_turn(self):
        raise NotImplemented()

    def play_game(self):
        self.run_game()

    def run_game(self):
        raise NotImplemented()


