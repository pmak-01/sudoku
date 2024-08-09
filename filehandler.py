import csv

class FileHandler():
    def __init__(self):
        self.grid = [[None for i in range(9)] for j in range(9)]

    def read_file(self, filename : str):
        with open(filename) as f:
            reader = csv.reader(f)

            i = 0
            for line in reader:
                for j in range(len(line)):
                    if line[j].strip() != '_':
                        self.grid[i][j] = int(line[j])
                i += 1
