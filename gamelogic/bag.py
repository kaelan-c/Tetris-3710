import random
from .constants import PIECES
from .tetromino import Tetromino

class Bag:
    def __init__(self):
        self.pieces = []  # Initialize pieces list
        self.genPieces()
        self.fillBag()

    def fillBag(self):
        self.bag = self.pieces[:]  # Copy pieces to avoid mutation
        random.shuffle(self.bag)


    def genPieces(self):
        for p in PIECES.values():  # Iterate over the values (the dictionaries)
            self.pieces.append(
                Tetromino(p["name"], p["shape2d"], p["offset"], p["colour"])
            )  # Access the values in the dictionary


    def viewNextPiece(self):
        if self.bag:
            return self.bag[-1]
        else:
            self.fillBag()
            return self.bag[-1]

    def getNextPiece(self):
        if not self.bag:
            self.fillBag()
        return self.bag.pop()