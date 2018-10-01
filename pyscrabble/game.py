from collections import namedtuple
from operator import itemgetter, attrgetter
import sys
import logging
import curses
import os
import time
from .board import Board
from .bag import Bag
from .move_generator import MoveGenerator
from .player import Player
from .word import Word
from .exceptions import (NoPossibleMovesException, TurnSkippedException,
    MissingRequiredLetterError, DictionaryError, MoveError, PlacementError)


class Game:
    DICTIONARY = 'dictionary.txt'
    Player_Moves = namedtuple('Player_Moves', ['move_set','best_move'])

    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.players = []
        self.number_players = 0
        self.turn = 0
        self.skips = 0
        self.current_player = None
        self.all_computer = None
        self.move_generator = MoveGenerator(self, self.DICTIONARY)

    def init_screen(self, stdscr):
        stdscr.scrollok(True)
        curses.echo()
        stdscr.keypad(True)

        height, width = stdscr.getmaxyx() 
        while height < 50 or width < 90:
            height, width = stdscr.getmaxyx()
            stdscr.addnstr(f"Terminal must be at least 50 lines and 90 columns.\n", width)
            stdscr.getch()
        self.stdscr = stdscr

    def add_player(self, name, is_computer):
        self.players.append(Player(name, is_computer, self.bag))

    def get_bag(self):
        return self.bag

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def get_next_player(self):
        '''
        Get the next player who has control of the board.

        @return: Next Player who has control of the board.
        '''

        if (len(self.players) == 0):
            return None

        self.current_player = self.players.pop(0)
        self.players.append(self.current_player)
        return self.current_player

    def skip_turn(self):
        self.skips += 1
        self.board.reset_last_play_cue()
        raise TurnSkippedException

    def get_player_moves(self):
        move_set = self.move_generator.generate_moves(self.current_player.get_rack().get_rack_arr())

        if len(move_set) > 0:
            best_move = max(move_set, key=itemgetter(3))
            return self.Player_Moves(move_set, best_move)
        else:
            raise NoPossibleMovesException

    def place_move(self, play):
        player_moves = self.get_player_moves()
        moves_gen = ((w,p,sq) for w,p,sq,sc in player_moves.move_set)
        if (play.get_word_str(), play.get_squares()[0], play.get_direction()) in moves_gen:
            self.current_player.increase_player_score(play.get_score())
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

            if not self.move_generator.gdg.__contains__(play.word):
                raise DictionaryError()

            raise MoveError()


    def input_player_word(self):
        self.render_header()
        self.stdscr.addstr(11, 0, self.board.visual_repr().encode('utf-8'))
        try:
            self.get_player_moves()
        except NoPossibleMovesException:
            while True:
                self.stdscr.addstr(46, 0, 'You have no possible moves! Skip turn? (y)')
                self.stdscr.clrtobot()
                resp = self.stdscr.getkey()
                if resp == 'y':
                    self.stdscr.addstr('\n')
                    return self.skip_turn()
                else:
                    continue

        while True:
            try:
                while True:
                    self.stdscr.addstr(46, 0, 'Direction to place word: (d/r): ')
                    self.stdscr.clrtobot()
                    direction = self.stdscr.getkey()
                    if direction in ['d','r']:
                        self.stdscr.addstr('\n')
                        break
                    else:
                        continue

                while True:
                    self.stdscr.addstr(46, 0, 'Coordinate to place word (row,column): ')
                    self.stdscr.clrtobot()
                    location = self.stdscr.getstr().decode(encoding="utf-8")
                    try:
                        location = tuple(map(int,location.split(',')))
                        break
                    except:
                        continue

                placement_square = self.board.get_square(location)

                try:
                    self.move_generator.find_anchor(placement_square, direction)
                except PlacementError as e:
                    raise e

                self.stdscr.addstr(47, 0, 'Enter word to play: ')
                self.stdscr.clrtobot()
                word = self.stdscr.getstr().decode(encoding="utf-8").upper()

                try:
                    play = Word(self, word, location, direction)
                    self.place_move(play)
                except Exception as e:
                    raise e

                break
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    self.stdscr.addstr(46, 0, 'Exiting game...')
                    self.stdscr.clrtobot()
                    self.stdscr.refresh()
                    curses.endwin()
                    sys.exit()
                else:
                    self.stdscr.addstr(46, 0, str(e))
                    self.stdscr.clrtobot()
                    self.stdscr.refresh()
                    time.sleep(1.5)
                    continue
        self.stdscr.erase()
        self.render_header()
        self.render_move(play)
        self.stdscr.addstr(11, 0, self.board.visual_repr().encode('utf-8'))
        self.stdscr.refresh()
        time.sleep(2)
        return play

    def input_computer_word(self):
        self.render_header()
        try:
            player_moves = self.get_player_moves()
        except NoPossibleMovesException:
            return self.skip_turn()

        #  For future non-greedy strategy
        # move_set = player_moves.move_set
        best_move = player_moves.best_move

        word = best_move[0]
        location = best_move[1].get_coord()
        direction = best_move[2]

        play = Word(self, word, location, direction)
        self.place_move(play)
        self.render_move(play)
        self.stdscr.addstr(11, 0, self.board.visual_repr().encode('utf-8'))
        self.stdscr.refresh()
        return play

    def setup_game(self):
        computer_count = 0
        try:
            while True:
                self.stdscr.addstr('Number of players (max 4): ')
                num_players = self.stdscr.getch() - ord('0')
                if 1 < num_players <= 4:
                    self.number_players = num_players
                    self.stdscr.addstr('\n')
                    break
                else:
                    self.stdscr.addstr('\n')
                    continue

            for i in range(num_players):
                while True:
                    self.stdscr.addstr(0, 0, 'Is Player %s a computer? (y/n): ' % str(i+1))
                    self.stdscr.clrtobot()
                    player_is_computer = chr(self.stdscr.getch())
                    if player_is_computer in ['y','n']:
                        player_is_computer = True if player_is_computer == 'y' else False
                        self.stdscr.addstr('\n')
                        break
                    else:
                        self.stdscr.addstr('\n')
                        continue

                if player_is_computer == True:
                    computer_count += 1
                    player_name = 'Computer ' + str(computer_count)
                else:
                    self.stdscr.addstr(0, 0, 'Name of Player %s: ' % str(i+1))
                    self.stdscr.clrtobot()
                    player_name = self.stdscr.getstr().decode(encoding="utf-8")
                    while player_name == "":
                        player_name = self.stdscr.getstr().decode(encoding="utf-8")

                self.add_player(player_name, player_is_computer)
        except KeyboardInterrupt:
            self.stdscr.addstr('Exiting game...')
            curses.endwin()
            sys.exit()

        if computer_count == num_players:
            self.all_computer = True
        else:
            self.all_computer = False
        self.stdscr.erase()

    def get_turn(self):
        return self.turn

    def process_turn(self):
        self.turn += 1
        play = None
        try:
            if self.current_player.is_computer():
                play = self.input_computer_word()
            else:
                play = self.input_player_word()
            self.skips = 0
        except TurnSkippedException:
            self.stdscr.addstr('%s has skipped their turn \n' % self.current_player.get_player_name())
        if play:
            logging.info("""Turn {} - {}:\n
                          Primary word: {}\n
                          Secondary words: {}\n\n""".format(self.turn, self.current_player.get_player_name(), play.word, play.get_secondary_words()))
        else:
            logging.info("""Turn {} - {}:\n
                            Skipped""".format(self.turn, self.current_player.get_player_name()))
        self.current_player.rack.refill_tiles_in_rack()
        self.stdscr.refresh()
        return play

    def render_header(self):
        self.stdscr.addstr('TURN %s: %s \n' % (self.turn, self.current_player.get_player_name()))
        self.stdscr.addstr('-----\n')
        self.stdscr.addstr("%s's Rack: %s \n" % (self.current_player.get_player_name(), self.current_player.rack.get_rack_str()))
        self.stdscr.addstr('Tiles Remaining: %s \n' % self.bag.get_bag_tile_count())
        for player in sorted(self.players, key=attrgetter('name')):
            self.stdscr.addstr('%s score: %s \n' % (player.get_player_name(), player.get_player_score()))
        self.stdscr.addstr('\n')
        self.stdscr.refresh()

    def render_move(self, play):
        self.stdscr.addstr('Computer Word: %s \n' % play.get_word_str())
        self.stdscr.addstr('Move score: %s \n' % play.get_score())
        self.stdscr.addstr('Location: (%s, %s) %s \n' % (*play.get_location(), 'right\n' if play.get_direction() == 'r' else 'down\n'))

    def play_game(self, stdscr):
        self.init_screen(stdscr)
        self.setup_game()
        END = False
        while self.skips < self.number_players:
            self.get_next_player()
            self.process_turn()

            while self.current_player.is_computer() or self.all_computer:
                self.stdscr.addstr(46, 0, '\nPress (n) for next turn or (q) for quit.')
                self.stdscr.clrtobot()
                c = self.stdscr.getkey()
                if c == 'n':
                    break
                elif c == 'q':
                    curses.endwin()
                    END = True
                    break
                else:
                    continue
            
            if END:
                break

            if self.skips < self.number_players:
                self.stdscr.erase()
        curses.endwin()
        print('GAME END')