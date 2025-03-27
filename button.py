from common import *

class Button:
    """ Initiate button"""
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.clicked = False
    
    def draw(self, screen, font):
        """ display buttons"""
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
