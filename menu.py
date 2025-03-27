from button import Button
from common import *

class Menu:
    """initiate main menu"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True, italic = True)
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
        #back button for hall of fame
        self.back_button = Button(50, 50, 100, 40, TEXTS['back'], self.return_to_menu)
        self.selected_difficulty = None
        self.showing_scores = False
        #open json file to save scores
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError:
                    self.scores = {'easy': [], 'medium': [], 'hard': []}
        else:
            self.scores = {'easy': [], 'medium': [], 'hard': []}
    
    def set_difficulty(self, difficulty):
        """method to set the difficulty level selected"""
        self.selected_difficulty = difficulty
    
    def load_scores(self):
        """method to load json with best cores"""
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError:
                    self.scores = {'easy': [], 'medium': [], 'hard': []}
        else:
            self.scores = {'easy': [], 'medium': [], 'hard': []}

    def show_scores(self):
        """load scores before displaying them"""
        self.load_scores()  
        self.showing_scores = True
        
    def exit_game(self):
        """possibility to exit the game through button"""
        pygame.quit()
        exit()
    
    def draw(self, screen):
        """method to display the menu"""
        screen.fill(COLORS['menu_bg'])

        #main title
        title = self.title_font.render(TEXTS['title'], True, (255, 255, 255))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        #hall of fame menu
        if self.showing_scores:            
            mouse_pos = pygame.mouse.get_pos()
            self.back_button.check_hover(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.back_button.handle_event(event)

            self.back_button.draw(screen, self.button_font)

            # Score titles
            scores_title = self.title_font.render(TEXTS['highscores'], True, (255, 255, 255))
            screen.blit(scores_title, (self.screen_width // 2 - scores_title.get_width() // 2, 150))

            # number os scores to display
            MAX_SCORES_DISPLAY = 1  # This can be modified 

            # Display of best score per level
            y_offset = 250
            for diff, scores in self.scores.items():
                if scores:  
                    scores_text = f"{DIFFICULTIES[diff]['name']}: " 
                    
                    # Gets the smallest times and formats them
                    lowest_scores = sorted(scores)[:MAX_SCORES_DISPLAY]
                    scores_text += ", ".join(f"{s} sec" for s in lowest_scores)

                    rendered_text = self.button_font.render(scores_text, True, (255, 255, 255))
                    screen.blit(rendered_text, (self.screen_width // 2 - rendered_text.get_width() // 2, y_offset))
                    y_offset += 50

        else:
            # Display of menu buttons
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(mouse_pos)
                button.draw(screen, self.button_font)


    def return_to_menu(self):
        """method to return to main menu"""
        self.showing_scores = False
    
    def handle_events(self, events):
        """handle events in menu"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.showing_scores:
                    self.back_button.handle_event(event) 
                else:
                    for button in self.buttons:
                        button.handle_event(event)