import pygame
import math
import random
from pygame.locals import *
from opensimplex import OpenSimplex


#setup

background_colour = (0,0,0)
(width, height) = (300, 300)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Simplex Noise')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

simp = OpenSimplex()
print (simp.noise4d(x=10, y=10, z = 5, w = 2))

screen.fill(background_colour)

maxv = 0
minv = 255
values = []

for i in range(width):
	values.append([])
	for j in range(height):
		s = i/width
		t = j/height

		nx = 5 + 2*math.cos(2*math.pi*s)
		ny = 5.5 + 2*math.cos(2*math.pi*t)
		nz = 5 + 2*math.sin(2*math.pi*s)
		nw = 5 + 2*math.sin(2*math.pi*t)

		val = simp.noise4d(x=nx, y=ny, z=nz, w=nw)
		val_col = (val + 1)/2
		values[i].append(val_col)
		maxv = max(val_col, maxv)
		minv = min(val_col, minv)

for i in range(width):
	for j in range(height):

		val_col = values[i][j]
		adj_val_col = (val_col - minv)/(maxv - minv)
		colour = (int(255*adj_val_col),int(255*adj_val_col),int(255*adj_val_col))

		screen.set_at((i, j), colour)

		

print(minv, maxv)


pygame.display.flip()

pygame.image.save(screen, "perlin.png")

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False 



pygame.quit()