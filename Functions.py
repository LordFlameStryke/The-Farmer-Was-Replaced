#Return a plant from an entity type
def get_plant_from_entity(entity):
	if entity == Entities.Grass:
		return "hay"
	elif entity == Entities.Tree:
		return "tree"
	elif entity == Entities.Bush:
		return "bush"
	elif entity == Entities.Carrot:
		return "carrot"
	elif entity == Entities.Pumpkin:
		return "pumpkin"
	elif entity == Entities.Sunflower:
		return "sunflower"
	elif entity == Entities.Cactus:
		return "cactus"
	else:
		return None

#Move to specific coordinates considering world wrap-around
def moveto(x, y):
	desired_x = x - get_pos_x()
	desired_y = y - get_pos_y()
	if desired_x == 0 and desired_y == 0:
		return
	size = get_world_size() / 2
	if abs(desired_x) < size and desired_x < 0:
		while get_pos_x() != x:
			move(West)
	elif abs(desired_x) < size and desired_x > 0:
		while get_pos_x() != x:
			move(East)
	elif abs(desired_x) > size and desired_x < 0:
		while get_pos_x() != x:
			move(East)
	elif abs(desired_x) > size and desired_x > 0:
		while get_pos_x() != x:
			move(West)
	else:
		while get_pos_x() != x:
			move(East)
	if abs(desired_y) < size and desired_y < 0:
		while get_pos_y() != y:
			move(South)
	elif abs(desired_y) < size and desired_y > 0:
		while get_pos_y() != y:
			move(North)
	elif abs(desired_y) > size and desired_y < 0:
		while get_pos_y() != y:
			move(North)
	elif abs(desired_y) > size and desired_y > 0:
		while get_pos_y() != y:
			move(South)
	else:
		while get_pos_y() != y:
			move(North)

#Get the opposite direction
def opposite_direction(direction):
	if direction == North:
		return South
	elif direction == South:
		return North
	elif direction == East:
		return West
	elif direction == West:
		return East

#Plant different types of crops based on input
def plant_crop(plant_type, desired_substance):
	while get_water() < 0.76:
		use_item(Items.Water)
	if plant_type == "carrot":
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() == Entities.Carrot:
			return
		plant(Entities.Carrot)
	elif plant_type == "wood":
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			if get_entity_type() == Entities.Tree:
				return
			plant(Entities.Tree)
		else:
			if get_entity_type() == Entities.Bush:
				return
			plant(Entities.Bush)
	elif plant_type == "tree":
		if get_entity_type() == Entities.Tree:
			return
		plant(Entities.Tree)
	elif plant_type == "bush":
		if get_entity_type() == Entities.Bush:
			return
		plant(Entities.Bush)
	elif plant_type == "pumpkin":
		if get_entity_type() == Entities.Pumpkin:
			return
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
	elif plant_type == "sunflower":
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() == Entities.Sunflower:
			return
		plant(Entities.Sunflower)
	elif plant_type == "cactus":
		if get_entity_type() == Entities.Cactus:
			return
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
	else:
		if get_ground_type() == Grounds.Soil:
			till()
	if num_items(Items.Weird_Substance) < desired_substance and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

