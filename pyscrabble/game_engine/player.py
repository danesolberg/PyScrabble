from .rack import Rack


class Player:
    def __init__(self, name, computer_player, bag):
        self.name = name
        self.computer_player = computer_player
        self.rack = Rack(bag)
        self.score = 0

    def __repr__(self):
        return '<__main__.Player ' + self.name + ' >'

    def get_name(self):
        return self.name

    def increase_score(self, score_increment):
        self.score += score_increment

    def get_score(self):
        return self.score

    def get_rack(self):
        return self.rack

    def is_computer(self):
        return self.computer_player
