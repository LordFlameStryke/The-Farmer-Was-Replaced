import Functions

#Dinosaur A*
def dino_a_star(DX, DY, mode="Ham"):
	# =========================================
	# Shared direction + utility
	# =========================================

	DIR_N = 0
	DIR_E = 1
	DIR_S = 2
	DIR_W = 3

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

	def pos():
		return get_pos_x(), get_pos_y()

	def my_abs(v):
		if v < 0:
			return 0 - v
		return v

	world_size = get_world_size()

	# =========================================
	# =========  DINO AI MODE (SMART)  =========
	# =========================================

	# Full body state for AI mode
	snake_body_x = []
	snake_body_y = []
	snake_len = 0
	apples_eaten = 0

	def init_snake_state():
		global snake_len
		global apples_eaten
		global snake_body_x
		global snake_body_y

		cx = get_pos_x()
		cy = get_pos_y()

		snake_body_x = []
		snake_body_y = []

		snake_body_x.append(cx)
		snake_body_y.append(cy)

		apples_eaten = 0
		snake_len = 1

	def is_body(x, y):
		i = 0
		while i < len(snake_body_x):
			if snake_body_x[i] == x and snake_body_y[i] == y:
				return True
			i = i + 1
		return False

	def get_tail():
		if len(snake_body_x) == 0:
			return get_pos_x(), get_pos_y()
		return snake_body_x[0], snake_body_y[0]

	MOVE_RETRY = 2

	def safe_move_and_update(d, apple_x, apple_y):
		global snake_len
		global apples_eaten
		global snake_body_x
		global snake_body_y

		attempt = 0
		while attempt < MOVE_RETRY:
			if move(DIR_CONSTANT(d)):
				cx, cy = pos()

				if cx == apple_x and cy == apple_y:
					apples_eaten = apples_eaten + 1

				snake_len = apples_eaten + 1

				snake_body_x.append(cx)
				snake_body_y.append(cy)

				while len(snake_body_x) > snake_len:
					snake_body_x.pop(0)
					snake_body_y.pop(0)

				return True
			attempt = attempt + 1

		return False

	def no_legal_moves():
		cx, cy = pos()
		d = 0
		while d < 4:
			nx = cx + DX[d]
			ny = cy + DY[d]
			if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
				if not is_body(nx, ny) and can_move(DIR_CONSTANT(d)):
					return False
			d = d + 1
		return True

	def find_path_bfs(sx, sy, gx, gy, allow_tail):
		qx = []
		qy = []
		head = 0

		visited = []
		parent_x = []
		parent_y = []

		x = 0
		while x < world_size:
			row_v = []
			row_px = []
			row_py = []
			y = 0
			while y < world_size:
				row_v.append(False)
				row_px.append(-1)
				row_py.append(-1)
				y = y + 1
			visited.append(row_v)
			parent_x.append(row_px)
			parent_y.append(row_py)
			x = x + 1

		tx, ty = get_tail()

		visited[sx][sy] = True
		qx.append(sx)
		qy.append(sy)

		while head < len(qx):
			cx = qx[head]
			cy = qy[head]
			head = head + 1

			if cx == gx and cy == gy:
				path = []
				x0 = cx
				y0 = cy
				while not (x0 == sx and y0 == sy):
					path.append((x0, y0))
					px = parent_x[x0][y0]
					py = parent_y[x0][y0]
					x0 = px
					y0 = py
				path.append((sx, sy))

				rev = []
				i = len(path) - 1
				while i >= 0:
					rev.append(path[i])
					i = i - 1
				return rev

			d = 0
			while d < 4:
				nx = cx + DX[d]
				ny = cy + DY[d]

				if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
					if is_body(nx, ny):
						if not (allow_tail and nx == tx and ny == ty):
							d = d + 1
							continue

					if not visited[nx][ny]:
						visited[nx][ny] = True
						parent_x[nx][ny] = cx
						parent_y[nx][ny] = cy
						qx.append(nx)
						qy.append(ny)

				d = d + 1

		return []

	def follow_path_with_body(path, apple_x, apple_y):
		i = 1
		while i < len(path):
			cx, cy = pos()
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
				return False

			if not safe_move_and_update(d, apple_x, apple_y):
				return False

			i = i + 1

		return True

	def has_enough_space(nx, ny):
		tx, ty = get_tail()

		visited = []
		x = 0
		while x < world_size:
			row = []
			y = 0
			while y < world_size:
				row.append(False)
				y = y + 1
			visited.append(row)
			x = x + 1

		qx = []
		qy = []
		head = 0
		count = 0

		visited[nx][ny] = True
		qx.append(nx)
		qy.append(ny)

		while head < len(qx):
			cx = qx[head]
			cy = qy[head]
			head = head + 1

			count = count + 1
			if count >= snake_len + 2:
				return True

			d = 0
			while d < 4:
				xx = cx + DX[d]
				yy = cy + DY[d]

				if xx >= 0 and xx < world_size and yy >= 0 and yy < world_size:
					if not visited[xx][yy]:
						if is_body(xx, yy) and not (xx == tx and yy == ty):
							d = d + 1
							continue

						visited[xx][yy] = True
						qx.append(xx)
						qy.append(yy)
				d = d + 1

		if count >= snake_len:
			return True
		return False

	def head_can_reach_tail_from(nx, ny):
		tx, ty = get_tail()
		path = find_path_bfs(nx, ny, tx, ty, True)
		if len(path) > 0:
			return True
		return False

	def greedy_move_toward_apple(ax, ay):
		cx, cy = pos()

		dx = ax - cx
		dy = ay - cy

		if dx == 0 and dy == 0:
			return -1

		adx = my_abs(dx)
		ady = my_abs(dy)

		primary = -1
		secondary = -1

		if adx >= ady:
			if dx > 0:
				primary = DIR_E
			elif dx < 0:
				primary = DIR_W
			if dy > 0:
				secondary = DIR_N
			elif dy < 0:
				secondary = DIR_S
		else:
			if dy > 0:
				primary = DIR_N
			elif dy < 0:
				primary = DIR_S
			if dx > 0:
				secondary = DIR_E
			elif dx < 0:
				secondary = DIR_W

		dirs = []
		if primary != -1:
			dirs.append(primary)
		if secondary != -1:
			dirs.append(secondary)

		i = 0
		while i < len(dirs):
			d = dirs[i]
			nx = cx + DX[d]
			ny = cy + DY[d]

			if nx < 0 or nx >= world_size or ny < 0 or ny >= world_size:
				i = i + 1
				continue

			new_dx = my_abs(ax - nx)
			new_dy = my_abs(ay - ny)
			if new_dx + new_dy >= adx + ady:
				i = i + 1
				continue

			if is_body(nx, ny):
				i = i + 1
				continue

			if not can_move(DIR_CONSTANT(d)):
				i = i + 1
				continue

			if not has_enough_space(nx, ny):
				i = i + 1
				continue

			if not head_can_reach_tail_from(nx, ny):
				i = i + 1
				continue

			return d

			i = i + 1

		return -1

	def step_off_apple_after_eat():
		cx, cy = pos()
		d = 0
		while d < 4:
			nx = cx + DX[d]
			ny = cy + DY[d]

			if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
				if not is_body(nx, ny) and can_move(DIR_CONSTANT(d)):
					if safe_move_and_update(d, -1, -1):
						return True
			d = d + 1
		return False

	def step_off_initial_apple():
		global apples_eaten
		cx, cy = pos()

		apples_eaten = apples_eaten + 1

		d = 0
		while d < 4:
			nx = cx + DX[d]
			ny = cy + DY[d]

			if nx >= 0 and nx < world_size and ny >= 0 and ny < world_size:
				if can_move(DIR_CONSTANT(d)):
					if safe_move_and_update(d, cx, cy):
						return True
			d = d + 1

		return False

	def run_dinosaur_mode():
		change_hat(Hats.Dinosaur_Hat)
		init_snake_state()

		# first apple spawns under us; measure() tells us next apple while we stand on it
		first_next = measure()
		if first_next == None:
			change_hat(Hats.Brown_Hat)
			return

		target_x = first_next[0]
		target_y = first_next[1]

		if not step_off_initial_apple():
			change_hat(Hats.Brown_Hat)
			return

		while True:
			if no_legal_moves():
				change_hat(Hats.Brown_Hat)
				return

			cx, cy = pos()

			if cx == target_x and cy == target_y:
				nxt = measure()
				if nxt == None:
					change_hat(Hats.Brown_Hat)
					return

				next_x = nxt[0]
				next_y = nxt[1]

				if not step_off_apple_after_eat():
					change_hat(Hats.Brown_Hat)
					return

				target_x = next_x
				target_y = next_y
				continue

			dx = my_abs(target_x - cx)
			dy = my_abs(target_y - cy)
			maxd = dx
			if dy > maxd:
				maxd = dy

			# FAR: build + execute up to 10-step greedy segment
			if maxd > 10:
				segment_steps = 0
				while segment_steps < 10:
					cx2, cy2 = pos()
					if cx2 == target_x and cy2 == target_y:
						break

					gd = greedy_move_toward_apple(target_x, target_y)
					if gd == -1:
						break

					if not safe_move_and_update(gd, target_x, target_y):
						change_hat(Hats.Brown_Hat)
						return

					segment_steps = segment_steps + 1

				continue

			# MID: single-step greedy
			if maxd > 4:
				gd = greedy_move_toward_apple(target_x, target_y)
				if gd != -1:
					if not safe_move_and_update(gd, target_x, target_y):
						change_hat(Hats.Brown_Hat)
						return
					continue

			# NEAR or greedy failed: BFS to apple
			path_to_apple = find_path_bfs(cx, cy, target_x, target_y, True)

			if len(path_to_apple) > 0:
				if not follow_path_with_body(path_to_apple, target_x, target_y):
					change_hat(Hats.Brown_Hat)
					return
				continue

			# no path to apple: chase tail
			tail_x, tail_y = get_tail()
			path_to_tail = find_path_bfs(cx, cy, tail_x, tail_y, True)

			if len(path_to_tail) > 0:
				if not follow_path_with_body(path_to_tail, -1, -1):
					change_hat(Hats.Brown_Hat)
					return
				continue

			change_hat(Hats.Brown_Hat)
			return

	# =========================================
	# ======  HAMILTONIAN (SAFE) MODE  ========
	# =========================================

	ham_path_x = []
	ham_path_y = []
	ham_path_len = 0
	ham_index = 0
	ham_world_size = -1
	ham_forward = True
	ham_is_cycle = False

	ham_body_x = []
	ham_body_y = []
	ham_length = 0

	def ham_init_body(hx, hy):
		global ham_body_x
		global ham_body_y
		global ham_length

		ham_body_x = []
		ham_body_y = []
		ham_body_x.append(hx)
		ham_body_y.append(hy)
		ham_length = 1

	def ham_update_body(hx, hy, eaten):
		global ham_length
		ham_body_x.append(hx)
		ham_body_y.append(hy)
		if eaten:
			ham_length = ham_length + 1
		while len(ham_body_x) > ham_length:
			ham_body_x.pop(0)
			ham_body_y.pop(0)

	# ----- Hamiltonian path for odd N (simple serpentine) -----

	def generate_hpath_odd(N):
		px = []
		py = []

		y = 0
		while y < N:
			if y % 2 == 0:
				x = 0
				while x < N:
					px.append(x)
					py.append(y)
					x = x + 1
			else:
				x = N - 1
				while x >= 0:
					px.append(x)
					py.append(y)
					x = x - 1
			y = y + 1

		return px, py

	# ----- Hamiltonian CYCLE for even N -----
	# Pattern:
	# row 0:      (0,0) -> (1,0) -> ... -> (N-1,0)
	# row 1:      (N-1,1) -> (N-2,1) -> ... -> (1,1)
	# row 2:      (1,2) -> (2,2) -> ... -> (N-1,2)
	# row 3:      (N-1,3) -> ... -> (1,3)
	# ...
	# last row:   same snake pattern excluding x=0
	# then:       column 0 from bottom to top: (0,N-1) -> ... -> (0,1)
	# This leaves column 0 as the "return" to (0,0), forming a clean cycle.

	def generate_hcycle_even(N):
		cx = []
		cy = []

		#Bottom row:  left to right
		x = 0
		while x < N:
			cx.append(x)
			cy.append(0)
			x = x + 1
	
		# First, serpentine through all rows normally.
		y = 1
		while y < N:
			if y % 2 == 0:
				# even row: left → right
				x = 1
				while x < N:
					cx.append(x)
					cy.append(y)
					x = x + 1
			else:
				# odd row: right → left
				x = N - 1
				while x >= 1:
					cx.append(x)
					cy.append(y)
					x = x - 1
			y = y + 1
		cx.append(0)
		cy.append(N - 1)
		# Now add the return path up column 0
		# We end on (0,N-1) in the serpentine pattern already.
		# We must return from (0,N-1) → (0,0) without duplicating tiles.
		y = N - 2       # skip y = N-1 (already included)
		while y >= 0:   # stop at y=0; tile (0,0) is already the first tile
			cx.append(0)
			cy.append(y)
			y = y - 1

		# This produces a valid Hamiltonian cycle:
		# The last tile appended is (0,1), which is adjacent to (0,0)

		return cx, cy

	def ham_align(hx, hy, px, py):
		i = 0
		L = len(px)
		while i < L:
			if px[i] == hx and py[i] == hy:
				return i
			i = i + 1
		return 0

	def ham_get_dir(hx, hy, nx, ny):
		if nx == hx + 1 and ny == hy:
			return East
		if nx == hx - 1 and ny == hy:
			return West
		if ny == hy + 1 and nx == hx:
			return North
		return South

	def ham_rebuild_if_needed():
		global ham_world_size
		global ham_path_x
		global ham_path_y
		global ham_path_len
		global ham_index
		global ham_is_cycle
		global ham_forward

		N = get_world_size()

		if N != ham_world_size:
			ham_world_size = N

			if N % 2 == 0:
				# Even N: true Hamiltonian cycle
				ham_path_x, ham_path_y = generate_hcycle_even(N)
				ham_is_cycle = True
			else:
				# Odd N: Hamiltonian path, no true cycle
				ham_path_x, ham_path_y = generate_hpath_odd(N)
				ham_is_cycle = False
			ham_path_len = N * N

			hx, hy = pos()
			ham_index = ham_align(hx, hy, ham_path_x, ham_path_y)

			ham_init_body(hx, hy)
			ham_forward = True
			return ham_is_cycle

	def run_hamiltonian_mode():
		global ham_index
		global ham_forward
		global ham_is_cycle
		ham_is_cycle = ham_rebuild_if_needed()

		while True:
			ham_is_cycle = ham_rebuild_if_needed()

			# termination: reached max theoretical length
			if ham_length >= ham_path_len:
				# stop HAM mode; user can restart or do something else
				change_hat(Hats.Brown_Hat)
				return

			# check if we're currently standing on an apple
			res = measure()
			eaten_here = False
			if res != None:
				# standing on apple; we don't care where next apple will appear,
				# but we mark growth
				eaten_here = True

			ci = ham_index
			
			# We're not using Hamilton pathing for odd N right now
			ni = (ci + 1) % ham_path_len
#
#			if ham_is_cycle:
#				#EVEN N: true cycle, wrap around
#				ni = (ci + 1) % ham_path_len
#			else:
#				#ODD N: Hamiltonian path, bounce along it
#				if ham_forward:
#					if ci >= ham_path_len - 1:
#						ham_forward = False
#						ni = ci - 1
#					else:
#						ni = ci + 1
#				else:
#					if ci <= 0:
#						ham_forward = True
#						ni = 1
#					else:
#						ni = ci - 1


			hx = ham_path_x[ci]
			hy = ham_path_y[ci]
			nx = ham_path_x[ni]
			ny = ham_path_y[ni]

			d = ham_get_dir(hx, hy, nx, ny)

			if not move(d):
				change_hat(Hats.Brown_Hat)
				return

			ham_index = ni

			cx, cy = nx, ny
			ham_update_body(cx, cy, eaten_here)

	# =========================================
	# =========  MODE TOGGLER / ENTRY  ========
	# =========================================

	# Set this to "AI" for your smart Dino AI,
	# or "HAM" for Hamiltonian sweep mode.

	def run_dino_controller():
		if mode == "AI":
			run_dinosaur_mode()
		else:
			run_hamiltonian_mode()

	run_dino_controller()

#Fast dino code
def dino_fast():
	world_size = get_world_size()
	snake_length = 1

	def round(value, decimals):
		multiplier = 10 ** decimals
		return ((value * multiplier + 0.5) // 1) / multiplier

	def snake_move(dx, dy):
		global snake_length
		cx = get_pos_x()
		cy = get_pos_y()

		while not (cx == dx and cy == dy):
			apple = measure()
			if apple != None:
				snake_length += 1
				quick_print("Ate apple at (", cx, ", ", cy, "), length now ", round(snake_length/(world_size*world_size), 2)*100, "% of max")
			if cx < dx:
				if not move(East):
					return False
			elif cx > dx:
				if not move(West):
					return False
			elif cy < dy:
				if not move(North):
					return False
			elif cy > dy:
				if not move(South):
					return False
			cx = get_pos_x()
			cy = get_pos_y()
		return True
			

	while snake_length < world_size * world_size:
		cx = get_pos_x()
		cy = get_pos_y()
		if cx == 0 and cy == 0:
			moved = snake_move(world_size - 1, 0)
			moved = snake_move(world_size - 1, 1)
			if not moved:
				break
		elif cx == world_size - 1 and cy == world_size - 1:
			moved = snake_move(0, world_size - 1)
			moved = snake_move(0, 0)
			if not moved:
				break
		else:
			if cy % 2 == 1:
				moved = snake_move(1, cy)
				moved = snake_move(1, cy + 1)
				if not moved:
					break
			else:
				moved = snake_move(world_size - 1, cy)
				moved = snake_move(world_size - 1, cy + 1)
				if not moved:
					break

	change_hat(Hats.Brown_Hat)


