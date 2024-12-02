# *** CPSC 3710 - Term Project
# *** Team Kernel Panic Attak:
# *** Ethan Fisher,Patrick Bulbrook,
# *** Kaelan Croucher
class Cell:
    def __init__(self, render_root, loader):
        self.render_root = render_root
        self.loader = loader
        self.model = []
        self.color = (0, 0, 0, 0)
        self.empty = True

    def fill_cell(self, shape_string, pos):
        cube = self.loader.loadModel(shape_string)
        cube.setPos(pos)
        self.empty = False
        cube.reparentTo(self.render_root)
        self.model = cube

    def empty_cell(self):
        if self.model != []:
            self.model.removeNode()
            self.model = []
        self.empty = True
        self.color = (0, 0, 0, 0)

    def set_pos(self, pos):
        if self.model != []:
            self.model.setPos(pos)

    def is_empty(self):
        return self.empty
