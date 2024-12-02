# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher

import random
from .tetromino import Tetromino


# The bag class is responsible for generating pieces and
# randomly releasing them in accordance to the tetris algorithm
class Bag:
    def __init__(self, piece_config, spawn):
        self.piece_config = piece_config
        self.spawn = spawn
        self.bag = self.fill_bag()

    # Generate random pieces occording to passed piece config object
    def gen_pieces(self, piece_config, spawn):
        pieces = []
        for p in piece_config:
            pieces.append(Tetromino(p['name'], p['shape'], spawn, p['model'],))
        return pieces

    # Fill the bag with a random sample of generated pieces
    def fill_bag(self):
        pieces = self.gen_pieces(
            self.piece_config, self.spawn)
        return random.sample(pieces, len(pieces))

    # Return the piece at the top of the bag
    def view_next_peice(self):
        return self.bag[-1]if self.bag else None

    # Pop the next piece out of the bag
    def pop_next_piece(self):
        if len(self.bag) == 0:
            self.bag = self.fill_bag()
        return self.bag.pop()
