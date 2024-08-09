from filehandler import FileHandler
from random import choice

class Variable():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.domain = set([i for i in range(1, 10)])
        self.value = None

    def mark_value(self, n: int):
        if self.domain:
            self.domain = None
            self.value = n

    def remove_value(self, n: int):
        if self.domain:
            self.domain.discard(n)

    def infer(self) -> bool:
        if not self.domain:
            return False
        if len(self.domain) == 1:
            for x in self.domain: self.value = x
            self.domain = None
            return True
        else:
            return False

    def known_value(self):
        if not self.domain:
            return ((self.i, self.j), self.value)
        if len(self.domain) == 1:
            for x in self.domain: self.value = x
            self.domain = None
            return ((self.i, self.j), self.value)
        else:
            return None

    def __repr__(self):
        if self.domain:
            return f'Variable({self.i}, {self.j}, {self.domain})'
        else:
            return f'Variable({self.i}, {self.j}, value = {self.value})'

class SudokuSolver():
    def __init__(self, grid = None):
        '''Stores the grid size and creates an empty grid of Variable objects.
        Also creates a list of Variables according to rows, columns, subgrids'''
        self.size = 9
        
        self.safe_moves = []
        self.moves_made = set()

        self.grid = []
        
        self.rows = []
        self.columns = []
        self.subgrids = [[] for i in range(9)]
        for i in range(9):
            self.grid.append([])
            for j in range(9):
                self.grid[i].append(Variable(i, j))
                
                # subgrid_index = self.get_subgrid_index((i, j))
                # self.subgrids[subgrid_index].append(self.grid[i][j])

            self.rows.append(self.grid[i])

        for i in range(9):
            self.columns.append([self.grid[j][i] for j in range(9)])

        self.game_grid = [[None for i in range(self.size)] for j in range(self.size)]
        if grid:
            for i in range(9):
                for j in range(9):
                    if grid[i][j]:
                        self.game_grid[i][j] = grid[i][j]
                        self.mark_known((i, j), grid[i][j])
                        self.moves_made.add(((i, j), grid[i][j]))
    
    def get_subgrid_corners(self, pos: tuple[int]) -> list:
        i, j = pos
        ref = dict()
        ref[0] = [(0, 0), (2, 2)]
        ref[1] = [(0, 3), (2, 5)]
        ref[2] = [(0, 6), (2, 8)]
        ref[3] = [(3, 0), (5, 2)]
        ref[4] = [(3, 3), (5, 5)]
        ref[5] = [(3, 6), (5, 8)]
        ref[6] = [(6, 0), (8, 2)]
        ref[7] = [(6, 3), (8, 5)]
        ref[8] = [(6, 6), (8, 8)]

        for r in range(9):
            subgrid_corner = ref[r]
            start_i, start_j = subgrid_corner[0]
            end_i, end_j = subgrid_corner[1]
            if start_i <= i <= end_i and start_j <= j <= end_j:
                return subgrid_corner

    def mark_known(self, pos: tuple[int], n: int):
        '''Marks Variables in `self.grid` according to the partially filled grid provided'''
        i, j = pos
        self.grid[i][j].mark_value(n)

        self.infer_from(pos)

    def mark_incorrect(self, pos:tuple[int], n: int):
        i, j = pos
        self.grid[i][j].remove_value(n)

        self.infer_from(pos)

    def infer_from(self, pos: tuple[int]):
        '''Updates all cells in the row, column and subgrid of the given marked cell
        and adds new known moves to `self.safe_moves`'''
        i, j = pos

        # update row
        for x in range(9):
            self.grid[i][x].remove_value(self.grid[i][j].value)
            new_inference = self.grid[i][x].infer()
            if new_inference:
                safe_move = self.grid[i][x].known_value()
                if safe_move:
                    self.safe_moves.append(safe_move)
                    self.infer_from((i, x))
        
        # update column
        for y in range(9):
            self.grid[y][j].remove_value(self.grid[i][j].value)
            new_inference = self.grid[y][j].infer()
            if new_inference:
                safe_move = self.grid[y][j].known_value()
                if safe_move:
                    self.safe_moves.append(safe_move)
                    self.infer_from((y, j))
        
        # update subgrid
        subgrid_corners = self.get_subgrid_corners(pos)
        start_i, start_j = subgrid_corners[0]
        end_i, end_j = subgrid_corners[1]
        for y in range(start_i, end_i+1):
            for x in range(start_j, end_j+1):
                self.grid[y][x].remove_value(self.grid[i][j].value)
                new_inference = self.grid[y][x].infer()
                if new_inference:
                    safe_move = self.grid[y][x].known_value()
                    if safe_move:
                        self.safe_moves.append(safe_move)
                        self.infer_from((y, x))

    def query_safe_move(self):
        while len(self.safe_moves) > 0:
            move = self.safe_moves.pop(0)
            i, j = move[0]
            if not self.game_grid[i][j]:
                self.game_grid[i][j] = move[1]
                self.mark_known(move[0], move[1])
                return move
        return None
    
    def len_key(self, var: Variable) -> int:
        if var.domain:
            return len(var.domain)
        else:
            return 10

    def query_random_move(self):
        all_cells = []
        for row in self.grid:
            for cell in row:
                all_cells.append(cell)
        all_cells.sort(key=self.len_key)
        pos = all_cells[0].i, all_cells[0].j
        val = choice(list(all_cells[0].domain))
        return(pos, val)
    
    def get_reply(self, query_move: tuple, is_correct: bool):
        if is_correct:
            i, j = query_move[0]
            self.game_grid[i][j] = query_move[1]
            self.mark_known(query_move[0], query_move[1])
        else:
            self.mark_incorrect(query_move[0], query_move[1])

    def is_complete(self) -> bool:
        for i in range(9): 
            for j in range(9):
                if not self.game_grid[i][j]:
                    return False
        return True
    
    def print(self):
        for i in range(9):
            s = ''
            for j in range(9):
                val = self.game_grid[i][j]
                if val:
                    s += f'{val} '
                else:
                    s += '_ '
            print(s)
        print()
fh = FileHandler()
fh.read_file('grid.txt')
ss = SudokuSolver(fh.grid)