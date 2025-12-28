import Functions

def assign_poly(poly, loc, crop):
	poly[loc] = crop

def get_loc():
	return get_pos_x(), get_pos_y()


#Mix planting different crops based on current inventory
def mix(poly, desired_substance):
	for i in range( get_world_size()):
		for j in range( get_world_size()):
			if can_harvest():
				harvest()
			curr_loc = get_loc()
			if curr_loc in poly:
				Functions.plant_crop(Functions.get_plant_from_entity(poly[curr_loc]), desired_substance)
				crop, location = get_companion()
				assign_poly(poly, location, crop)
				poly.pop(curr_loc)
			else:
				Functions.plant_crop("hay", desired_substance)
				crop, location = get_companion()
				poly[location] = crop
			move(North)
		move(East)

#Reset the "poly" array used for mixing crops
def reset_poly(poly):
	for i in range(get_world_size()):
		poly.append([i])
		for j in range(get_world_size()):
			poly[i].append([j])
			poly[i][j] = None
	return poly

