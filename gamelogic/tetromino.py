#  TODO: Need to implement logic for 2d rotate, according to srs
from math import cos, sin, radians
from panda3d.core import Point3


class Tetromino:
    def __init__(self, name, shape, spawn, color, render_root, loader):
        self.name = name
        self.shape = shape
        self.position = Point3(spawn)
        self.color = color
        self.loader = loader
        self.model = []
        self.render_root = render_root

    def render_piece(self):
        for x, y in self.shape:
            cube = self.loader.loadModel("Tetronimos/SingleCube.glb")
            pos = self.position + Point3(x, y, 0)
            cube.setPos(pos)
            cube.reparentTo(self.render_root)
            cube.setColor(self.color)

            self.model.append((pos, cube))

    def rotate_x(self):
        angle = 90
        anchor = self.get_rotation_anchor()
        new_position = []
        cos_angle = cos(radians(angle))
        sin_angle = sin(radians(angle))

        for pos, cube in self.model:
            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            new_y = (rot_pos.y * cos_angle) - (rot_pos.z * sin_angle)
            new_z = (rot_pos.y * sin_angle) + (rot_pos.z * cos_angle)
            new_pos = Point3(rot_pos.x + anchor.x,
                             new_y + anchor.y, new_z + anchor.z)
            new_position.append(new_pos)

        return new_position

    def rotate_y(self):
        angle = 90
        anchor = self.get_rotation_anchor()
        new_position = []
        cos_angle = cos(radians(angle))
        sin_angle = sin(radians(angle))

        for pos, cube in self.model:
            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)
            # Perform the rotation around the Y axis
            new_x = (rot_pos.x * cos_angle) + (rot_pos.z * sin_angle)
            new_z = (-rot_pos.x * sin_angle) + (rot_pos.z * cos_angle)

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x,
                             rot_pos.y + anchor.y, new_z + anchor.z)
            new_position.append(new_pos)
        return new_position

    def rotate_z(self):
        angle = 90
        anchor = self.get_rotation_anchor()
        new_position = []
        cos_angle = cos(radians(angle))
        sin_angle = sin(radians(angle))

        for pos, cube in self.model:
            # Translate to the anchor
            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            # Perform the rotation around the Z axis
            new_x = (rot_pos.x * cos_angle) - (rot_pos.y * sin_angle)
            new_y = (rot_pos.x * sin_angle) + (rot_pos.y * cos_angle)

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x, new_y +
                             anchor.y, rot_pos.z + anchor.z)
            new_position.append(new_pos)

        return new_position

    def move_piece(self, x, y, z):
        # Check new positions against the grid bounds and block positions
        new_position = []
        for pos, _ in self.model:
            new_position.append(Point3(pos.x + x, pos.y + y, pos.z + z))

        return new_position

    def set_position(self, new_pos):
        for i, (pos, cube) in enumerate(self.model):
            cube.setPos(new_pos[i])
            self.model[i] = (new_pos[i], cube)

    def remove_piece(self):
        for pos, cube in self.model:
            cube.removeNode()

    def drop_peice(self):
        print("drop ")

    def get_shape(self):
        print(self.name)
        return self.shape

    def get_coords(self):
        return self.position

    def get_rotation_anchor(self):
        return self.model[1][0]
