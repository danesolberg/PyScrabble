from ..configs import sio, tty_printer, user_config
from ..utilities import render_rack


@sio.on('update rack')
def update_rack(rack):
    tty_printer.render_str(51, 0, "%s's Rack: %s" % (user_config['username'], render_rack(rack)))
