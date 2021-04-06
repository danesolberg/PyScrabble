import logging
import curses
import time

from .debug_interface import DebugInterface
from .game import Game
from .word import Word
from .exceptions import (NoPossibleMovesException, TurnSkippedException, PlacementError)


class DebugGame(Game):
    def __init__(self):
        super().__init__()
        self.tty_printer = None

    def query_player_word(self):
        try:
            self.get_player_moves()
        except NoPossibleMovesException:
            while True:
                self.tty_printer.render_str(46, 0, 'You have no possible moves! Skip turn? (y)')
                self.tty_printer.clear_to_bottom()
                resp = self.tty_printer.get_key()
                if resp == 'y':
                    self.tty_printer.render_line()
                    return self.skip_turn()
        while True:
            try:
                while True:
                    self.tty_printer.render_str(46, 0, 'Direction to place word: (d/r): ')
                    direction = self.tty_printer.get_key()
                    if direction in ['d', 'r']:
                        self.tty_printer.render_line()
                        break
                while True:
                    self.tty_printer.render_str(46, 0, 'Coordinate to place word (row,column): ')
                    location = self.tty_printer.get_str()
                    try:
                        location = location.split(',')
                        location = tuple(map(int, [location[0], location[1]]))
                        break
                    except (ValueError, IndexError):
                        pass
                placement_square = self.board.get_square(location)
                try:
                    self.move_generator.find_anchor(placement_square, direction)
                except PlacementError as e:
                    raise e
                self.tty_printer.render_str(47, 0, 'Enter word to play: ')
                word = self.tty_printer.get_str().upper()
                try:
                    play = Word(self, word, location, direction)
                    self.place_move(play)
                except Exception as e:
                    raise e
                break
            except Exception as e:
                self.tty_printer.render_str(46, 0, str(e))
                self.tty_printer.clear_to_bottom()
                self.tty_printer.refresh()
                time.sleep(1.5)
        return play

    def setup_game(self):
        computer_count = 0
        try:
            while True:
                self.tty_printer.render_str(0, 0, 'Number of players (max 4): ')
                num_players = self.tty_printer.get_char() - ord('0')
                if 1 < num_players <= 4:
                    break
            for i in range(num_players):
                while True:
                    self.tty_printer.render_str(0, 0, 'Is Player %s a computer? (y/n): ' % str(i + 1))
                    player_is_computer = self.tty_printer.get_key()
                    if player_is_computer in ['y', 'n']:
                        player_is_computer = player_is_computer == 'y'
                        break
                if player_is_computer is True:
                    computer_count += 1
                    player_name = 'Computer ' + str(computer_count)
                else:
                    self.tty_printer.render_str(0, 0, 'Name of Player %s: ' % str(i + 1))
                    player_name = self.tty_printer.get_str()
                    while player_name == "":
                        player_name = self.tty_printer.get_str()
                self.add_player(player_name, player_is_computer)
        except KeyboardInterrupt:
            self.tty_printer._safe_close(None, None)
        if computer_count == num_players:
            self.all_computer = True
        else:
            self.all_computer = False
        self.tty_printer.erase()

    def process_turn(self):
        self.turn += 1
        play = None
        try:
            if self.current_player.is_computer():
                self.tty_printer.render_header()
                play = self.gen_computer_word()
                self.place_move(play)
                self.tty_printer.render_move(play)
                self.tty_printer.render_str(11, 0, self.board.render_board().encode('utf-8'))
                self.tty_printer.refresh()
            else:
                self.tty_printer.render_header()
                self.tty_printer.render_str(11, 0, self.board.render_board().encode('utf-8'))
                play = self.query_player_word()
                self.tty_printer.erase()
                self.tty_printer.render_header()
                self.tty_printer.render_move(play)
                self.tty_printer.render_str(11, 0, self.board.render_board().encode('utf-8'))
                self.tty_printer.refresh()
                time.sleep(2)
            self.skips = 0
        except TurnSkippedException:
            self.tty_printer.render_str('%s has skipped their turn \n' % self.current_player.get_name())
        if play:
            logging.info("""Turn {} - {}:\n
                          Primary word: {}\n
                          Secondary words: {}\n\n""".format(self.turn, self.current_player.get_name(), play.word,
                                                            play.get_secondary_words()))
        else:
            logging.info("""Turn {} - {}:\n
                            Skipped""".format(self.turn, self.current_player.get_name()))
        self.current_player.rack.refill_tiles_in_rack()
        self.tty_printer.refresh()
        return play

    def play_game(self):
        curses.wrapper(self.run_game)

    def run_game(self, stdscr):
        self.tty_printer = DebugInterface(stdscr, self)
        self.setup_game()
        while not self.is_end_state():
            self.get_next_player()
            self.process_turn()

            while self.current_player.is_computer() or self.all_computer:
                self.tty_printer.render_str(46, 0, '\nPress (n) for next turn or (q) for quit.')
                self.tty_printer.clear_to_bottom()
                c = self.tty_printer.get_key()
                if c == 'n':
                    break
                elif c == 'q':
                    self.tty_printer._safe_close(None, None)

            if self.skips < self.number_players:
                self.tty_printer.erase()

        if self.end_state is self.OUT_OF_TILES_ENDING:
            zero_tile_player = None
            other_players = []
            for player in self.players:
                if len(player.rack) == 0:
                    zero_tile_player = player
                else:
                    other_players.append(player)
            for player in other_players:
                for tile in player.rack:
                    player.score -= tile.score
                    zero_tile_player.score += tile.score

        self.tty_printer.render_header()
        self.tty_printer.refresh()
        time.sleep(5)
        self.tty_printer._safe_close(None, None)