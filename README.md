# Sudoku Solver
My very own Sudoku Solver. This solver started as a project for Harvard CS50's Intro to AI with Python online MOOC. Two versions exist: `v1` requires verification from the user, while `v2` automatically computes a valid solution.


This program phrases Sudoku solving as a **Constraint Satisfaction Problem** (`CSP`) and applies relevant concepts and techniques such as **arc consistency** and **backtracking** based on the **AC-3 algorithm** to find a valid filling of the blanks in the grid. 

### v1
Example usage: `python runner.py grid2.txt`
1. Initially, the partially-filled grid is read from `grid2.txt`. In this case, it contains 2 blanks. The algorithm creates a domain of possible values (digits 1-9) for each of those blank spaces
2. Over several iterations, **arc consistency** is ensured. For each blank, it is ensured that its domain does not contain digits which are already present in its own row, column or subgrid. If, for any blank, only one possible value remains in the domain, this is inserted into the grid, performing a **safe move**. If the algorithm does not find such a safe move, it asks the user for assistance by suggesting a random move, and having the user check if the suggested move is valid or not. However, this method works only if the user has access to a filled grid.
3. Once the grid is filled, the program draws a filled grid using `pygame` and stores it in the file `puzzle.png`.

### v2
Example usage: `python sudoku_v2.py grid.txt`

This also utilises the AC-3 algorithm described above. A couple of heuristics are applied, which are stated in `improvements.txt`. This program always finds a valid solution if it exists, and prints it in the command window. Since this utilises recursion and tests many possible fillings, it results in longer runtimes than `v1`.