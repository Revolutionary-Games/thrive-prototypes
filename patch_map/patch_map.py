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

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

def distance(a,b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_type(pos):
	if pos[1] < 0.25*height:
		if pos[0] < 0.33*width:
			return "Ice Shelf"
		return random.choice(["Tidepool", "Estuary"])
	if pos[1] < 0.4*height:
		return random.choice(["Ocean Surface", "Coastal Shelf"])
	if pos[1] < 0.6*height:
		return random.choice(["Mid Ocean", "Mid Ocean", "Cave"])
	if pos[1] < 0.8*height:
		return random.choice(["Deep Ocean", "Hydrothermal"])
	return "Ocean Floor"

patch_names = ["Hydrothermal", "Ocean Floor", "Deep Ocean", "Mid Ocean", "Ocean Surface", "Coastal Shelf", "Tidepool", "Cave", "Ice Shelf", "Estuary"]

patches = []
min_seperation = 100 #pixels between patches

class patch:
	def __init__(self, pos, patch_type):
		self.pos = pos
		self.depth = int(3600*(pos[1] - 0.25*height)/(0.75*height))
		if pos[1] < 0.25*height:
			self.depth = int(50*(pos[1] - 0.25*height)/(0.25*height))
		self.patch_type = patch_type
		self.starter_patch = False
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
	global patches
	patches = []
	needed_patches = patch_names[:]
	#build patch list
	#while there is room for another patch
	while 1:
		made_patch = False
		patch_type = False
		counter = 0
		#try to add a patch
		while 1:
			#choose random position
			pos = [random.randint(10,width-10), random.randint(10,height-10)]
			#find out what kind of patch the new one is
			patch_type = get_type(pos)
			#check if you need that patch to have one of each
			need_patch = True
			if len(needed_patches) > 0 and patch_type not in needed_patches:
				need_patch = False
			#check if the position is too close to another
			too_close = False
			for p in patches:
				if distance(p.pos,pos) < min_seperation:
					too_close = True
			if too_close == False:
				made_patch = True
				break
			#fail after 1000 attempts
			counter += 1
			if counter == 1000:
				break
		#if you failed to add a new patch you are done
		if made_patch == False:
			break
		patches.append(patch(pos, patch_type))
		if patch_type in needed_patches:
			needed_patches.remove(patch_type)

	#work out where the starter patch is
	best_dist = 10*width
	best_patch = False
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

	#draw patches
	for p in patches:
		if p.starter_patch:
			pygame.draw.circle(screen, [0,255,0], p.pos, 20)
		pygame.draw.circle(screen, p.colour, p.pos, 10)

	#display info for hovered patch
	pos = pygame.mouse.get_pos()
	for p in patches:
		if distance(p.pos, pos) < 50:
			textsurface = myfont.render("Patch Type : " + str(p.patch_type) + "  Depth : " + str(p.depth) + "m", True, [255,255,255])
			screen.blit(textsurface,(10, 10))


	pygame.display.flip()
	
	

pygame.quit()