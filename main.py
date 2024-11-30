from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Point3, DirectionalLight, AmbientLight

from gamelogic.well import Well
from gamelogic.bag import Bag
from gamelogic.constants import GRID
from gamelogic.constants import PIECES
from gamelogic.constants import SPAWN


class Tetris(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.grid_width = GRID["Width"]
        self.grid_height = GRID["Height"]
        self.grid_depth = GRID["Depth"]
        self.pieces = PIECES.values()
        self.spawn = SPAWN

        self.drop_speed = 1.0
        self.count = 11

# ******** Setup Bag
        # Works!
        self.piece_bag = Bag(self.pieces, self.spawn, self.render, self.loader)

        self.current_piece = self.piece_bag.pop_next_piece()

        self.mainLight = DirectionalLight('main light')
        self.mainLightNodePath = self.render.attachNewNode(self.mainLight)
        self.mainLightNodePath.setHpr(30, -60, 0)
        self.render.setLight(self.mainLightNodePath)

        self.ambientLight = AmbientLight('ambient light')
        self.ambientLight.setColor((0.5, 0.5, 0.5, 1))
        self.ambientLightNodePath = self.render.attachNewNode(
            self.ambientLight)
        self.render.setLight(self.ambientLightNodePath)

# ********************* Render Tetris Grid
        self.tetris_grid = Well(
            self.render,
            self.loader,
            self.grid_width,
            self.grid_depth,
            self.grid_height)

        # Task to update game logic and block movement
        # THIS IS THE MAIN GAMELOOP
        self.taskMgr.add(self.update_task, "updateTask")
        self.taskMgr.doMethodLater(self.drop_speed, self.auto_drop_piece, "dropPiece")


# ************ Sky Box Definition
        # Load the skybox model
        # Empty model as a base for the skybox
        self.skybox = self.loader.loadModel("models/box")
        self.skybox.reparentTo(self.render)
        self.skybox.setTwoSided(True)  # Render textures on both sides

        # Load the textures for each face of the skybox
        self.front = self.loader.loadTexture("skybox/sky.jpg")
        self.back = self.loader.loadTexture("skybox/sky.jpg")
        self.left = self.loader.loadTexture("skybox/sky.jpg")
        self.right = self.loader.loadTexture("skybox/sky.jpg")
        self.up = self.loader.loadTexture("skybox/sky.jpg")
        self.down = self.loader.loadTexture("skybox/sky.jpg")

        # Apply the textures to the faces
        self.skybox.setTexture(self.front, 0)  # front texture
        self.skybox.setTexture(self.back, 1)   # back texture
        self.skybox.setTexture(self.left, 2)   # left texture
        self.skybox.setTexture(self.right, 3)  # right texture
        self.skybox.setTexture(self.up, 4)     # up texture
        self.skybox.setTexture(self.down, 5)   # down texture

        # Scale and position the skybox
        self.skybox.setScale(100)  # Set size
        self.skybox.setPos(-50, -50, -50)  # Position in the center

# *********** Good above this line *********
# ***** Score Board Logic ******
        self.score = 0
        self.score_text = OnscreenText(
            text=f'Score: {self.score}', pos=(-0.9, 0.9), scale=0.1, fg=(1,1,1,1), mayChange=True)

# ****************** Camera Definitions

        # NEED TO IMPLEMENT A MOVING CAMERA
        self.disableMouse()
        # maybe add more camera presets
        self.camera_positions = [
            (Point3(2.5, -40, 6), Point3(2.5, 100, 6)),  # Front view
            (Point3(-20, -20, 35), Point3(2.5, 2.5, 3)),
            (Point3(2.5, 2.5, 35), Point3(2.5, 2.5, 0)),  # Top view
        ]

        self.current_view = 0
        self.set_camera_view(self.current_view)

        # Bind keys to switch scenes
        self.accept("1", self.switch_to_view, [0])
        self.accept("2", self.switch_to_view, [1])
        self.accept("3", self.switch_to_view, [2])


# ******************************** Movement / KeyBinds

        # Accept key inputs for moving and rotating the block
        self.accept("arrow_left", self.move_piece, [-1, 0, 0])  # Move left
        self.accept("arrow_right", self.move_piece, [1, 0, 0])  # Move right
        self.accept("arrow_up", self.move_piece, [0, 1, 0])  # Move forward
        self.accept("arrow_down", self.move_piece, [0, -1, 0])  # Move backward
        self.accept("q", self.rotate_piece, ['x'])  # Rotate on X
        self.accept("w", self.rotate_piece, ['y'])  # Rotate on Y
        self.accept("e", self.rotate_piece, ['z'])  # Rotate on Z
        self.accept("d", self.full_drop, [])
        self.accept("space", self.move_piece, [0, 0, -1])  # Drop block faster

        # ******* render bag from peice
        self.current_piece.render_piece()

    def move_piece(self, x, y, z):
        new_pos = self.current_piece.move_piece(x, y, z)
        if self.tetris_grid.validate_position(new_pos):
            self.current_piece.set_position(new_pos)
            return True
        return False

    def rotate_piece(self, dir):
        if dir == 'x':
            new_pos = self.current_piece.rotate_x()
        elif dir == 'y':
            new_pos = self.current_piece.rotate_y()
        else:
            new_pos = self.current_piece.rotate_z()
        if self.tetris_grid.validate_position(new_pos):
            self.current_piece.set_position(new_pos)

    def full_drop(self):
        can_move = self.move_piece(0, 0, -1)
        while can_move:
            can_move = self.move_piece(0, 0, -1)

    def set_camera_view(self, view_index):
        position, look_at = self.camera_positions[view_index]
        self.camera.setPos(position)
        self.camera.lookAt(look_at)

    def switch_to_view(self, view_index):
        self.current_view = view_index
        self.set_camera_view(self.current_view)

    def auto_drop_piece(self, task):
        if self.count % 10 == 0 and self.count < 500:
            self.drop_speed -= 0.01
            self.update_drop_speed(self.drop_speed)
        self.count += 1

        next_drop_pos = self.current_piece.move_piece(0, 0, -1)
        if self.tetris_grid.validate_position(next_drop_pos):
            self.current_piece.set_position(next_drop_pos)
        else:
            self.tetris_grid.place_piece(self.current_piece)
            self.current_piece.remove_piece()
            self.current_piece = self.piece_bag.pop_next_piece()
            self.current_piece.render_piece()

        return task.again

    # Main game loop, moving the block constantly, locking blocks
    def update_drop_speed(self, new_speed):
        self.taskMgr.remove("dropPiece")  # Remove the old task
        self.taskMgr.doMethodLater(new_speed, self.auto_drop_piece, "dropPiece")
        
    def update_task(self, task):
        score_multiple = self.tetris_grid.check_row()
        print(self.drop_speed)
        if score_multiple == -1:
            print("Game Over!")
            self.taskMgr.stop()
        self.update_score(score_multiple)
        return task.cont  # Continue the task

    def update_score(self, rows):
        self.score += rows * 100
        if rows > 0:
            self.score_text.setText(f'Score: {self.score}')


# Initialize the game
app = Tetris()
app.run()
