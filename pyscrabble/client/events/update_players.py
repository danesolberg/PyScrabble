from ..configs import sio, tty_printer


@sio.on('update players')
def update_players(data):
    tty_printer.render_str(2, 0, 'Players: ' + ", ".join(data['players']))

