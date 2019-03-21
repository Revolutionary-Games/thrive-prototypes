import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (500, 500)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Swarming')
pygame.font.init()
clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 20)

def distance(i,j):
	return math.sqrt((i.x - j.x)**2 + (i.y - j.y)**2)

class animal:
	def __init__(self):
		self.x = random.randint(-100,100)
		self.y = random.randint(-100,100)
		self.dx = 1
		self.dy = 1
		self.angle = random.uniform(0,2*math.pi)


	def display(self):
		pygame.draw.circle(screen, (255,0,0), [int(self.x + width/2), int(self.y + height/2)], 5)
		endx = self.x - 15*math.cos(self.angle)
		endy = self.y - 15*math.sin(self.angle)
		pygame.draw.line(screen, (0,0,255), [int(self.x + width/2), int(self.y + height/2)],
			[int(endx + width/2), int(endy + height/2)], 3)


	def think(self, mousepos):
		bros = []
		for i in animals:
			bros.append([i,distance(self,i)])
		#sort the list of other animals on the screen by distance, this is very slow
		bros.sort(key = lambda bros: bros[1])
		#if you are too close move away
		if bros[1][1] <= 20:
			self.dx += 0.1*(self.x - bros[1][0].x)
			self.dy += 0.1*(self.y - bros[1][0].y)
		#if you are too close to the mouse move away
		if math.sqrt((self.x - mousepos[0])**2 + (self.y - mousepos[1])**2) <= 50:
			self.dx += 0.1*(self.x - mousepos[0])
			self.dy += 0.1*(self.y - mousepos[1])
		#if you can see some other animals move towards them
		for i in bros:
			if i[1] <= 100:
				self.dx += -0.0002*(self.x - i[0].x)
				self.dy += -0.0002*(self.y - i[0].y)
		#if you are going very fast then slow down
		if abs(self.dx) >= 1:
			self.dx = self.dx*0.9
		if abs(self.dy) >= 1:
			self.dy = self.dy*0.9				

	def update(self):
		timestep = 0.3
		self.x += self.dx*timestep
		self.y += self.dy*timestep
		#periodic boundary conditions.
		if self.x >= width/2:
			self.x += -width
		if self.x <= -width/2:
			self.x += width
		if self.y >= height/2:
			self.y += -height
		if self.y <= -height/2:
			self.y += height
		self.angle = math.atan2(self.dy, self.dx)


animals = []
for i in range(50):
	animals.append(animal())

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False

	screen.fill(background_colour)

	mousepos = [pygame.mouse.get_pos()[0] - width/2, pygame.mouse.get_pos()[1] - height/2]

	for i in animals:
		i.display()
		i.think(mousepos)
		i.update()

	clock.tick(60)


	pygame.display.flip()

pygame.quit()