import Functions

#Check to see if any pumpkins are still dead and replant them
def check_pumpkins(dead=[], desired_substance=1):
	 
	quick_print(dead)
	if len(dead) == 0:
		for i in range( get_world_size()):
			for j in range( get_world_size()):
				if get_entity_type() == Entities.Dead_Pumpkin or get_entity_type() == None:
					dead.append([get_pos_x(), get_pos_y()])
					Functions.plant_crop("pumpkin", desired_substance)
				move(North)
			move(East)
	else:
		for coord in range(len(dead)-1, -1, -1):
			coords = dead[coord]
			Functions.moveto(coords[0], coords[1])
			if get_entity_type() == Entities.Pumpkin:
				dead.remove(coords)
			else:
				while not can_harvest() and not get_entity_type() == Entities.Dead_Pumpkin:
					pass
				Functions.plant_crop("pumpkin", desired_substance)
	if len(dead) == 1:
		while not get_entity_type() == Entities.Pumpkin:
			do_a_flip()
			Functions.plant_crop("pumpkin", desired_substance)
		while not can_harvest():
			pass
	if len(dead) > 0:
		check_pumpkins(dead, desired_substance)
	Functions.moveto(0, 0)
	harvest()

#Plant pumpkins and check for dead ones
def plant_pumpkins(desired_substance):
	 
	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			if not get_entity_type() == Entities.Pumpkin:
				Functions.plant_crop("pumpkin", desired_substance)
			move(North)
		move(East)
	check_pumpkins([], desired_substance)

