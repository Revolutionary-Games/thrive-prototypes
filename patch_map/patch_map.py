import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,0,0)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Patch Map')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20, bold = True)

clock = pygame.time.Clock()

def distance(a,b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

#given a screen position and a total depth of the ocean return the type of patch
def get_type(pos, ocean_depth):
	if pos[1] < 0.25*height:
		if pos[0] < 0.33*width:
			return "Ice Shelf"
		return random.choice(["Tidepool", "Estuary"])
	patch_depth = ocean_depth*(pos[1] - height*0.25)/(height*0.75)
	#epipelagic zone
	if patch_depth < 200:
		return random.choice(["Ocean Surface", "Coastal Shelf"])
	#mesopelagic zone
	if patch_depth < 700:
		return random.choice(["Mid Ocean", "Mid Ocean", "Mid Ocean", "Cave"])
	#bathypelagic zone
	if patch_depth > 700 and pos[1] < 0.8*height:
		return random.choice(["Deep Ocean", "Deep Ocean", "Deep Ocean", "Cave"])
	#ocean floor
	return random.choice(["Ocean Floor", "Ocean Floor", "Hydrothermal"])

patch_names = ["Hydrothermal", "Ocean Floor", "Deep Ocean", "Mid Ocean", "Ocean Surface", "Coastal Shelf", "Tidepool", "Cave", "Ice Shelf", "Estuary"]

patches = []
min_seperation = 75 #pixels between patches
max_number_of_caves = 4 #what is the max number of caves allowed?
#note: photosynthesis is linear up to 100w/m^2 and then stops increasing. 

class patch:
	def __init__(self, pos, patch_type, ocean_depth, solar_strike):
		#screen position
		self.pos = pos
		#work out depth of the patch
		self.depth = int(ocean_depth*(pos[1] - height*0.25)/(height*0.75))
		if pos[1] < 0.25*height:
			self.depth = int(15*(pos[1] - 0.25*height)/(0.25*height))
		#work out how much light hits the patch
		self.sunlight = min(solar_strike, math.exp(-0.023*self.depth)*solar_strike)
		if patch_type == "Cave":
			self.sunlight = 0
		#what type of patch are you? from patch_names
		self.patch_type = patch_type
		#are you the patch where the player first starts?
		self.starter_patch = False
		#what other patches are you connected to?
		self.neighbours = []

		if patch_type == "Hydrothermal":
			self.colour = [255,0,0]
		if patch_type == "Ocean Floor":
			self.colour = [0,10,75]
		if patch_type == "Deep Ocean":
			self.colour = [0,20,100]
		if patch_type == "Mid Ocean":
			self.colour = [0,50,150]
		if patch_type == "Ocean Surface":
			self.colour = [0,75,200]
		if patch_type == "Coastal Shelf":
			self.colour = [0,255,255]
		if patch_type == "Tidepool":
			self.colour = [50,200,50]
		if patch_type == "Cave":
			self.colour = [50,50,50]
		if patch_type == "Ice Shelf":
			self.colour = [255,255,255]
		if patch_type == "Estuary":
			self.colour = [255,255,0]


def reset():
	#total ocean depth
	ocean_depth = random.randint(1000,5000)
	global patches
	patches = []
	needed_patches = patch_names[:]
	#build patch list
	#while there is room for another patch
	cave_counter = 0
	#amount of solar radiation strking the planet
	solar_strike = random.randint(300,3000) #watts per m^2
	while 1:
		made_patch = False
		patch_type = False
		counter = 0
		
		#try to add a patch
		while 1:
			#choose random position
			pos = [random.randint(10,width-10), random.randint(10,height-10)]
			#find out what kind of patch the new one is
			patch_type = get_type(pos, ocean_depth)
			#check if you need that patch to have one of each
			need_patch = True
			if (len(needed_patches) > 0 and patch_type not in needed_patches) or (patch_type == "Cave" and cave_counter >= max_number_of_caves):
				need_patch = False
			#check if the position is too close to another
			too_close = False
			for p in patches:
				if distance(p.pos,pos) < min_seperation:
					too_close = True
			#if the patch is not too close to another and is needed then make it 
			if too_close == False and need_patch == True:
				made_patch = True
				break
			#fail after 1000 attempts
			counter += 1
			if counter == 1000:
				break
		#if you failed to add a new patch you are done
		if made_patch == False:
			break
		patches.append(patch(pos, patch_type, ocean_depth, solar_strike))
		if patch_type in needed_patches:
			needed_patches.remove(patch_type)
		if patch_type == "Cave":
			cave_counter += 1

	#work out where the starter patch is
	best_dist = 10*width
	best_patch = patches[0]
	for p in patches:
		dist = abs(width/2 - p.pos[0])
		if p.patch_type == "Hydrothermal" and dist < best_dist:
			best_dist = dist
			best_patch = p
	best_patch.starter_patch = True
	print("Done")

reset()


running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        elif event.key == K_SPACE:
	        	reset()
	       

	screen.fill(background_colour)

	#draw ocean surface
	pygame.draw.line(screen, [0,0,200], [0, 0.25*height], [width, 0.25*height], 1)

	#draw patches
	for p in patches:
		if p.starter_patch:
			pygame.draw.circle(screen, [0,255,0], p.pos, 20)
		pygame.draw.circle(screen, p.colour, p.pos, 10)

	#display info for hovered patch
	pos = pygame.mouse.get_pos()
	for p in patches:
		if distance(p.pos, pos) < 50:
			textsurface = myfont.render("Patch Type : " + str(p.patch_type) + 
				"  Depth : " + str(p.depth) + "m" +
				"  Sunlight : " + str(round(p.sunlight,2)) + "w/m^2", True, [255,255,255])
			screen.blit(textsurface,(10, 10))


	pygame.display.flip()
	
	

pygame.quit()