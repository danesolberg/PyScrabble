import locale
import curses
from pyscrabble.game import Game

game = Game()
curses.wrapper(game.play_game)