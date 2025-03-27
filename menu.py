from button import Button
from common import *

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
        
        self.back_button = Button(50, 50, 100, 40, TEXTS['back'], self.return_to_menu)
        self.selected_difficulty = None
        self.showing_scores = False
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError:
                    self.scores = {'easy': [], 'medium': [], 'hard': []}
        else:
            self.scores = {'easy': [], 'medium': [], 'hard': []}
    
    def set_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
    
    def load_scores(self):
        """Recharge les scores depuis le fichier JSON."""
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError:
                    self.scores = {'easy': [], 'medium': [], 'hard': []}
        else:
            self.scores = {'easy': [], 'medium': [], 'hard': []}

    def show_scores(self):
        """Charge les scores avant de les afficher."""
        self.load_scores()  # Ajoutez cet appel
        self.showing_scores = True
        
    def exit_game(self):
        pygame.quit()
        exit()
    
    def draw(self, screen):
        screen.fill(COLORS['menu_bg'])
        
        if self.showing_scores:
            # Bouton retour
            
            mouse_pos = pygame.mouse.get_pos()
            self.back_button.check_hover(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.back_button.handle_event(event)

            self.back_button.draw(screen, self.button_font)

            # Titre des scores
            scores_title = self.title_font.render(TEXTS['highscores'], True, (255, 255, 255))
            screen.blit(scores_title, (self.screen_width // 2 - scores_title.get_width() // 2, 150))

            # Nombre de scores à afficher
            MAX_SCORES_DISPLAY = 1  # Vous pouvez changer cette valeur

            # Affichage des meilleurs scores pour chaque difficulté
            y_offset = 250
            for diff, scores in self.scores.items():
                if scores:  # Ne traiter que les difficultés avec des scores
                    scores_text = f"{DIFFICULTIES[diff]['name']}: " 
                    
                    # Prend les N plus bas temps et les formate
                    lowest_scores = sorted(scores)[:MAX_SCORES_DISPLAY]
                    scores_text += ", ".join(f"{s} sec" for s in lowest_scores)

                    rendered_text = self.button_font.render(scores_text, True, (255, 255, 255))
                    screen.blit(rendered_text, (self.screen_width // 2 - rendered_text.get_width() // 2, y_offset))
                    y_offset += 50

        else:
            # Affichage des boutons du menu
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(mouse_pos)
                button.draw(screen, self.button_font)

    
    # def hide_scores(self):
    #     self.showing_scores = False

    def return_to_menu(self):
        self.showing_scores = False
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.showing_scores:
                    self.back_button.handle_event(event) 
                else:
                    for button in self.buttons:
                        button.handle_event(event)