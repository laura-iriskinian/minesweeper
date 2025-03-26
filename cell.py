

class Cell:
    def __init__(self):
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.question = False
        self.neighbor_mines = 0

    def __str__(self):
        if self.flagged:
            return "F"
        if self.question:
            return "?"
        if not self.revealed:
            return " "
        if self.is_mine:
            return "*"
        return str(self.neighbor_mines) if self.neighbor_mines > 0 else " "