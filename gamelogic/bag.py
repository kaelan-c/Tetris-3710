# *** CPSC 3710 - Term Project
# *** Team Kernel Panic Attak:
# *** Ethan Fisher,Patrick Bulbrook,
# *** Kaelan Croucher

import random
from .tetromino import Tetromino


class Bag:
    def __init__(self, piece_config, spawn, render_root, loader):
        self.piece_config = piece_config
        self.spawn = spawn
        self.render_root = render_root
        self.loader = loader
        self.bag = self.fill_bag()

    def gen_pieces(self, piece_config, spawn, render_root, loader):
        pieces = []
        for p in piece_config:
            pieces.append(Tetromino(p['name'], p['shape'],
                                    spawn, p['shape_string'],
                                    render_root, loader))
        return pieces

    def fill_bag(self):
        pieces = self.gen_pieces(
            self.piece_config, self.spawn, self.render_root, self.loader)
        return random.sample(pieces, len(pieces))

    def view_next_peice(self):
        return self.bag[-1]if self.bag else None

    def pop_next_piece(self):
        if len(self.bag) == 0:
            self.bag = self.fill_bag()
        return self.bag.pop()
