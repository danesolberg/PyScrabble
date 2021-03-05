class Tile:
    TILE_SCORES = {
        'A': 1,
        'B': 3,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 4,
        'G': 2,
        'H': 4,
        'I': 1,
        'J': 8,
        'K': 5,
        'L': 1,
        'M': 3,
        'N': 1,
        'O': 1,
        'P': 3,
        'Q': 10,
        'R': 1,
        'S': 1,
        'T': 1,
        'U': 1,
        'V': 4,
        'W': 4,
        'X': 8,
        'Y': 4,
        'Z': 10,
        '_': 0
    }

    BLANK_SYMBOL = "_"

    def __init__(self, letter):
        self.letter = None
        self.score = None
        self.is_blank = None
        self.last_played = False

        self._set_letter(letter)
        self._set_score(letter)
        self._set_is_blank(letter)

    def __repr__(self):
        return '<__main__.Tile ' + self.letter + ' >'

    def _set_is_blank(self, letter):
        if letter == self.BLANK_SYMBOL:
            self.is_blank = True
        else:
            self.is_blank = False

    def _set_letter(self, letter):
        if letter == self.BLANK_SYMBOL:
            self.letter = self.BLANK_SYMBOL
        elif isinstance(letter, str) and letter.isalpha():
            self.letter = letter.upper()
        else:
            raise ValueError("Letter must be an alphabet character.")

    def _set_score(self, letter):
        self.score = Tile.TILE_SCORES[letter.upper()]

    def get_score(self):
        return self.score

    def get_is_blank(self):
        return self.is_blank

    def get_letter(self):
        return self.letter

    def set_blank_letter(self, letter):
        if not self.is_blank:
            raise ValueError("Tile is not blank.")
        elif isinstance(letter, str) and letter.isalpha():
            self.letter = letter.upper()
        else:
            raise ValueError("Letter must be an alphabet character.")

    def reset_last_played(self):
        self.last_played = False

    def set_last_played(self):
        self.last_played = True

    def get_visual_repr(self):
        vis = self.letter

        if self.last_played is True:
            dec_code = ord(vis) + 119743
            hex_code = hex(dec_code)

            vis = 'U000' + str(hex_code)[2:]
            vis = '\\' + vis
            vis = bytes(vis, 'ascii').decode('unicode-escape')

        if self.is_blank and self.letter is not self.BLANK_SYMBOL:
            vis = vis + '\u0332'

        return vis
