import Functions

#Plant cactus in the world
def plant_cactus(desired_substance):
	 
	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			Functions.plant_crop("cactus", desired_substance)
			move(North)
		move(East)
	sort_cactus()

#Sort cactus plants in the world
def sort_cactus():
	 
	swapped = True
	while swapped:
		swapped = False
		for i in range( get_world_size()):
			if get_pos_y() ==  get_world_size() - 1 or not spawn_drone(sort_rows):
				sort_rows( get_world_size())
			move(North)
			if i == ( get_world_size() - 1):
				Functions.moveto(i,0)
		Functions.moveto(0,0)
		while num_drones() > 1:
			if random() < 0.5:
				do_a_flip()
			else:
				pet_the_piggy()
		for i in range( get_world_size()):
			if get_pos_x() ==  get_world_size() - 1 or not spawn_drone(sort_cols):
				sort_cols( get_world_size())	
			move(East)
			if i == ( get_world_size() - 1):
				Functions.moveto(0,0)
	while num_drones() > 1:
		if random() < 0.5:
			do_a_flip()
		else:
			pet_the_piggy()
	harvest()

#Sort columns of cactus plants
def sort_cols(max=None):
	change_hat(Hats.Cactus_Hat) 
	if max == None:
		max =  get_world_size()
	if max == 0:
		return
	Functions.moveto(get_pos_x(), 0)
	swapped = False
	for _ in range(max):
		if measure() == None:
			Functions.plant_crop("cactus", 1)
		if measure(North) == None and get_pos_y() < max - 1:
			move(North)
			Functions.plant_crop("cactus", 1)
			move(South)
		if measure(South) == None and get_pos_y() > 0:
			move(South)
			Functions.plant_crop("cactus", 1)
			move(North)
		if get_pos_y() < max - 1 and measure() > measure(North):
			swap(North)
			swapped = True
		if get_pos_y() > 0 and measure() < measure(South):
			swap(South)
			swapped = True
		move(North)
		if get_pos_y() == max:
			Functions.moveto(get_pos_x(), 0)
	if swapped:
		sort_cols(max - 1)

#Sort rows of cactus plants
def sort_rows(max=None):
	change_hat(Hats.Cactus_Hat)
	if max == None:
		max =  get_world_size()
	if max == 0:
		return
	Functions.moveto(0, get_pos_y())
	swapped = False
	for _ in range(max):
		if measure() == None:
			Functions.plant_crop("cactus", 1)
		if measure(East) == None and get_pos_x() < max - 1:
			move(East)
			Functions.plant_crop("cactus", 1)
			move(West)
		if measure(West) == None and get_pos_x() > 0:
			move(West)
			Functions.plant_crop("cactus", 1)
			move(East)
		if get_pos_x() < max - 1 and measure() > measure(East):
			swap(East)
			swapped = True
		if get_pos_x() > 0 and measure() < measure(West):
			swap(West)
			swapped = True
		move(East)
		if get_pos_x() == max:
			Functions.moveto(0, get_pos_y())
	if swapped:
		sort_rows(max - 1)
