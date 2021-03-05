from ..configs import sio, tty_printer


@sio.on('update header')
def update_header(data):
    turn_num = data['turn_number']
    cur_player = data['current_player']
    scores = data['scores']
    rem_tiles = data['remaining_tiles']

    tty_printer.render_str(2, 0, f"Turn {turn_num}: {cur_player}")
    tty_printer.render_str(3, 0, "Scores:")
    i = 3
    for player, score in scores.items():
        i += 1
        tty_printer.render_str(i, 2, f"{player}: {score}")
    tty_printer.render_str(i+1, 0, f"Remaining tiles: {rem_tiles}")
