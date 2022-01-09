class NoPossibleMovesException(Exception):
    """Raised when the user can make no plays during turn."""
    pass


class TurnSkippedException(Exception):
    """Raised when the user skips his turn."""
    pass


class CoordinateError(IndexError):
    """Raised when access to non-existing board square is attempted."""

    def __init__(self, coords):
        msg = f'Square at coordinate ({coords[0]}, {coords[1]}) does not exist.'
        super().__init__(msg)


class MoveError(ValueError):
    """General error for an invalid move."""

    def __init__(self, msg=None):
        if not msg:
            msg = "Invalid move."
        super().__init__(msg)


class PlacementError(MoveError):
    """Raised when an invalid word placement is attempted."""

    def __init__(self, msg=None):
        if not msg:
            msg = "Invalid placement."
        super().__init__(msg)


class AnchorSquareError(PlacementError):
    """Raised when word has no valid anchor square to existing word."""

    def __init__(self):
        msg = "Invalid placement; no valid connection to existing word."
        super().__init__(msg)


class StartingSquareError(PlacementError):
    """Raised when the starting word does not cross the board center."""

    def __init__(self):
        msg = "Invalid placement; first word must cross the center of the board."
        super().__init__(msg)


class WordError(MoveError):
    """Raised when an invalid word is attempted."""

    def __init__(self, msg=None):
        if not msg:
            msg = "Invalid word."
        super().__init__(msg)


class MissingRequiredLetterError(WordError):
    """Raised when a word is played and the player is missing a required letter."""

    def __init__(self, letters):
        msg = f'Invalid word; rack is missing required letter {str(letters)}.'
        super().__init__(msg)


class DictionaryError(WordError):
    """Raised when a word is not present in word dictionary."""

    def __init__(self, word):
        msg = f"Invalid word; {word} not found in game's dictionary."
        super().__init__(msg)


class NonUniquePlayerNameException(Exception):
    """Raised when a player attempts to join game with same name as prior player."""

    def __init__(self):
        msg = "Player name already exists and names must be unique."
        super().__init__(msg)
