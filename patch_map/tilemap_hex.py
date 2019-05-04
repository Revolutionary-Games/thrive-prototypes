import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,43,66)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
fake_screen = pygame.Surface((1000,700))
#fake_screen.fill(background_colour)
pygame.display.set_caption('Let there be Tiles')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

tile_size = 200

#draw tile i,j at position x,y
def draw_tile(i,j,x,y):
	offset = 0
	cropRect = (i*tile_size + offset, j*tile_size + offset, tile_size - 2*offset, tile_size - 2*offset)
	tile = pygame.Surface([tile_size, tile_size])
	tile.blit(tiles, [-i*tile_size,-j*tile_size])
	tile.convert_alpha()
	tile.set_colorkey((255,255,255)) 
	pygame.draw.polygon(tile, [255,255,255,0], [[0,0], [0.25*tile_size,0], [0,0.5*tile_size]])
	pygame.draw.polygon(tile, [255,255,255,0], [[0.75*tile_size,0], [tile_size,0], [tile_size,0.5*tile_size]])
	pygame.draw.polygon(tile, [255,255,255,0], [[0,tile_size], [0.25*tile_size,tile_size], [0,0.5*tile_size]])
	pygame.draw.polygon(tile, [255,255,255,0], [[0.75*tile_size,tile_size], [tile_size,tile_size], [tile_size,0.5*tile_size]])
	w = x*0.75*tile_size + 25
	h = y*tile_size
	if x % 2 == 0:
		h = (y + 0.5)*tile_size
	fake_screen.blit(tile,(int(w), int(h)))
	#screen.blit(tiles,(int(x*tile_size), int(y*tile_size)),cropRect)

def tesselate(test_connections, tiles_placed, i, j):
	if i == 0:
		if test_connections[4] == 1 or test_connections[5] == 1:
			return False
	if j == 0:
		if test_connections[0] == 1:
			return False
	if i == cols-1:
		if test_connections[1] == 1 or test_connections[2] == 1:
			return False
	if j == rows-1:
		if test_connections[3] == 1:
			return False
	if i % 2 == 1:
		if i > 0:
			if tiles_placed[i-1][j][1] != test_connections[4]:
				return False
			if j > 0:
				if tiles_placed[i-1][j-1][2] != test_connections[5]:
					return False
	else:
		if i > 0:
			if tiles_placed[i-1][j][2] != test_connections[5]:
				return False
			if j < rows-1:
				if tiles_placed[i-1][j+1][1] != test_connections[4]:
					return False
	if j > 0:
		if tiles_placed[i][j-1][3] != test_connections[0]:
			return False
	return True
	

connections = [[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1]], [[0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1]], [[0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 1, 0], [0, 1, 0, 1, 1, 1]], [[0, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1], [0, 1, 1, 1, 0, 0], [0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1]], [[1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0], [1, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0], [1, 0, 0, 1, 1, 1]], [[1, 0, 1, 0, 0, 0], [1, 0, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1], [1, 0, 1, 1, 0, 0], [1, 0, 1, 1, 0, 1], [1, 0, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1]], [[1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 1]], [[1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0], [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1]]]

tiles_placed = []

tiles = pygame.image.load("tiles_hex_drawn.png").convert_alpha()
#screen.blit(tiles, [0,0])

cols = 6
rows = 3

def reset():
	screen.fill([0,0,0])
	global tiles_placed
	tiles_placed = []
	for i in range(cols):
		tiles_placed.append([])
		for j in range(rows):
			while 1:
				k = random.randint(0,7)
				l = random.randint(0,7)
				test_connections = connections[k][l][:]
				if tesselate(test_connections, tiles_placed, i, j):
					tiles_placed[i].append(test_connections)
					draw_tile(k,l,i,j)
					break

	#use flood fill to get all connected tiles
	if True:
		stack = [[0,0]]
		processed = []
		while len(stack) > 0:
			for s in reversed(stack):
				if s[0] >= 0 and s[0] < cols and s[1] >= 0 and s[1] < rows:
					tile = tiles_placed[s[0]][s[1]]
					print("tile = ", tile)
					if tile[0] == 1:
						neighbour = [s[0],s[1]-1]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
					if tile[1] == 1:
						neighbour = [s[0]+1,s[1]-1]
						if s[0] % 2 == 0:
							neighbour = [s[0]+1,s[1]]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
					if tile[2] == 1:
						neighbour = [s[0]+1,s[1]]
						if s[0] % 2 == 0:
							neighbour = [s[0]+1,s[1]+1]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
					if tile[3] == 1:
						neighbour = [s[0],s[1]+1]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
					if tile[4] == 1:
						neighbour = [s[0]-1,s[1]]
						if s[0] % 2 == 0:
							neighbour = [s[0]-1,s[1]+1]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
					if tile[5] == 1:
						neighbour = [s[0]-1,s[1]-1]
						if s[0] % 2 == 0:
							neighbour = [s[0]-1,s[1]]
						if neighbour not in stack and neighbour not in processed:
							stack.append(neighbour)
				if s not in processed:
					processed.append(s)
				stack.remove(s)
				print("stack = ", stack)
				print("processed = ", processed)

		#if not all tiles are connected try again
		done = True
		for i in range(cols):
			for j in range(rows):
				if [i,j] not in processed and tiles_placed[i][j] != [0,0,0,0]:
					done = False

		if done == False:
			print("disconnected")
			reset()

	screen.blit(pygame.transform.scale(fake_screen, (1000,600)), (0, 0))



print(tiles_placed)

reset()
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	        	reset()
	       

	#screen.fill(background_colour)

	pygame.display.flip()
	
	

pygame.quit()