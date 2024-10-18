class Cell:
    def __init__(self):
        self.colour = (0, 0, 0)
        self.empty = True

    def fillCell(self, colour):
        self.colour = colour
        self.empty = False

    def getEmptyState(self):
        return self.empty

    def getColour(self):
        return self.colour
