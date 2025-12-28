import Functions

#Plant carrots in the world
def plant_carrots(desired_substance):

	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			Functions.plant_crop("carrot", desired_substance)
			move(North)
		move(East)

