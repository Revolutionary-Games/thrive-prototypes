import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,43,66)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be Books')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

tile_size = 200

#draw tile i,j at position x,y
def draw_tile(i,j,x,y):
	offset = 0
	cropRect = (i*tile_size + offset, j*tile_size + offset, tile_size - 2*offset, tile_size - 2*offset)
	screen.blit(tiles,(int(x*tile_size), int(y*tile_size)),cropRect)

def tesselate(test_connections, tiles_placed, i, j):
	if i == 0:
		if test_connections[3] == 1:
			return False
	if j == 0:
		if test_connections[0] == 1:
			return False
	if i == 4:
		if test_connections[1] == 1:
			return False
	if j == 2:
		if test_connections[2] == 1:
			return False
	if i > 0:
		if tiles_placed[i-1][j][1] != test_connections[3]:
			return False
	if j > 0:
		if tiles_placed[i][j-1][2] != test_connections[0]:
			return False
	return True
	

connections = [[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0]], [[0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1]], [[1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0]], [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1]], [[0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0]]]

tiles_placed = []

tiles = pygame.image.load("tiles_drawn.png")
#screen.blit(tiles, [0,0])

def reset():
	screen.fill(background_colour)
	global tiles_placed
	tiles_placed = []
	for i in range(5):
		tiles_placed.append([])
		for j in range(3):
				while 1:
					k = random.randint(0,4)
					l = random.randint(0,4)
					test_connections = connections[k][l][:]
					if tesselate(test_connections, tiles_placed, i, j):
						tiles_placed[i].append(test_connections)
						draw_tile(k,l,i,j)
						break

	#use flood fill to get all connected tiles
	stack = [[0,0]]
	processed = []
	while len(stack) > 0:
		for s in reversed(stack):
			tile = tiles_placed[s[0]][s[1]]
			print("tile = ", tile)
			if tile[0] == 1:
				neighbour = [s[0],s[1]-1]
				if neighbour not in stack and neighbour not in processed:
					stack.append(neighbour)
			if tile[1] == 1:
				neighbour = [s[0]+1,s[1]]
				if neighbour not in stack and neighbour not in processed:
					stack.append(neighbour)
			if tile[2] == 1:
				neighbour = [s[0],s[1]+1]
				if neighbour not in stack and neighbour not in processed:
					stack.append(neighbour)
			if tile[3] == 1:
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
	for i in range(5):
		for j in range(3):
			if [i,j] not in processed and tiles_placed[i][j] != [0,0,0,0]:
				done = False

	if done == False:
		reset()



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