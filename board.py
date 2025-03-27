from common import *
from cell import Cell
import random

class Board:
    """Inititate game board"""
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
        """method to place mines randomly on the game board"""
        x, y = first_click_pos
        mines_count = random.randint(*self.mine_range)
        
        #prevents a mine from being on the first click
        forbidden = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))
        
        #possible places where the mines can be after first click
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

    def reveal(self, x, y):
        """method to reveal the cells when clicked"""
        cell = self.grid[y][x]
        
        if cell.revealed or cell.flagged or self.game_over:
            return False
        
        if self.first_click:
            self.first_click = False
            self.place_mines((x, y))
            
        if cell.is_mine:
            cell.revealed = True  # change mine to revealed so it shows
            self.game_over = True
            return True
        
        cell.revealed = True
        
        #recursion
        if cell.neighbor_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal(nx, ny)
        
        #condition for ending game
        if self.check_win():
            self.win = True
            self.game_over = True
        
        return False

    def toggle_flag(self, x, y):
        """method to display flag or question mark"""
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

    def draw(self, screen, font, offset_y=0):
        """method to display board"""
        last_clicked_mine = None  # Variable to keep track of the mine clicked
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                rect_x = x * (CELL_SIZE + MARGIN)
                rect_y = y * (CELL_SIZE + MARGIN) + offset_y
                
                #display appropriate sprites when cell clicked
                if cell.revealed:
                    if cell.is_mine:
                        if self.game_over:
                            screen.blit(spr_mineClicked, (rect_x, rect_y))
                        else: 
                            screen.blit(spr_mine, (rect_x, rect_y))
                    elif cell.neighbor_mines > 0:
                        screen.blit(number_sprites[cell.neighbor_mines], (rect_x, rect_y))
                    else:
                        screen.blit(spr_emptyGrid, (rect_x, rect_y))
                else:
                    # If game is over, display all the minbes
                    if self.game_over and cell.is_mine:
                        # Differentiate the mine clicked
                        if cell.revealed:
                            screen.blit(spr_mineClicked, (rect_x, rect_y))
                        else:
                            screen.blit(spr_mine, (rect_x, rect_y))
                    else:
                        screen.blit(spr_grid, (rect_x, rect_y))  #basic grid cell not yet revealed
                        if cell.flagged:
                            screen.blit(spr_flag, (rect_x, rect_y))  # flag
                        elif cell.question:
                            text = font.render("?", True, (255, 0, 0))  # question mark as rendered text
                            text_rect = text.get_rect(center=(rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 2))
                            screen.blit(text, text_rect)