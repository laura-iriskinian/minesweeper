import pygame
import os
import json


pygame.init()

CELL_SIZE = 30
MARGIN = 1
COLORS = {
    'hidden': (200, 200, 200),
    'revealed': (180, 180, 180),
    'flag': (255, 0, 0),
    'text': (0, 0, 0),
    'menu_bg': (0, 102, 102),
    'button': (153, 153, 204),
    'button_hover': (51, 204, 102),
    'button_text': (255, 255, 255)
}

DIFFICULTIES = {
    'easy': {'size': (15, 14), 'mines': (10, 15), 'name': 'Easy'},
    'medium': {'size': (22, 22), 'mines': (40, 60), 'name': 'Medium'},
    'hard': {'size': (30, 20), 'mines': (99, 150), 'name': 'Difficult'}
}

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

number_sprites = {
    1: spr_grid1, 2: spr_grid2, 3: spr_grid3, 4: spr_grid4,
    5: spr_grid5, 6: spr_grid6, 7: spr_grid7, 8: spr_grid8
}

TEXTS = {
    'title': "MINE SWEEPER",
    'menu': "Menu",
    'restart': "Reset",
    'time': "T: {} sec",
    'mines': "M: {}",
    'win': "You won!",
    'lose': "You lost!",
    'highscores': "Hall of fame",
    'back': "Back",
    'exit': "Exit",
    'flags': "Flags: {}",
    'easy': "Easy",
    'medium': "Medium",
    'hard': "Difficult"
}

def save_score(difficulty, score):
    """Ajoute un nouveau score et sauvegarde les N meilleurs (plus bas) temps."""
    # Nombre de scores à conserver
    MAX_SCORES = 1  # Vous pouvez changer cette valeur

    # Charger les scores existants
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            try:
                scores = json.load(f)
            except json.JSONDecodeError:
                scores = {'easy': [], 'medium': [], 'hard': []}
    else:
        scores = {'easy': [], 'medium': [], 'hard': []}
    
    # Ajouter le nouveau score
    if difficulty not in scores:
        scores[difficulty] = []
    
    scores[difficulty].append(score)
    # Garder uniquement les N plus bas temps
    scores[difficulty] = sorted(scores[difficulty])[:MAX_SCORES]

    # Sauvegarder les scores
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

def show_scores(self):
    """Affiche les scores lorsqu'on clique sur le bouton."""
    self.load_scores()  # Charger les scores depuis le fichier
    self.showing_scores = True


def load_image(name, size):
    try:
        image = pygame.image.load(name)
        return pygame.transform.scale(image, size)
    except:
        surface = pygame.Surface(size)
        surface.fill((255, 0, 0))
        font = pygame.font.SysFont('Arial', 20)
        text = font.render("BOMB", True, (255, 255, 255))
        surface.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 - text.get_height()//2))
        return surface








