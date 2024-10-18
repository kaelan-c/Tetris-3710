#  TODO: Need to implement logic for 2d rotate, according to srs

class Tetromino:
    def __init__(self, name, shape2d, offset, colour):
        self.name = name
        self.shape = shape2d
        self.spawn_offset = offset,
        self.colour = colour
        self.active = False  # Flag for if piece is active

    def rotate2d(self, direction):
        print("Rotated by dir: ", direction)

    def get_shape2d(self):
        print(self.name)
        return self.shape

    def get_position2d(self):
        return self.position

    def move2d(self, x, y):
        self.position[0] += x
        self.position[1] += y
