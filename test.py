from math import ceil, cos, floor, radians, sin
import random
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath, Vec3, LColor, Point3

class Tetris(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.block_speed = 0.01

        self.count = 0

        self.score = 0 
        self.score_text = OnscreenText(text=f'Score: {self.score}', pos=(-0.9, 0.9), scale=0.1, mayChange=True)

        # Block Shapes
        self.block_shapes = {
            "line": [(0, 0), (1, 0), (2, 0)],  # 3x1 footprint
            "t_shape": [(0, 0), (1, 0), (2, 0), (1, 1)],  # T shape
            "l_shape": [(0, 0), (0, 1), (0, 2)],  # L shape
            "reverse_l": [(1, 0), (1, 1), (1, 2)],  # Reverse L shape
            "s_shape": [(0, 0), (1, 0), (1, 1)],  # S shape
            "z_shape": [(0, 0), (1, 0), (1, 1)],  # Z shape
        }

        # NEED TO IMPLEMENT A MOVING CAMERA
        self.disableMouse()
        # maybe add more camera presets 
        self.camera_positions = [
            (Point3(2.5, -20, 5), Point3(2.5, 2.5, 5)),  # Front view
            (Point3(2.5, 2.5, 40), Point3(2.5, 2.5, 0)),  # Top view
        ]

        self.current_view = 0
        self.set_camera_view(self.current_view)
        
        # Bind keys to switch scenes
        self.accept("1", self.switch_to_view, [0])
        self.accept("2", self.switch_to_view, [1])

        # Grid dimensions
        self.grid_width = 5
        self.grid_height = 15
        self.grid_depth = 5
        self.grid_size = 1  # Size of each grid cell

        # Initialize dictionary to track occupied positions
        self.block_positions = {}

        # Current block variables
        self.current_block_parts = []  # Track individual block parts
        self.current_block_type = None
        self.current_block_pos = Point3(1, 1, 9)  # Start near the top


        # Accept key inputs for moving and rotating the block
        self.accept("arrow_left", self.move_block, [-1, 0, 0])  # Move left
        self.accept("arrow_right", self.move_block, [1, 0, 0])  # Move right
        self.accept("arrow_up", self.move_block, [0, 1, 0])  # Move forward
        self.accept("arrow_down", self.move_block, [0, -1, 0])  # Move backward
        self.accept("q", self.rotate_x, [90])  # Rotate on X
        # self.accept("e", self.rotate_x, [-90])  # Rotate on X counter-clockwise
        self.accept("w", self.rotate_y, [90])  # Rotate on Y
        self.accept("e", self.rotate_z, [90])  # Rotate on Z
        self.accept("space", self.drop_block)  # Drop block faster
        # self.accept("r", self.respawn_block)  # Respawn block when 'R' is pressed, 

        # Draw the grid outline
        self.draw_grid_outline()

        # Create the initial block
        self.spawn_new_block()

        # Task to update game logic and block movement
        # THIS IS THE MAIN GAMELOOP 
        self.taskMgr.add(self.update_task, "updateTask")

    def set_camera_view(self, view_index):
        """Sets the camera position and orientation based on view index."""
        position, look_at = self.camera_positions[view_index]
        self.camera.setPos(position)
        self.camera.lookAt(look_at)
    
    def switch_to_view(self, view_index):
        """Switches to the specified camera view."""
        self.current_view = view_index
        self.set_camera_view(self.current_view)

    # Draw the 3D grid
    def draw_grid_outline(self):
        line_segs = LineSegs()
        line_segs.setColor(LColor(0.5, 0.5, 0.5, 1.0))
        line_segs.setThickness(0.5)

        for x in range(self.grid_width + 1):
            for y in range(self.grid_depth + 1):
                start = Vec3(x * self.grid_size, y * self.grid_size, 0)
                end = Vec3(x * self.grid_size, y * self.grid_size, self.grid_height * self.grid_size)
                line_segs.moveTo(start)
                line_segs.drawTo(end)

        for z in range(self.grid_height + 1):
            for x in range(self.grid_width + 1):
                line_segs.moveTo(Vec3(x * self.grid_size, 0, z * self.grid_size))
                line_segs.drawTo(Vec3(x * self.grid_size, self.grid_depth * self.grid_size, z * self.grid_size))
            for y in range(self.grid_depth + 1):
                line_segs.moveTo(Vec3(0, y * self.grid_size, z * self.grid_size))
                line_segs.drawTo(Vec3(self.grid_width * self.grid_size, y * self.grid_size, z * self.grid_size))

        grid_np = NodePath(line_segs.create())
        grid_np.reparentTo(self.render)

    def random_color(self):
            return (random.random(), random.random(), random.random(), 1)  # Random RGBA values

    # Spawns a new block at the top of the grid (1, 1, 9). Chooses a random block type, tracks individual parts
    def spawn_new_block(self):
        self.current_block_type = random.choice(list(self.block_shapes.keys()))  # Choose random block type
        self.current_block_pos = Point3(1, 1, 9)  # Reset position to top of the grid
        self.current_block_parts = []  # Clear previous block parts
        self.count += 1
        if self.count % 10 == 0:
            self.block_speed += 0.01

        # Generate a random color for the entire block
        block_color = self.random_color()

        # Create individual block parts based on the shape coordinates
        for x_offset, y_offset in self.block_shapes[self.current_block_type]:
            block_part = self.loader.loadModel("models/box")  # Replace with actual model path
            part_pos = self.current_block_pos + Point3(x_offset, y_offset, 0)
            block_part.setPos(part_pos)
            block_part.reparentTo(self.render)
            block_part.setColor(*block_color)  # Set the same color for all block parts
            self.current_block_parts.append((part_pos, block_part))  # Track each part's position and NodePath
            
    # # Calculating the center for rotation. 
    # def get_center(self):
    #     x_coords = [(pos.x) for pos, _ in self.current_block_parts]
    #     y_coords = [(pos.y) for pos, _ in self.current_block_parts]
    #     z_coords = [(pos.z) for pos, _ in self.current_block_parts]

    #     center_x = sum(x_coords) / len(self.current_block_parts)
    #     center_y = sum(y_coords) / len(self.current_block_parts)
    #     center_z = sum(z_coords) / len(self.current_block_parts)

    #     return Point3(center_x, center_y, center_z)

    # Checking if the position is valid for a specific movement, used in translation and rotations
    def is_position_valid(self, pos):
        if (pos.x < 0 or pos.x >= self.grid_width or
                pos.y < 0 or pos.y >= self.grid_depth or
                pos.z < 0 or pos.z >= self.grid_height):
            return False
        
        if (pos.x, pos.y, pos.z) in self.block_positions:
            return False
        
        return True

    # Constant rotation point, the second block
    def get_rotation_anchor(self):
        return self.current_block_parts[1][0]  # Return the position of the second block part
    
# ROTATIONS X, Y, Z
    def rotate_x(self, angle):
        anchor = self.get_rotation_anchor()
        new_positions = []

        for pos, block_part in self.current_block_parts:
            # Translate to the anchor
            translated_pos = Point3(pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)
            
            # Perform the rotation around the X axis
            new_y = translated_pos.y * cos(radians(angle)) - translated_pos.z * sin(radians(angle))
            new_z = translated_pos.y * sin(radians(angle)) + translated_pos.z * cos(radians(angle))
            
            # Translate back to the original anchor
            new_pos = Point3(translated_pos.x + anchor.x, new_y + anchor.y, new_z + anchor.z)
            new_positions.append(new_pos)

        # Check if all new positions are valid
        if all(self.is_position_valid(pos) for pos in new_positions):
            # Update the current block part position if valid
            for i, (pos, block_part) in enumerate(self.current_block_parts):
                self.current_block_parts[i] = (new_positions[i], block_part)
                block_part.setPos(new_positions[i])

    def rotate_y(self, angle):
        anchor = self.get_rotation_anchor()
        new_positions = []

        for pos, block_part in self.current_block_parts:
            # Translate to the anchor
            translated_pos = Point3(pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            # Perform the rotation around the Y axis
            new_x = translated_pos.x * cos(radians(angle)) + translated_pos.z * sin(radians(angle))
            new_z = -translated_pos.x * sin(radians(angle)) + translated_pos.z * cos(radians(angle))

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x, translated_pos.y + anchor.y, new_z + anchor.z)
            new_positions.append(new_pos)

        # Check if all new positions are valid
        if all(self.is_position_valid(pos) for pos in new_positions):
            # Update the current block part position if valid
            for i, (pos, block_part) in enumerate(self.current_block_parts):
                self.current_block_parts[i] = (new_positions[i], block_part)
                block_part.setPos(new_positions[i])

    def rotate_z(self, angle):
        anchor = self.get_rotation_anchor()
        new_positions = []

        for pos, block_part in self.current_block_parts:
            # Translate to the anchor
            translated_pos = Point3(pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            # Perform the rotation around the Z axis
            new_x = translated_pos.x * cos(radians(angle)) - translated_pos.y * sin(radians(angle))
            new_y = translated_pos.x * sin(radians(angle)) + translated_pos.y * cos(radians(angle))

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x, new_y + anchor.y, translated_pos.z + anchor.z)
            new_positions.append(new_pos)

        # Check if all new positions are valid
        if all(self.is_position_valid(pos) for pos in new_positions):
            # Update the current block part position if valid
            for i, (pos, block_part) in enumerate(self.current_block_parts):
                self.current_block_parts[i] = (new_positions[i], block_part)
                block_part.setPos(new_positions[i])


    # Translations 
    def move_block(self, x_offset, y_offset, z_offset):
        # Check new positions against the grid bounds and block positions
        new_positions = [Point3(pos.x + x_offset, pos.y + y_offset, pos.z + z_offset) for pos, _ in self.current_block_parts]

        if all(self.is_position_valid(pos) for pos in new_positions):
            self.current_block_pos += Point3(x_offset, y_offset, z_offset)
            for i, (pos, block_part) in enumerate(self.current_block_parts):
                new_pos = Point3(pos.x + x_offset, pos.y + y_offset, pos.z + z_offset)
                self.current_block_parts[i] = (new_pos, block_part)
                block_part.setPos(new_pos)

    # Main game loop, moving the block constantly, locking blocks
    def update_task(self, task):
        # Check if the block can move down
        can_move_down = all(self.is_position_valid(Point3(pos.x, pos.y, floor(pos.z - self.block_speed))) for pos, _ in self.current_block_parts)

        if can_move_down:
            # Automatically move the block down
            self.move_block(0, 0, -self.block_speed)
        else:
            # Lock the block in place if it can't move down anymore
            self.lock_block()

            # Additionally, check if any row is complete and clear it
            for i in range(self.grid_height):
                self.clear_complete_rows()

        return task.cont  # Continue the task
        
    # Clears complete x or y rows, then shifts above blocks down
    # CANT CLEAR MULTIPLE ROWS AT ONCE
    def clear_complete_rows(self):
        for z in range(self.grid_height):  # Check each depth level
            rows_to_clear_x = {
                y for y in range(self.grid_depth)
                if all((x, y, z) in self.block_positions for x in range(self.grid_width))
            }
            
            rows_to_clear_y = {
                x for x in range(self.grid_width)
                if all((x, y, z) in self.block_positions for y in range(self.grid_depth))
            }

            # Clear all blocks in the complete rows along the x-axis
            for y in rows_to_clear_x:
                for x in range(self.grid_width):
                    block = self.block_positions.pop((x, y, z), None)
                    if block:
                        block.removeNode()  # Remove the block from the scene
                        self.update_score()

            # Clear all blocks in the complete columns along the y-axis
            for x in rows_to_clear_y:
                for y in range(self.grid_depth):
                    block = self.block_positions.pop((x, y, z), None)
                    if block:
                        block.removeNode()  # Remove the block from the scene
                        self.update_score()

            for x in sorted(rows_to_clear_y):
                for y in range(self.grid_depth):  # For each y in the cleared column
                    # Clear blocks in the cleared column at depth z
                    block = self.block_positions.pop((x, y, z), None)
                    if block:
                        block.removeNode()  # Remove the block from the scene
                        self.update_score()
                        

                # Shift all blocks down in the column at x, filling all empty positions
                for current_z in range(z + 1, self.grid_height):
                    for y in range(self.grid_depth):
                        pos = (x, y, current_z)
                        if pos in self.block_positions:
                            block = self.block_positions.pop(pos)
                            # Calculate the new position by moving down to fill empty spaces
                            new_z = current_z - 1
                            while (x, y, new_z) not in self.block_positions and new_z >= 0:
                                new_z -= 1
                            new_z += 1  # Move back to the first available position
                            self.block_positions[(x, y, new_z)] = block
                            block.setPos(x, y, new_z)

            for y in sorted(rows_to_clear_x):
                for x in range(self.grid_width):  # For each x in the cleared row
                    # Clear blocks in the cleared row at depth z
                    block = self.block_positions.pop((x, y, z), None)
                    if block:
                        block.removeNode()  # Remove the block from the scene

                # Shift all blocks down in the row at y, filling all empty positions
                for current_z in range(z + 1, self.grid_height):
                    for x in range(self.grid_width):
                        pos = (x, y, current_z)
                        if pos in self.block_positions:
                            block = self.block_positions.pop(pos)
                            # Calculate the new position by moving down to fill empty spaces
                            new_z = current_z - 1
                            while (x, y, new_z) not in self.block_positions and new_z >= 0:
                                new_z -= 1
                            new_z += 1  # Move back to the first available position
                            self.block_positions[(x, y, new_z)] = block
                            block.setPos(x, y, new_z)

    # Moves the block down 1 z level
    def drop_block(self):
        can_move_down = all(self.is_position_valid(Point3(pos.x, pos.y, floor(pos.z - 1))) for pos, _ in self.current_block_parts)
        if can_move_down:
            self.move_block(0, 0, -1)  # Move down until it can't anymore

    # Locks the block in place, then spawns a new block
    def lock_block(self):
        """Locks the current block in place and spawns a new block."""
        for pos, block_part in self.current_block_parts:
            # Round position coordinates to avoid floating-point precision issues
            rounded_pos = (round(pos.x), round(pos.y), round(pos.z))
            self.block_positions[rounded_pos] = block_part  # Save block position

        self.spawn_new_block()  # Spawn a new block

    # Repsawn the block, debugging function not part of the game currently
    def respawn_block(self):
        """Respawns the current block to the starting position."""
        self.current_block_parts.clear()  # Clear current parts
        self.spawn_new_block()  # Spawn a new block

    def update_score(self):
        self.score += 100
        self.score_text.setText(f'Score: {self.score}')

# Initialize the game 
app = Tetris()
app.run()