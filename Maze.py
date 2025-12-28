import Functions

#Run Maze code
def run_astar_maze(substance, DX, DY):
	# =========================================
	# Direction setup
	# =========================================

	moves_done = 0

	DIR_N = 0
	DIR_E = 1
	DIR_S = 2
	DIR_W = 3
	DIR_ORDER = [DIR_N, DIR_E, DIR_S, DIR_W]

	def DIR_CONSTANT(d):
		if d == DIR_N:
			return North
		if d == DIR_E:
			return East
		if d == DIR_S:
			return South
		if d == DIR_W:
			return West
		return North

	def opposite_dir(d):
		if d == DIR_N:
			return DIR_S
		if d == DIR_E:
			return DIR_W
		if d == DIR_S:
			return DIR_N
		if d == DIR_W:
			return DIR_E
		return DIR_N

	def pos():
		return get_pos_x(), get_pos_y()

	# =========================================
	# Global grid structures
	# =========================================

	world_size = get_world_size()

	# visited[x][y] = True if tile discovered
	visited = []
	# neighbors_x[x][y] / neighbors_y[x][y] store lists of neighbor coordinates
	neighbors_x = []
	neighbors_y = []

	x = 0
	while x < world_size:
		row_v = []
		row_nx = []
		row_ny = []
		y = 0
		while y < world_size:
			row_v.append(False)
			row_nx.append([])  # list of neighbor x coords
			row_ny.append([])  # list of neighbor y coords
			y = y + 1
		visited.append(row_v)
		neighbors_x.append(row_nx)
		neighbors_y.append(row_ny)
		x = x + 1

	# =========================================
	# Helpers for adjacency recording
	# =========================================

	def add_edge(ax, ay, bx, by):
		# add bx,by to neighbors of ax,ay if not already there
		i = 0
		found = False
		while i < len(neighbors_x[ax][ay]):
			if neighbors_x[ax][ay][i] == bx and neighbors_y[ax][ay][i] == by:
				found = True
				break
			i = i + 1
		if not found:
			neighbors_x[ax][ay].append(bx)
			neighbors_y[ax][ay].append(by)

		# and add reverse edge
		i = 0
		found2 = False
		while i < len(neighbors_x[bx][by]):
			if neighbors_x[bx][by][i] == ax and neighbors_y[bx][by][i] == ay:
				found2 = True
				break
			i = i + 1
		if not found2:
			neighbors_x[bx][by].append(ax)
			neighbors_y[bx][by].append(ay)

	# =========================================
	# Move helper
	# =========================================

	MOVE_RETRY = 2

	def safe_move(d):
		# Try moving a few times to avoid transient failure
		attempt = 0
		while attempt < MOVE_RETRY:
			if move(DIR_CONSTANT(d)):
				return True
			attempt = attempt + 1
		return False

	def move_toward_origin():
		# Very simple greedy return to (0,0)
		while True:
			x0 = get_pos_x()
			y0 = get_pos_y()
			if x0 == 0 and y0 == 0:
				return

			moved = False

			if x0 > 0:
				if can_move(West):
					if move(West):
						moved = True
			elif x0 < 0:
				if can_move(East):
					if move(East):
						moved = True

			if moved:
				continue

			if y0 > 0:
				if can_move(South):
					if move(South):
						moved = True
			elif y0 < 0:
				if can_move(North):
					if move(North):
						moved = True

			if not moved:
				return

	# =========================================
	# DFS Maze Mapping (movement-based)
	# =========================================

	def reset_mapping():
		x = 0
		while x < world_size:
			y = 0
			while y < world_size:
				visited[x][y] = False
				neighbors_x[x][y] = []
				neighbors_y[x][y] = []
				y = y + 1
			x = x + 1

	def dfs_map():
		global moves_done
		global DX
		global DY
		cx, cy = pos()
		if get_entity_type() == Entities.Treasure:
			# Found treasure during mapping; use Weird Substance
			moves_done = moves_done + 1
			if moves_done < 300:
				use_item(Items.Weird_Substance, substance)

		visited[cx][cy] = True

		i = 0
		while i < 4:
			d = DIR_ORDER[i]
			dir_const = DIR_CONSTANT(d)
												
			if can_move(dir_const) and not visited[(cx + DX[d])][cy + DY[d]]:
				# attempt move
				if move(dir_const):

					if get_entity_type() == Entities.Treasure:
						# Found treasure during mapping; use Weird Substance
						moves_done = moves_done + 1
						if moves_done < 300:
							use_item(Items.Weird_Substance, substance)


					nx, ny = pos()
					add_edge(cx, cy, nx, ny)

					if not visited[nx][ny]:
						dfs_map()

					# backtrack
					back_dir = DIR_CONSTANT(opposite_dir(d))
					move(back_dir)

					if get_entity_type() == Entities.Treasure:
						# Found treasure during mapping; use Weird Substance
						moves_done = moves_done + 1
						if moves_done < 300:
							use_item(Items.Weird_Substance, substance)


					# after this, we should be back at cx,cy
			i = i + 1

	def map_entire_maze():
		reset_mapping()
		move_toward_origin()
		dfs_map()
		return

	# =========================================
	# A* Solver using adjacency lists
	# =========================================

	def manhattan(ax, ay, bx, by):
		dx = ax - bx
		if dx < 0:
			dx = 0 - dx
		dy = ay - by
		if dy < 0:
			dy = 0 - dy
		return dx + dy

	def astar_path(sx, sy, gx, gy):
		# gscore, came_from
		gscore = []
		came_x = []
		came_y = []

		x = 0
		while x < world_size:
			row_g = []
			row_px = []
			row_py = []
			y = 0
			while y < world_size:
				row_g.append(999999)
				row_px.append(-1)
				row_py.append(-1)
				y = y + 1
			gscore.append(row_g)
			came_x.append(row_px)
			came_y.append(row_py)
			x = x + 1

		open_x = []
		open_y = []
		open_f = []
		open_g = []

		gscore[sx][sy] = 0
		h0 = manhattan(sx, sy, gx, gy)
		open_x.append(sx)
		open_y.append(sy)
		open_f.append(h0)
		open_g.append(0)

		while len(open_x) > 0:
			# pick best f
			best = 0
			i = 1
			while i < len(open_x):
				if open_f[i] < open_f[best]:
					best = i
				i = i + 1

			cx = open_x.pop(best)
			cy = open_y.pop(best)
			cf = open_f.pop(best)
			cg = open_g.pop(best)

			if cx == gx and cy == gy:
				# reconstruct path as list of (x,y)
				path = []
				x0 = cx
				y0 = cy
				while not (x0 == sx and y0 == sy):
					path.append((x0, y0))
					px = came_x[x0][y0]
					py = came_y[x0][y0]
					x0 = px
					y0 = py
				path.append((sx, sy))
				# reverse
				rev = []
				j = len(path) - 1
				while j >= 0:
					rev.append(path[j])
					j = j - 1
				return rev

			# explore neighbors from adjacency
			k = 0
			while k < len(neighbors_x[cx][cy]):
				nx = neighbors_x[cx][cy][k]
				ny = neighbors_y[cx][cy][k]

				if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
					tentative_g = cg + 1
					if tentative_g < gscore[nx][ny]:
						gscore[nx][ny] = tentative_g
						h1 = manhattan(nx, ny, gx, gy)
						f1 = tentative_g + h1
						open_x.append(nx)
						open_y.append(ny)
						open_f.append(f1)
						open_g.append(tentative_g)
						came_x[nx][ny] = cx
						came_y[nx][ny] = cy
				k = k + 1

		return []

	# =========================================
	# Follow path by coordinates
	# =========================================

	def follow_path(path):
		i = 1
		while i < len(path):
			cx, cy = pos()

			# ============================================
			# 1. OPTIONAL DYNAMIC MAP UPDATE (non-intrusive)
			# ============================================
			# Check all 4 directions for newly opened corridors
			dcheck = 0
			while dcheck < 4:
				dtest = DIR_ORDER[dcheck]
				dir_const = DIR_CONSTANT(dtest)

				# If we previously thought this edge was blocked (no adjacency),
				# but now can_move says it's open, add it.
				if can_move(dir_const):
					# compute neighbor coords safely
					nx = cx
					ny = cy
					if dtest == DIR_N:
						ny = ny + 1
					elif dtest == DIR_E:
						nx = nx + 1
					elif dtest == DIR_S:
						ny = ny - 1
					elif dtest == DIR_W:
						nx = nx - 1

					# verify within bounds
					if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
						# check if this adjacency already exists
						exists = False
						j = 0
						while j < len(neighbors_x[cx][cy]):
							if neighbors_x[cx][cy][j] == nx and neighbors_y[cx][cy][j] == ny:
								exists = True
								break
							j = j + 1

						if not exists:
							# found a new open path: add adjacency
							neighbors_x[cx][cy].append(nx)
							neighbors_y[cx][cy].append(ny)

							# add reverse edge
							neighbors_x[nx][ny].append(cx)
							neighbors_y[nx][ny].append(cy)

				dcheck = dcheck + 1



			nx = path[i][0]
			ny = path[i][1]

			dx = nx - cx
			dy = ny - cy

			d = -1

			if dx == 0 and dy == 1:
				d = DIR_N
			elif dx == 1 and dy == 0:
				d = DIR_E
			elif dx == 0 and dy == -1:
				d = DIR_S
			elif dx == -1 and dy == 0:
				d = DIR_W
			else:
				# path step is not adjacent or position desynced
				return False

			if not safe_move(d):
				return False

			i = i + 1

		return True

	def return_to_origin():
		sx, sy = pos()
		if sx == 0 and sy == 0:
			return True
		path = astar_path(sx, sy, 0, 0)
		if len(path) == 0:
			return False
		return follow_path(path)

	# =========================================
	# Treasure cycle: 300 uses, harvest, exit
	# =========================================

	def run_treasure_cycle(substance):
		# Map once at the start
		map_entire_maze()

		global moves_done
		while moves_done < 300:
			tx, ty = measure()
			sx, sy = pos()

			path = astar_path(sx, sy, tx, ty)
			if len(path) == 0:
				# mapping might be off; rebuild and retry
				map_entire_maze()
				continue

			ok = follow_path(path)
			if not ok:
				# got blocked somehow; remap and retry
				map_entire_maze()
				continue

			# we’re at treasure, use Weird Substance
			moves_done = moves_done + 1
			if moves_done < 300:
				use_item(Items.Weird_Substance, substance)

		# after 300 fertilizations, harvest and go home, then exit
		harvest()
		Functions.moveto(0, 0)
	run_treasure_cycle(substance)
	return True

def generate_maze(substance, DX, DY):
	Functions.moveto(0, 0)
	s = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	if s > substance:
		return False
	plant(Entities.Bush)
	use_item(Items.Fertilizer)
	while not can_harvest():
		pass
	use_item(Items.Weird_Substance, s)
	run_astar_maze(s, DX, DY)