import random

from constants import PIECES
from tetromino import Tetromino


class Bag:
    def __init__(self):
        self.genPieces()
        self.bag = self.fillBag()

    def fillBag(self):
        self.bag = random.shuffle(self.pieces)

    def genPieces(self):
        for p in PIECES:
            self.pieces.append(Tetromino(p.name, p.shape2d,
                                         p.offset, p.colour))

    def viewNextPeice(self):
        return self.bag[-1]

    def getNextPeice(self):
        if len(self.bag) <= 0:
            self.fillBag()

        return self.bag.pop()
