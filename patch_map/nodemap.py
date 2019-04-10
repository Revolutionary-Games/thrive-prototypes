import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (10,10,30)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Node Map')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

colours = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 190), (0, 128, 128), (230, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255)]

#check if a circle is off the screen
def collide_circle_screen(x,y,r):
	if x + r > width or x - r < 0 or y + r > height or y - r < 0:
		return True
	else:
		return False

#distance between two points
def distance(x1,y1,x2,y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#check if two circles are colliding
def collide_circles(x1,y1,r1,x2,y2,r2):
	if distance(x1,y1,x2,y2) < r1 + r2:
		return True
	else:
		return False

#a cluster of patch nodes
class cluster:
	def __init__(self,x,y,r):
		self.x = x
		self.y = y
		self.r = r
		self.nodes = []
		self.neighbours = []

	def draw_connections(self):
		for n in self.neighbours:
			pygame.draw.line(screen, [125,125,225], (int(self.x), int(self.y)), (int(n.x), int(n.y)), 2)

	def draw(self):
		pygame.draw.circle(screen, background_colour, (int(self.x), int(self.y)), int(self.r))
		pygame.draw.circle(screen, [125,125,225], (int(self.x), int(self.y)), int(self.r), 2)

#a patch node
class node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.colour = random.choice(colours)

	def draw(self):
		pygame.draw.circle(screen, self.colour,(int(self.x), int(self.y)), int(10))

clusters = []
def reset():
	#add some random clusters to the map
	global clusters
	clusters = []
	counter = 0
	while counter < 1000:
		counter += 1
		x = random.randint(0,width)
		y = random.randint(0,height)
		r = random.randint(40,100)
		#if the cluster is fully on the screen
		if collide_circle_screen(x,y,r) == False:
			#check the cluster does not collide with any others
			collided = False		
			for c in clusters:			
				if collide_circles(x,y,1.1*r,c.x,c.y,1.1*c.r):
					collided = True
					break
			#if it is on the screen and not colliding with any others then add it
			if collided == False:
				clusters.append(cluster(x,y,r))

	#add patches to each random cluster
	for c in clusters:
		n = random.randint(2,7)
		step = 2*math.pi/n 
		for i in range(n):
			angle = -math.pi/2 + step*i
			x = c.x + 0.6*c.r*math.cos(angle)
			y = c.y + 0.6*c.r*math.sin(angle)
			c.nodes.append(node(x,y))

	#add connections between clusters
	for c in clusters:
		while 1:
			d = random.choice(clusters)
			if distance(d.x,d.y,c.x,c.y) < 300 and d != c and c not in d.neighbours:
				c.neighbours.append(d)
				break


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

	for c in clusters:
		c.draw_connections()

	for c in clusters:
		c.draw()
		for n in c.nodes:
			n.draw()

	pygame.display.flip()
	
	

pygame.quit()