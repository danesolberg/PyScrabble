from operator import attrgetter

from pyscrabble.client.tty_printer import TtyPrinter


class DebugInterface(TtyPrinter):
    def __init__(self, stdscr, game):
        super().__init__(stdscr)

        self.game = game

    def render_header(self):
        self.stdscr.addstr('TURN %s: %s \n' % (self.game.turn, self.game.current_player.get_name()))
        self.stdscr.addstr('-----\n')
        self.stdscr.addstr(
            "%s's Rack: %s \n" % (self.game.current_player.get_name(), ", ".join(self.game.current_player.rack.get_rack_str())))
        self.stdscr.addstr('Tiles Remaining: %s \n' % len(self.game.bag))
        for player in sorted(self.game.players, key=attrgetter('name')):
            self.stdscr.addstr('%s score: %s \n' % (player.get_name(), player.get_score()))
        self.stdscr.addstr('\n')
        self.stdscr.refresh()

    def render_move(self, play):
        self.stdscr.addstr('Played Word: %s \n' % play.get_word_str())
        self.stdscr.addstr('Move score: %s \n' % play.get_score())
        loc, direction = play.get_location(), play.get_direction()
        self.stdscr.addstr(f'Location: ({loc[0], loc[1]})' + 'right' if direction == 'r' else 'down' + '\n')
