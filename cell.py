

class Cell:
    """ Initiate cell"""
    def __init__(self):
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.question = False
        self.neighbor_mines = 0

    