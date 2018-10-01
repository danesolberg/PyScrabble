class Word:
    def __init__(self, game, word, location, direction):
        self.game = game
        self.board = game.get_board()
        self.word = word
        self.location = location
        self.direction = direction
        self.current_player = game.get_current_player()
        self.squares = self.set_squares()
        self.required_letters = self.set_required_letters()
        self.word_placement = self.set_word_placement()
        self.secondary_word_placements = self.get_secondary_word_placements()
        self.score = self.calculate_score()

    def get_word_str(self):
        return self.word

    def get_location(self):
        return self.location

    def get_direction(self):
        return self.direction

    def get_length(self):
        return len(self.word)

    def get_score(self):
        return self.score

    def set_squares(self):
        coord = self.location

        squares = []
        square = self.board.get_square(coord)
        squares.append(square)

        for _ in range(self.get_length() - 1):
            if self.direction =='r':
                coord = (coord[0], coord[1] + 1)
                square = self.board.get_square(coord)
                squares.append(square)
            elif self.direction =='d':
                coord = (coord[0] + 1, coord[1])
                square = self.board.get_square(coord)
                squares.append(square)
            else:
                raise ValueError('Incorrect direction entered.')
        return squares

    def get_squares(self):
        return self.squares

    def set_word_placement(self):
        """
            Sets self.word_placement using the following pattern
            [(Square,Tile),(Square,Tile)]
        """
        word_placement = []
        
        for i, square in enumerate(self.squares):
            if square.get_tile():
                word_placement.append((square,square.get_tile()))
            else:
                if self.word[i] not in self.current_player.rack.get_rack_str():
                    for tile in self.current_player.rack.get_rack_arr():
                        if tile.get_is_blank():
                            tile.set_blank_letter(self.word[i])
                            word_placement.append((square,tile))
                            break
                else:
                    for tile in self.current_player.rack.get_rack_arr():
                        if self.word[i] == tile.get_letter():
                            word_placement.append((square,tile))
                            break
        return word_placement

    def set_required_letters(self):
        required_letters = []
        for i, square in enumerate(self.squares):
            if not square.get_tile():
                required_letters.append(self.word[i].upper())
        return required_letters

    def get_word_placement(self):
        return self.word_placement

    def get_required_letters(self):
        return self.required_letters

    def get_secondary_word_placements(self):
        def word_placement(board, square, primary_word_placement, direction):

            if not square.is_empty():
                tile = square.get_tile()
            else:
                tile = [tile for square_, tile in primary_word_placement if square_ == square][0]

            if direction == 'r':
                new_square = board.get_adjacent_square(square).down
            elif direction == 'd':
                new_square = board.get_adjacent_square(square).right

            if not new_square.is_empty() or any(new_square == square for square, tile in primary_word_placement):
                word_arr = word_placement(board, new_square, primary_word_placement, direction)
            else:
                word_arr = []

            word_arr.insert(0, (square, tile))
            return word_arr

        all_secondary_word_placements = []

        for square, _ in self.word_placement:
            if self.direction == 'r':
                #  check up and down tiles
                #  get position of most vertical conjoining square for each square in placed word
                starting_square = square
                while not self.board.get_adjacent_square(starting_square).up.is_empty():
                    starting_square = self.board.get_adjacent_square(starting_square).up
                secondary_word_placement = word_placement(self.board, starting_square, self.word_placement, self.direction)
                all_secondary_word_placements.append(secondary_word_placement)
            elif self.direction =='d':
                #  check left and right tiles
                #  get position of left-most conjoining square for each square in placed word
                starting_square = square
                while not self.board.get_adjacent_square(starting_square).left.is_empty():
                    starting_square = self.board.get_adjacent_square(starting_square).left
                secondary_word_placement = word_placement(self.board, starting_square, self.word_placement, self.direction)
                all_secondary_word_placements.append(secondary_word_placement)
        #  secondary words must be atleast 2 tiles long
        all_secondary_word_placements = [word for word in all_secondary_word_placements
                                         if len([square for square, tile in word]) > 1
                                         and any([tile for square, tile in word if square.is_empty()])]

        return all_secondary_word_placements

    def get_secondary_words(self):
        word_arr = [''.join([tile.get_letter() for square, tile in placement]) for placement in self.secondary_word_placements]
        return word_arr

    def calculate_score(self):
        def score_word(word_placement):
            word_multipliers = []
            word_score = 0
            for square, tile in word_placement:
                tile_score = tile.get_score()

                if square.is_empty():
                    multiplier = square.get_multiplier()

                    if multiplier in ['TWS','DWS']:
                        word_multipliers.append(multiplier)
                    elif multiplier == 'TLS':
                        tile_score *= 3
                    elif multiplier == 'DLS':
                        tile_score *= 2
                word_score += tile_score
            for multiplier in word_multipliers:
                if multiplier == 'TWS':
                    word_score *= 3
                elif multiplier == 'DWS':
                    word_score *= 2
            return word_score

        def calculate_primary(self):
            primary_score = score_word(self.word_placement)
            if len(self.required_letters) == 7:
                primary_score += 50
            return primary_score

        def calculate_secondary(self):
            secondary_score = 0
            secondary_word_placements = self.get_secondary_word_placements()
            for word_placement in secondary_word_placements:
                word_score = score_word(word_placement)
                secondary_score += word_score
            return secondary_score

        ps = calculate_primary(self)
        ss = calculate_secondary(self)
        return ps + ss