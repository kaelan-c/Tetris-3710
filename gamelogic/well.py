from .cell import Cell
from .constants import GRID

class Well:
    def __init__(self):
        self.height = GRID["Height"]
        self.width = GRID["Width"]
        self.depth = GRID["Depth"]
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]  # Initialize the grid

    def generateGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = Cell()

    def getGrid(self):
        return self.grid

    def getGridCell(self, x, y):
        return self.grid[x][y]

    def placePiece(self):
        print("Check place piece stub")

    def checkGrid(self):
        for i in range(self.height):
            cell_count = 0
            for j in range(self.width):
                empty, colour = self.grid[i][j].getStatus()
                if not empty:
                    cell_count += 1
            if cell_count == self.width:
                self.clearLine(i)

    def clearLine(self, i):
        del self.grid[i]
        self.grid.insert(0, [Cell()] * self.width)
