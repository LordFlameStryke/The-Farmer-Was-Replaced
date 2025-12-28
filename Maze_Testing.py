clear()
import Maze
import Calibrate
DX, DY = Calibrate.calibrate_directions()
Maze.generate_maze(num_items(Items.Weird_Substance), DX, DY)