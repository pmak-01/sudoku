import sys
from sudoku import SudokuSolver, Variable
from filehandler import FileHandler
import pygame
pygame.init()

# Usage: python runner.py grid.txt
grid_file = sys.argv[1]

class Game:
    def __init__(self):
        self.filehandler = FileHandler()
        self.solver = SudokuSolver()
        self.drawer = Drawer()
        self.grid = None

    def read_file(self, grid_file: str):
        self.filehandler.read_file(grid_file)
        self.grid = self.filehandler.grid
        self.solver = SudokuSolver(self.grid)

    def get_move(self):
        self.move = self.solver.query_safe_move()
        if self.move:
            print("AI providing safe move: ")
            print(f"{self.move[0]}: {self.move[1]}")
        else:
            self.move = self.solver.query_random_move()
            print("AI providing random move: ")
            print(f"{self.move[0]}: {self.move[1]}")
            self.verify_move()
    
    def verify_move(self):
        reply = input('Is it correct? (y/n) ')
        if reply == 'y':
            pos, n = self.move[0], self.move[1]
            self.solver.get_reply(self.move, True)
        else:
            self.solver.get_reply(self.move, False)
        self.move = None

    def main(self):
        self.read_file(sys.argv[1])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.image.save(self.drawer.window, r'puzzle.png')
                    pygame.quit()
            
            if self.solver.is_complete():
                pygame.image.save(self.drawer.window, r'puzzle.png')
                pygame.quit()
                break

            self.get_move()
            self.drawer.draw(self.solver.game_grid)

class Drawer:
    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self):
        self.cell_size = 60
        self.game_size = 9
        self.window_height, self.window_width = self.cell_size*self.game_size, self.cell_size*self.game_size

        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.font = pygame.font.SysFont('algerian', self.cell_size-4)

    def draw(self, grid: list[list[int]]):
        for i in range(0, self.window_height, self.cell_size):
            for j in range(0, self.window_width, self.cell_size):
                cell_rect2 = pygame.Rect((j, i), (self.cell_size, self.cell_size))
                cell_rect1 = pygame.Rect((j+1, i+1), (self.cell_size-5, self.cell_size-5))
                digit = grid[i//self.cell_size][j//self.cell_size] if grid[i//self.cell_size][j//self.cell_size] else ' '
                digit = self.font.render(str(digit), 0, Drawer.black)
                pygame.draw.rect(self.window, Drawer.black, cell_rect2)
                pygame.draw.rect(self.window, Drawer.white, cell_rect1)
                self.window.blit(digit, cell_rect1)
        
        pygame.display.flip()

Game().main()