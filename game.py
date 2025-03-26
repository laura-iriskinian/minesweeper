from menu import Menu
from common import *
from board import Board
from button import Button
import time


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
                            if self.start_time is None :
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