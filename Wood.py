import Functions

#Plant wood in the world
def plant_wood(desired_substance):

	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			Functions.plant_crop("wood", desired_substance)
			move(North)
		move(East)

