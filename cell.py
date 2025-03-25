import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


class Cell:
    def __init__(self, x, y, size, shift):
        self.x = x
        self.y = y
        self.size = size
        self.shift = shift
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.mines_around = 0

    def draw(self, screen):
        rect = pygame.Rect(self.x * self.size, self.y * self.size + self.shift, self.size, self.size)
        Cell = Cell(self.x, self.y, self.size, self.shift)
        if self.is_revealed:
            if self.is_mine:
                Cell.blit(spr_mineClicked, rect)
            else:
                Cell.blit(spr_emptyGrid, rect)
                if self.mines_around > 0:
                    if self.mines_around == 1:
                        Cell.blit(spr_grid1, rect)
                    elif self.mines_around == 2:
                        Cell.blit(spr_grid2, rect)
                    elif self.mines_around == 3:
                        Cell.blit(spr_grid3, rect)
                    elif self.mines_around == 4:
                        Cell.blit(spr_grid4, rect)
                    elif self.mines_around == 5:
                        Cell.blit(spr_grid5, rect)
                    elif self.mines_around == 6:
                        Cell.blit(spr_grid6, rect)
                    elif self.mines_around == 7:
                        Cell.blit(spr_grid7, rect)
                    elif self.mines_around == 8:
                        Cell.blit(spr_grid8, rect)
        else:
            if self.is_flagged:
                Cell.blit(spr_flag, rect)  
            else:   
                Cell.blit(spr_grid, rect)


    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged


    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return self.is_mine
        return False
