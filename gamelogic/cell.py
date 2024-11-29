class Cell:
    def __init__(self, render_root, loader):
        self.render_root = render_root
        self.loader = loader
        self.color = (0, 0, 0, 0)
        self.model = []
        self.empty = True

    def fill_cell(self, shape_string, pos):
        cube = self.loader.loadModel(shape_string)
        cube.setPos(pos)
        self.empty = False
        cube.reparentTo(self.render_root)
        self.model = cube

    def empty_cell(self):
        self.model.removeNode()
        self.model = []
        self.empty = True
        self.color = (0, 0, 0, 0)

    def is_empty(self):
        return self.empty

    def get_color(self):
        return self.color
