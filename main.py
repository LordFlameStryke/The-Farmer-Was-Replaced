#imports
import Calibrate
import Pumpkin
import Dinosaur
import Maze
import Sunflower
import Functions
import Polyculture
import Cactus
import Carrot
import Hay
import Wood


# Values for easy reading
THOUSAND = 1000
MILLION = THOUSAND * THOUSAND
BILLION = THOUSAND * MILLION

# Desired amount of resources
DESIRED_HAY = 1 * BILLION
DESIRED_WOOD = 10 * BILLION
DESIRED_CARROTS = 1 * BILLION
DESIRED_PUMPKINS = 100 * MILLION
DESIRED_CACTUS = 1 * BILLION
DESIRED_WEIRD_SUBSTANCE = 1 * MILLION
DESIRED_TREASURE = 100 * MILLION
DESIRED_POWER = 1 * MILLION
DESIRED_BONES = 100 * MILLION

#set_world_size(6)

change_hat(Hats.Wizard_Hat)
if get_entity_type() == Entities.Treasure:
	harvest()
elif get_entity_type() == Entities.Hedge:
	clear()
pet_the_piggy()

first_run = True
poly = {}
	
while True:
	if first_run:
		DX,DY = Calibrate.calibrate_directions()
		first_run = False

	Functions.moveto(0, 0)
	if num_items(Items.Power) < DESIRED_POWER:
		change_hat(Hats.Sunflower_Hat)
		Sunflower.plant_sunflowers(DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Weird_Substance) < DESIRED_WEIRD_SUBSTANCE:
		change_hat(Hats.Purple_Hat)
		Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Hay) < DESIRED_HAY:
		change_hat(Hats.The_Farmers_Remains)
#		Hay.plant_hay(DESIRED_WEIRD_SUBSTANCE)
		Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Wood) < DESIRED_WOOD:
		change_hat(Hats.Brown_Hat)
#		Wood.plant_wood(DESIRED_WEIRD_SUBSTANCE)
		Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Carrot) < DESIRED_CARROTS:
		change_hat(Hats.Carrot_Hat)
#		Carrot.plant_carrots(DESIRED_WEIRD_SUBSTANCE)
		Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Pumpkin) < DESIRED_PUMPKINS:
		change_hat(Hats.Pumpkin_Hat)
		Pumpkin.plant_pumpkins(DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Cactus) < DESIRED_CACTUS:
		change_hat(Hats.Cactus_Hat)
		Cactus.plant_cactus(DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Gold) < DESIRED_TREASURE:
		change_hat(Hats.Gold_Hat)
		a = Maze.generate_maze(DESIRED_WEIRD_SUBSTANCE, DX, DY)
		if not a:
			# not enough weird substance to run maze, make more
			Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)
	elif num_items(Items.Bone) < DESIRED_BONES:
		clear()
		Dinosaur.dino_a_star(DX, DY, "AI")
	else:
		change_hat(Hats.Traffic_Cone)
		Polyculture.mix(poly, DESIRED_WEIRD_SUBSTANCE)

