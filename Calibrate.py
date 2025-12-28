import Functions

# Calibrate movement directions
def calibrate_directions():
	DIRS = [North, East, South, West]
	DX = [0, 0, 0, 0]
	DY = [0, 0, 0, 0]
	Functions.moveto((get_world_size() // 2), (get_world_size() // 2))

	i = 0
	while i < 4:
		d = DIRS[i]

		# Only test directions we can move into
		px0 = get_pos_x()
		py0 = get_pos_y()

		if can_move(d):
			moved = move(d)
			if moved:
				px1 = get_pos_x()
				py1 = get_pos_y()

				DX[i] = px1 - px0
				DY[i] = py1 - py0

				# move back
				bx = px0
				by = py0

				# compute opposite
				if px1 > px0 and can_move(West):
					move(West)
				elif px1 < px0 and can_move(East):
					move(East)
				elif py1 > py0 and can_move(South):
					move(South)
				elif py1 < py0 and can_move(North):
					move(North)

		i = i + 1
	Functions.moveto(0, 0)
	return DX, DY

