# agent guessing game prototype

import pygame
import math
import random
from pygame.locals import *

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Noise')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

def distance(x1,y1,x2,y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class microbe:
	def __init__(self):
		self.x = random.randint(0,width - 200)
		self.y = random.randint(0,height - 50)
		self.vulnerable = random.randint(0,3)

	def display(self):
		for i in range(4):
			if self.vulnerable == i and distance(self.x, self.y, mousex, mousey) <= 50:
				pass
			else:
				pygame.draw.circle(screen, [200*i % 255,70*i % 255, (50 + 30*i) % 255], (int(self.x + 20*i), int(self.y)), 10, 0)


global microbes
microbes = []
for i in range(5):
	microbes.append(microbe())


running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False
	        

	screen.fill(background_colour)

	(mousex, mousey) = pygame.mouse.get_pos()

	for microbe in microbes:
		microbe.display()

	pygame.display.flip()

pygame.quit()