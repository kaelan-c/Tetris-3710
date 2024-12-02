# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, Point3

from gamelogic.bag import Bag
from gamelogic.constants import GRID, PIECES, SPAWN
from gamelogic.grid import Grid


# The Tetris class is the main entry point to the program,
# Responsible for setting up the game environment, rendering,
# and controlling the main game loop.
class Tetris(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Render Skybox
        self.skybox = self.loader.loadModel("models/box")
        self.skybox.reparentTo(self.render)
        self.skybox.setTwoSided(True)  # Render textures on both sides

        # Load the textures for each face of the skybox
        self.front = self.loader.loadTexture("assets/skybox/sky.jpg")
        self.back = self.loader.loadTexture("assets/skybox/sky.jpg")
        self.left = self.loader.loadTexture("assets/skybox/sky.jpg")
        self.right = self.loader.loadTexture("assets/skybox/sky.jpg")
        self.up = self.loader.loadTexture("assets/skybox/sky.jpg")
        self.down = self.loader.loadTexture("assets/skybox/sky.jpg")

        # Apply the textures to the faces
        self.skybox.setTexture(self.front, 0)  # front texture
        self.skybox.setTexture(self.back, 1)  # back texture
        self.skybox.setTexture(self.left, 2)  # left texture
        self.skybox.setTexture(self.right, 3)  # right texture
        self.skybox.setTexture(self.up, 4)  # up texture
        self.skybox.setTexture(self.down, 5)  # down texture

        # Scale and position the skybox
        self.skybox.setScale(100)  # Set size
        self.skybox.setPos(-50, -50, -50)  # Position in the center

        # Render lighting
        self.mainLight = DirectionalLight("main light")
        self.mainLightNodePath = self.render.attachNewNode(self.mainLight)
        self.mainLightNodePath.setHpr(30, -60, 0)
        self.render.setLight(self.mainLightNodePath)

        self.ambientLight = AmbientLight("ambient light")
        self.ambientLight.setColor((0.5, 0.5, 0.5, 1))
        self.ambientLightNodePath = self.render.attachNewNode(
            self.ambientLight)
        self.render.setLight(self.ambientLightNodePath)

        # Initialize and render tetris grid
        self.tetris_grid = Grid(GRID["Width"], GRID["Depth"], GRID["Height"])
        self.tetris_grid.render_grid(self.render)

        # load tetris cube models into peices list
        for p in PIECES.values():
            p["model"] = self.loader.loadModel(p["model"])

        # Initialize pieces
        self.piece_bag = Bag(PIECES.values(), SPAWN)
        # Take first piece from bag and render it
        self.current_piece = self.piece_bag.pop_next_piece()
        self.current_piece.render_piece(self.render)

        # Set drop speed and timer for speed increase
        self.drop_speed = 1.0
        self.count = 11

        # Main game loop task
        self.taskMgr.add(self.update_task, "updateTask")
        # Task that drops block, increasing speed by ever 11 seconds
        self.taskMgr.doMethodLater(
            self.drop_speed, self.auto_drop_piece, "dropPiece")

        # Initialize score board to 0
        self.score = 0
        self.score_text = OnscreenText(
            text=f"Score: {self.score}",
            pos=(-0.9, 0.9),
            scale=0.1,
            fg=(1, 1, 1, 1),
            mayChange=True,
        )

        # Disable mouse and set camera positions
        self.disableMouse()
        # Values are assuming 8 x 8 x 24 grid
        self.camera_positions = [
            (Point3(-24, -24, 36), Point3(12, 12, 0)),  # Side Isometric View
            (Point3(3, 3, 36), Point3(3, 3, 0)),  # Top view
        ]

        # Set camera view to isometric view first
        self.current_view = 0
        self.set_camera_view(self.current_view)

        # Bind keys for camera, and block movement
        self.accept("1", self.switch_to_view, [0])
        self.accept("2", self.switch_to_view, [1])

        self.accept("arrow_left", self.move_piece, [-1, 0, 0])  # Move left
        self.accept("arrow_right", self.move_piece, [1, 0, 0])  # Move right
        self.accept("arrow_up", self.move_piece, [0, 1, 0])  # Move forward
        self.accept("arrow_down", self.move_piece, [0, -1, 0])  # Move backward
        self.accept("q", self.rotate_piece, ["x"])  # Rotate on X
        self.accept("w", self.rotate_piece, ["y"])  # Rotate on Y
        self.accept("e", self.rotate_piece, ["z"])  # Rotate on Z
        self.accept("d", self.full_drop, [])
        self.accept("space", self.move_piece, [0, 0, -1])  # Drop block faster

    # Input handler for movement, validates posisiton then applies it
    # if valid
    def move_piece(self, x, y, z):
        new_pos = self.current_piece.move_piece(x, y, z)
        if self.tetris_grid.validate_position(new_pos):
            self.current_piece.set_position(new_pos)
            return True
        return False

    # Input handler for rotation, validates posisiton then applies it
    # if valid
    def rotate_piece(self, dir):
        if dir == "x":
            new_pos = self.current_piece.rotate_x()
        elif dir == "y":
            new_pos = self.current_piece.rotate_y()
        else:
            new_pos = self.current_piece.rotate_z()
        if self.tetris_grid.validate_position(new_pos):
            self.current_piece.set_position(new_pos)

    # Full drop, moves piece to lowet valid location
    def full_drop(self):
        can_move = self.move_piece(0, 0, -1)
        while can_move:
            can_move = self.move_piece(0, 0, -1)

    # Handlers for setting and switching cameras
    def set_camera_view(self, view_index):
        position, look_at = self.camera_positions[view_index]
        self.camera.setPos(position)
        self.camera.lookAt(look_at)

    def switch_to_view(self, view_index):
        self.current_view = view_index
        self.set_camera_view(self.current_view)

    # task to auto drop piece on a decreasing interval
    def auto_drop_piece(self, task):
        if self.count % 10 == 0 and self.count < 500:
            self.drop_speed -= 0.01
            self.update_drop_speed(self.drop_speed)
        self.count += 1

        next_drop_pos = self.current_piece.move_piece(0, 0, -1)
        if self.tetris_grid.validate_position(next_drop_pos):
            self.current_piece.set_position(next_drop_pos)
        else:
            self.tetris_grid.place_piece(self.current_piece, self.render)
            self.current_piece.remove_piece()
            self.current_piece = self.piece_bag.pop_next_piece()
            self.current_piece.render_piece(self.render)

        return task.again

    # Function to increase rate of block dropping
    def update_drop_speed(self, new_speed):
        self.taskMgr.remove("dropPiece")  # Remove the old task
        self.taskMgr.doMethodLater(
            new_speed, self.auto_drop_piece, "dropPiece")

    # Main game loop, every loop, checks grid and updates score.
    # if check_row returns 0, game over state is triggered
    def update_task(self, task):
        score_multiple = self.tetris_grid.check_row(self.render)
        if score_multiple == -1:
            print("Game Over!")
            self.taskMgr.stop()
        self.update_score(score_multiple)
        return task.cont  # Continue the task

    # Simple function to update score by + 100 * number of rows cleared
    def update_score(self, rows):
        self.score += rows * 100
        if rows > 0:
            self.score_text.setText(f"Score: {self.score}")


# Initialize the game
app = Tetris()
app.run()
