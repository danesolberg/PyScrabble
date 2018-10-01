class Tile:
    def __init__(self, letter, score):
        self.letter = letter.upper()
        self.score = score
        self.is_blank = self.set_is_blank()
        self.blank_letter = None
        self.last_played = False

    def __repr__(self):
        return '<__main__.Tile ' + self.letter + ' >'

    def set_is_blank(self):
        if self.letter == '_':
            return True
        else:
            return False

    def get_score(self):
        return self.score

    def get_is_blank(self):
        return self.is_blank

    def set_blank_letter(self, letter):
        self.blank_letter = letter.upper()

    def get_letter(self):
        if self.is_blank and self.blank_letter != None:
            return self.blank_letter
        else:
            return self.letter

    def reset_last_played(self):
        self.last_played = False

    def set_last_played(self):
        self.last_played = True

    def get_visual_repr(self):
        if self.is_blank and self.blank_letter != None:
            vis = self.blank_letter
        else:
            vis = self.letter

        if self.last_played is True:
            dec_code = ord(vis) + 119743
            hex_code = hex(dec_code)

            vis = 'U000' + str(hex_code)[2:]
            vis = '\\' + vis
            vis = bytes(vis, 'ascii').decode('unicode-escape')

        if self.is_blank and self.blank_letter != None:
            # vis = '\033[4m' + self.blank_letter
            vis = vis + '\u0332'

        return vis