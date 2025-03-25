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
        self.font = pygame.font.SysFont(None, 36)


    def draw(self, screen):
        rect = pygame.Rect(self.x * self.size, self.y * self.size + self.shift, self.size, self.size)
        if self.is_revealed:
            if self.is_mine:
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.circle(screen, BLACK, rect.center, self.size // 4)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                if self.mines_around > 0:
                    text = self.font.render(str(self.mines_around), True, BLUE)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, DARK_GRAY if self.is_flagged else GRAY, rect)
        
        pygame.draw.rect(screen, BLACK, rect, 1)


    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged


    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return self.is_mine
        return False
