import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (20,20,20)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Metaballs 2D')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

#Euclidean distance
def distance(a,b):
	return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def la(i,j,i1,j1):
	lines.append([[i,j], [i1,j1]])

#when you know the values on the corners of a square what lines should you draw?
#codes are [top left > 0 ? 1 : 0, top right, bottom right, bottom left]
def code_to_lines(code,i,j):
	if code == [1,0,0,0]: la(i + 0.5, j, i, j + 0.5)
	if code == [0,1,0,0]: la(i + 0.5, j, i + 1, j + 0.5)
	if code == [0,0,1,0]: la(i + 0.5, j + 1, i + 1, j + 0.5)
	if code == [0,0,0,1]: la(i, j + 0.5, i + 0.5, j + 1)

	if code == [1,1,0,0]: la(i, j + 0.5, i + 1, j + 0.5)
	if code == [0,1,1,0]: la(i + 0.5, j, i + 0.5, j + 1)
	if code == [0,0,1,1]: la(i + 1, j + 0.5, i, j + 0.5)
	if code == [1,0,0,1]: la(i + 0.5, j, i + 0.5, j + 1)

	if code == [1,0,1,0]: 
		la(i + 0.5, j, i, j + 0.5)
		la(i + 0.5, j + 1, i + 1, j + 0.5)
	if code == [0,1,0,1]: 
		la(i + 0.5, j, i + 1, j + 0.5)
		la(i + 0.5, j + 1, i, j + 0.5)

	if code == [1,1,1,0]: la(i, j + 0.5, i + 0.5, j + 1)
	if code == [0,1,1,1]: la(i + 0.5, j, i, j + 0.5)
	if code == [1,0,1,1]: la(i + 0.5, j, i + 1, j + 0.5)
	if code == [1,1,0,1]: la(i + 1, j + 0.5, i + 0.5, j + 1)

grid = [] #the grid of points you are marching over
lines = [] #lines to draw to find the edge of the shape
threshold = 4 #at what value of the scalar function should you find the boundary?
side_length = 100 #how many gridpoints per side?


def reset():
	global grid
	global lines
	global sources
	grid = [] #the grid of points you are marching over
	lines = [] #lines to draw to find the edge of the shape

	#add sources
	sources = []
	for i in range(random.randint(3,8)):
		sources.append([random.randint(int(0.2*side_length), int(0.8*side_length)), 
				random.randint(int(0.2*side_length), int(0.8*side_length))])

	#setup the grid
	for i in range(side_length):
		grid.append([])
		for j in range(side_length):
			grid[i].append([0])

	#work out scalar value at each point
	#scale for the number of sources and also the size of the grid
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			val = 0
			for s in sources:
				val += 1/max(0.1,distance(s,[i,j]))
			grid[i][j] = val*side_length/len(sources) 

	#march over the grid
	for i in range(len(grid) - 1):
		for j in range(len(grid[i]) - 1):
			#work out if the points are more or less than the threshold
			p1 = grid[i][j] - threshold
			p2 = grid[i + 1][j] - threshold
			p3 = grid[i + 1][j + 1] - threshold
			p4 = grid[i][j + 1] - threshold
			#from this populate the code with the values of the corners
			code = []
			for p in [p1,p2,p3,p4]:
				if p > 0:
					code.append(1)
				else:
					code.append(0)
			code_to_lines(code,i,j)

	#draw the result
	step_x = int(width/side_length)
	step_y = int(height/side_length)
	screen.fill(background_colour)

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if [i,j] not in sources:
				#pygame.draw.circle(screen, [0,0,255], [i*step_x, j*step_y], int(10*grid[i][j]))
				pass

	for l in lines:
		pygame.draw.line(screen, [0,255,0], [l[0][0]*step_x, l[0][1]*step_y], [l[1][0]*step_x, l[1][1]*step_y], 2)

	for s in sources:
		pygame.draw.circle(screen, [255,0,0], [s[0]*step_x, s[1]*step_y], 5)


	pygame.display.flip()

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
	       

	
	#clock.tick(100) 

pygame.quit()