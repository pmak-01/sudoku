from filehandler import FileHandler

class Variable:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.pos = (i, j)
        self.val = None
        self.domain = {i for i in range(1, 10)}

    def __repr__(self):
        return f'Variable({self.pos}, {self.domain})'

class SudokuSolver:

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


    def __init__(self, filehandler_grid: list[list[int]]):
        self.grid = [[None for i in range(9)] for j in range(9)]
        self.game_grid = filehandler_grid.copy()

        for i in range(9):
            for j in range(9):
                self.grid[i][j] = Variable(i, j)
                if self.game_grid[i][j]:
                    self.grid[i][j].domain = {self.game_grid[i][j]}

    def get_subgrid_corners(self, pos: tuple[int]) -> list:
        '''For a given `pos`, return the coordinates of the two corners 
        (top-left & bottom-right) of the subgrid that it is part of'''
        i, j = pos

        for r in range(9):
            subgrid_corner = SudokuSolver.ref[r]
            start_i, start_j = subgrid_corner[0]
            end_i, end_j = subgrid_corner[1]
            if start_i <= i <= end_i and start_j <= j <= end_j:
                return subgrid_corner

    def solve(self):
        '''Calls the required functions to solve the sudoku, if possible'''
        print(self.ac3())
        print(self.backtrack())
        print(self.grid)
        print()
        print(self.game_grid)

    def revise(self, pos: tuple) -> bool:
        '''Given a confirmed Variable _Var_ at `pos`, make each `Variable` in its row, 
        column and subgrid arc consistent with _Var_
        
        Returns `True` if all the checked Variables have non-empty domains
        and `False` otherwise
        '''
        i, j = pos
        val = self.game_grid[i][j]
        ans = True
        if not val:
            return None
        
        # update row
        for x in range(9):
            if (i, x) == pos:
                continue
            if val in self.grid[i][x].domain:
                self.grid[i][x].domain.remove(val)
                if len(self.grid[i][x].domain) == 0:
                    ans = False

        # update column
        for y in range(9):
            if (y, j) == pos:
                continue
            if val in self.grid[y][j].domain:
                self.grid[y][j].domain.remove(val)
                if len(self.grid[y][j].domain) == 0:
                    ans = False
            
        # update subgrid
        subgrid_corners = self.get_subgrid_corners(pos)
        start_i, start_j = subgrid_corners[0]
        end_i, end_j = subgrid_corners[1]
        for y in range(start_i, end_i+1):
            for x in range(start_j, end_j+1):
                if (y, x) == pos:
                    continue
                if val in self.grid[y][x].domain:
                    self.grid[y][x].domain.remove(val)
                    if len(self.grid[y][x].domain) == 0:
                        ans = False
        
        return ans

    def ac3(self) -> bool:
        '''Update the domains in `self.grid` so that all Variable domains are arc consistent
        with the confirmed values they share an arc with'''

        for i in range(9):
            for j in range(9):
                if not self.game_grid[i][j]:
                    continue
                if not self.revise((i, j)):
                    return False
        return True

    def assignment_complete(self) -> bool:
        '''Return `True` if assignment is complete (i.e. each variable has an assigned value),
        else return `False`. Here assignment is directly the `self.game_grid`'''
        for i in range(9):
            if not all(self.game_grid[i]):
                return False
        return True

    def consistent(self) -> bool:
        '''Check the entire game_grid whether current assignments agree with the 
        rules of the game. Here assignment is directly the `self.game_grid`'''
        full = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # check all rows
        for i in range(9):
            st = set()
            for j in range(9):
                if self.game_grid[i][j] != None and self.game_grid[i][j] in st:
                    return False
                st.add(self.game_grid[i][j])
            
        # check all columns
        for i in range(9):
            st = set()
            for j in range(9):
                if self.game_grid[j][i] != None and self.game_grid[j][i] in st:
                    return False
                st.add(self.game_grid[j][i])
        
        # check all subgrids
        for subgrid_corners in SudokuSolver.ref.values():
            st = set()
            start_i, start_j = subgrid_corners[0]
            end_i, end_j = subgrid_corners[1]
            for y in range(start_i, end_i+1):
                for x in range(start_j, end_j+1):
                    if self.game_grid[y][x] != None and self.game_grid[y][x] in st:
                        return False
                    st.add(self.game_grid[y][x])
            
        return True
    
    def select_unassigned_variable(self) -> tuple[int]:
        '''Select an unassigned Variable from the grid
        and return its position'''
        for i in range(9):
            for j in range(9):
                if not self.game_grid[i][j]:
                    return (i, j)
        return None
    
    def len_key(self, pos: tuple[int]) -> int:
        i, j = pos
        return len(self.grid[i][j].domain)

    def get_unassigned_variables(self):
        lst = []
        for i in range(9):
            for j in range(9):
                if not self.game_grid[i][j]:
                    lst.append((i, j))
        lst.sort(key = self.len_key)
        return lst

    def backtrack(self) -> bool:
        '''Use Backtracking Search to find a correct Sudoku assignment 
        using knowledge from `self.grid`. Assigns to the `self.game_grid`.
        Returns True if a valid assignment is made, False otherwise'''
        print(self.get_unassigned_variables())

        for pos in self.get_unassigned_variables():
            if self.assignment_complete():
                return True
            # pos = self.select_unassigned_variable()
            if not pos:
                break
            i, j = pos
            # print(pos, self.game_grid)
            for val in self.grid[i][j].domain:
                # print(pos, val, self.consistent())
                self.game_grid[i][j] = val
                if self.consistent():
                    if self.backtrack():
                        return True
                self.game_grid[i][j] = None
        return False

fh = FileHandler()
fh.read_file('grid.txt')
ss = SudokuSolver(fh.grid)
ss.solve()
