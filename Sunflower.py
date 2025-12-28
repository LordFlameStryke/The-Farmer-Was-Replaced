import Functions

#Harvest sunflowers based on their size
def harvest_sunflower(sunflower_array):
	
	for i in range(len(sunflower_array) - 1, -1, -1):
		for j in range(len(sunflower_array[i])):
			Functions.moveto(sunflower_array[i][j][0], sunflower_array[i][j][1])
			harvest()

#Plant sunflowers in the world
def plant_sunflowers(desired_substance):
	MAX_PETALS = 15
	MIN_PETALS = 7
	sunflower_array = []
	for i in range(MAX_PETALS - MIN_PETALS):
		sunflower_array.append([])
	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			Functions.plant_crop("sunflower", desired_substance)
			while measure() == MAX_PETALS:
				while not can_harvest():
					use_item(Items.Fertilizer)
				harvest()
				Functions.plant_crop("sunflower", desired_substance)
			sunflower_array[measure() - MIN_PETALS].append([get_pos_x(), get_pos_y()])
			move(North)
		move(East)
	harvest_sunflower(sunflower_array)
	
