import pygame
import random
import time
import os


pygame.init()


CELL_SIZE = 30
MARGIN = 1
COLORS = {
    'hidden': (200, 200, 200),
    'revealed': (180, 180, 180),
    'flag': (255, 0, 0),
    'text': (0, 0, 0),
    'numbers': [None, (0, 0, 255), (0, 128, 0), (255, 0, 0),
                (0, 0, 128), (128, 0, 0), (0, 128, 128),
                (0, 0, 0), (128, 128, 128)],
    'menu_bg': (50, 50, 50),
    'button': (100, 100, 100),
    'button_hover': (150, 150, 150),
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

TEXTS = {
    'title': "MINE SWEEPER",
    'menu': "Menu",
    'restart': "Reset",
    'time': "T: {} sec",
    'mines': "M: {}",
    'win': "You won!",
    'lose': "You lost!",
    'highscores': "SCORES",
    'back': "Back",
    'exit': "Exit",
    'flags': "Flags: {}",
    'easy': "Easy",
    'medium': "Medium",
    'hard': "Difficult"
}


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


# if not os.path.exists('images'):
#     os.makedirs('images')


# if not os.path.exists('images/bomb.png'):
#     bomb_img = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10))
#     bomb_img.fill((0, 0, 0))
#     pygame.draw.circle(bomb_img, (255, 0, 0), (CELL_SIZE//2-5, CELL_SIZE//2-5), CELL_SIZE//2-5)
#     pygame.image.save(bomb_img, 'images/bomb.png')

bomb_image = load_image('images/bomb.png', (CELL_SIZE-10, CELL_SIZE-10))

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

class Board:
    def __init__(self, width, height, mine_range):
        self.width = width
        self.height = height
        self.mine_range = mine_range
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.first_click = True
        self.game_over = False
        self.win = False
        self.mines = set()
        self.flags = 0
        self.questions = 0

    def place_mines(self, first_click_pos):
        x, y = first_click_pos
        mines_count = random.randint(*self.mine_range)
        
        forbidden = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))
        
        possible_positions = []
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) not in forbidden:
                    possible_positions.append((i, j))
        
        self.mines = set(random.sample(possible_positions, mines_count))
        
        for x, y in self.mines:
            self.grid[y][x].is_mine = True
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.grid[ny][nx].neighbor_mines += 1

    # game conditions
    def reveal(self, x, y):
        cell = self.grid[y][x]
        
        if cell.revealed or cell.flagged or self.game_over:
            return False
        
        if self.first_click:
            self.place_mines((x, y))
            self.first_click = False
        
        if cell.is_mine:
            self.game_over = True
            return True
        
        cell.revealed = True
        
        if cell.neighbor_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal(nx, ny)
        
        if self.check_win():
            self.win = True
            self.game_over = True
        
        return False

    def toggle_flag(self, x, y):
        cell = self.grid[y][x]
        
        if cell.revealed or self.game_over:
            return
        
        if not cell.flagged and not cell.question:
            cell.flagged = True
            self.flags += 1
        elif cell.flagged:
            cell.flagged = False
            cell.question = True
            self.flags -= 1
            self.questions += 1
        elif cell.question:
            cell.question = False
            self.questions -= 1

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if not cell.is_mine and not cell.revealed:
                    return False
        return True
    
    #sprites
    def draw(self, screen, font, offset_y=0):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                rect = pygame.Rect(
                    x * (CELL_SIZE + MARGIN),
                    y * (CELL_SIZE + MARGIN) + offset_y,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                if cell.revealed:
                    color = COLORS['revealed']
                elif cell.flagged:
                    color = COLORS['flag']
                else:
                    color = COLORS['hidden']
                
                pygame.draw.rect(screen, color, rect)
                
                if cell.revealed:
                    if cell.is_mine:
                        screen.blit(spr_mineClicked, rect)
                    elif cell.neighbor_mines > 0:
                        text = font.render(str(cell.neighbor_mines), True, COLORS['numbers'][cell.neighbor_mines])
                        screen.blit(text, text.get_rect(center=rect.center))
                elif cell.flagged:
                    screen.blit(spr_flag, rect)
                elif cell.question:
                    text = font.render("?", True, COLORS['text'])
                    screen.blit(text, text.get_rect(center=rect.center))

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.clicked = False
    
    def draw(self, screen, font):
        color = COLORS['button_hover'] if self.hovered else COLORS['button']
        if self.clicked:
            color = (80, 80, 80)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, COLORS['button_text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.hovered and self.clicked:
                self.clicked = False
                if self.action:
                    self.action()
            else:
                self.clicked = False
        return False

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 30)
        
      
        menu_width = 300
        menu_height = 400
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2
        
       
        button_width = 200
        button_height = 50
        start_y = menu_y + 80
        
        self.buttons = [
            Button(menu_x + (menu_width - button_width)//2, start_y, button_width, button_height, 
                   TEXTS['easy'], lambda: self.set_difficulty('easy')),
            Button(menu_x + (menu_width - button_width)//2, start_y + 70, button_width, button_height, 
                   TEXTS['medium'], lambda: self.set_difficulty('medium')),
            Button(menu_x + (menu_width - button_width)//2, start_y + 140, button_width, button_height, 
                   TEXTS['hard'], lambda: self.set_difficulty('hard')),
            Button(menu_x + (menu_width - button_width)//2, start_y + 210, button_width, button_height, 
                   TEXTS['highscores'], self.show_scores),
            Button(menu_x + (menu_width - button_width)//2, start_y + 280, button_width, button_height, 
                   TEXTS['exit'], self.exit_game)
        ]
        
        self.selected_difficulty = None
        self.showing_scores = False
        self.scores = {'easy': float('inf'), 'medium': float('inf'), 'hard': float('inf')}  
    
    def set_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
    
    def show_scores(self):
        self.showing_scores = True
    
    def exit_game(self):
        pygame.quit()
        exit()
    
    def draw(self, screen):
      
        screen.fill(COLORS['menu_bg'])
        
        
        title = self.title_font.render(TEXTS['title'], True, (255, 255, 255))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        if self.showing_scores:
                 
                    back_button = Button(50, 50, 100, 40, TEXTS['back'], self.hide_scores)
                    mouse_pos = pygame.mouse.get_pos()
                    back_button.check_hover(mouse_pos)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                            back_button.handle_event(event)
                    back_button.draw(screen, self.button_font)
                    
                    scores_title = self.title_font.render(TEXTS['highscores'], True, (255, 255, 255))
                    screen.blit(scores_title, (self.screen_width//2 - scores_title.get_width()//2, 150))
                    
                    y_offset = 250
                    for diff, score in self.scores.items():
                        if score == float('inf'):
                            score_text = f"{DIFFICULTIES[diff]['name']}: --"
                        else:
                            score_text = f"{DIFFICULTIES[diff]['name']}: {int(score)} sec"
                        rendered_text = self.button_font.render(score_text, True, (255, 255, 255))
                        screen.blit(rendered_text, (self.screen_width//2 - rendered_text.get_width()//2, y_offset))
                        y_offset += 50

        else:
        
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(mouse_pos)
                button.draw(screen, self.button_font)
    
    def hide_scores(self):
        self.showing_scores = False
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.handle_event(event)

class Game:
    def __init__(self):
        self.difficulty = None
        self.screen = None
        self.clock = pygame.time.Clock()
        self.menu = None
        self.board = None
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 30, bold=True)
        self.start_time = None
        self.elapsed_time = 0
        self.game_active = False
        self.top_panel_height = 60
    
    def run(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(TEXTS['title'])
        self.menu = Menu(800, 600)
        
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            if self.game_active:
             
                self.handle_game_events(events)
                self.draw_game()
            else:
              
                self.menu.handle_events(events)
                self.menu.draw(self.screen)
                
                if self.menu.selected_difficulty:
                    self.difficulty = self.menu.selected_difficulty
                    self.reset()
                    self.game_active = True
                    self.menu.selected_difficulty = None
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
    
    def reset(self):
        config = DIFFICULTIES[self.difficulty]
        self.board = Board(config['size'][0], config['size'][1], config['mines'])
        self.start_time = None
        self.elapsed_time = 0
        
       
        width = config['size'][0] * (CELL_SIZE + MARGIN)
        height = config['size'][1] * (CELL_SIZE + MARGIN) + self.top_panel_height
        self.screen = pygame.display.set_mode((width, height))
    
    def return_to_menu(self):
        self.game_active = False
        self.screen = pygame.display.set_mode((800, 600))
    
    def handle_game_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
         
                if pos[1] < self.top_panel_height:
            
                    menu_button_rect = pygame.Rect(10, 10, 100, 40)
                    if menu_button_rect.collidepoint(pos):
                        self.return_to_menu()
                        return
                    
                  
                    restart_rect = pygame.Rect(self.screen.get_width() - 110, 10, 100, 40)
                    if restart_rect.collidepoint(pos):
                        self.reset()
                        return
                
           
                elif pos[1] >= self.top_panel_height:
                    x = pos[0] // (CELL_SIZE + MARGIN)
                    y = (pos[1] - self.top_panel_height) // (CELL_SIZE + MARGIN)
                    
                    if 0 <= x < self.board.width and 0 <= y < self.board.height:
                        if event.button == 1:  
                            if self.start_time is None and not self.board.first_click:
                                self.start_time = time.time()
                            self.board.reveal(x, y)
                        elif event.button == 3:  
                            self.board.toggle_flag(x, y)
    
    def draw_game(self):
        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((220, 220, 220))
        
    
        panel_rect = pygame.Rect(0, 0, screen_width, self.top_panel_height)
        pygame.draw.rect(self.screen, (180, 180, 180), panel_rect)
        pygame.draw.line(self.screen, (150, 150, 150), (0, self.top_panel_height), 
                         (screen_width, self.top_panel_height), 2)
        
      
        menu_button = Button(10, 10, 100, 40, TEXTS['menu'], self.return_to_menu)
        mouse_pos = pygame.mouse.get_pos()
        menu_button.check_hover(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                menu_button.handle_event(event)
        menu_button.draw(self.screen, self.font)
        
       
        restart_button = Button(screen_width - 110, 10, 100, 40, TEXTS['restart'], self.reset)
        restart_button.check_hover(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                restart_button.handle_event(event)
        restart_button.draw(self.screen, self.font)
        
  
        if self.start_time and not self.board.game_over:
            self.elapsed_time = time.time() - self.start_time
        time_text = self.font.render(TEXTS['time'].format(int(self.elapsed_time)), True, (0, 0, 0))
        self.screen.blit(time_text, (screen_width//2 - time_text.get_width()//2, 20))
    

        mines_text = self.font.render(TEXTS['mines'].format(len(self.board.mines) - self.board.flags), True, (0, 0, 0))
        self.screen.blit(mines_text, (150, 20))
        

        self.board.draw(self.screen, self.font, self.top_panel_height)
        
   
        if self.board.game_over:
            message = TEXTS['win'] if self.board.win else TEXTS['lose']
            text = self.big_font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
            
           
            s = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.screen.blit(s, (text_rect.x - 20, text_rect.y - 10))
            
            self.screen.blit(text, text_rect)
            

            if self.board.win and self.elapsed_time < self.menu.scores[self.difficulty]:
                self.menu.scores[self.difficulty] = self.elapsed_time

if __name__ == "__main__":
    game = Game()
    game.run()