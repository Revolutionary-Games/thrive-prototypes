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

#check if a rectangle collides with the screen
def collide_rect_screen(x,y,w,h):
	if x + w > width or x - w < 0 or y + h > height or y - h < 0:
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

#check if two rectangles collide
def collide_rects(x1,y1,w1,h1,x2,y2,w2,h2):
	if x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2:
		return False
	else:
		return True

#check if a point collides with a rect
def collide_point_rect(x,y,x1,y1,w1,h1):
	if x > x1 and x < x1 + w1 and y > y1 and y < y1 + h1:
		return True
	else:
		return False

#a cluster of patch nodes
class cluster:
	#x,y,width,height,number of nodes verticall, number of nodes horizontally
	def __init__(self,x,y,w,h,n,m):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.n = n
		self.m = m
		self.nodes = []
		self.neighbours = []
		#is the user hovering over this clusted?
		self.highlight = False

	def draw_connections(self):
		for n in self.neighbours:
			start = (int(self.x + 0.5*self.w), int(self.y + 0.5*self.h))
			end = (int(n.x + 0.5*n.w), int(n.y + 0.5*n.h))
			mid1 = (0.5*(start[0] + end[0]), start[1])
			mid2 = (0.5*(start[0] + end[0]), end[1])
			colour = [125,125,225]
			if self.highlight or n.highlight:
				colour = [125,225,125]			
			pygame.draw.line(screen, colour, start, mid1, 2)
			pygame.draw.line(screen, colour, mid1, mid2, 2)
			pygame.draw.line(screen, colour, mid2, end, 2)

	def draw(self):
		pygame.draw.rect(screen, background_colour, (int(self.x), int(self.y), int(self.w), int(self.h)))
		colour = [125,125,225]
		if self.highlight:
			colour = [125,225,125]
		pygame.draw.rect(screen, colour, (int(self.x), int(self.y), int(self.w), int(self.h)), 2)

#a patch node
class node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.colour = random.choice(colours)

	def draw(self):
		pygame.draw.circle(screen, self.colour,(int(self.x), int(self.y)), 10)

node_size = 30
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
		n = random.randint(1,5)
		m = random.choice([1,1,1,2,2,3])
		w = node_size*m
		h = node_size*n
		#if the cluster is fully on the screen
		if collide_rect_screen(x,y,w,h) == False:
			#check the cluster does not collide with any others
			collided = False		
			for c in clusters:	
				padding = 50		
				if collide_rects(x -padding,y-padding,w+2*padding,h+2*padding,c.x,c.y,c.w,c.h):
					collided = True
					break
			#if it is on the screen and not colliding with any others then add it
			if collided == False:
				clusters.append(cluster(x,y,w,h,n,m))

	#add patches to each random cluster
	for c in clusters:
		for i in range(c.m):
			x = c.x + i*node_size + node_size/2
			for j in range(c.n):
				y = c.y + j*node_size + node_size/2
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

	#check if the mouse pointer is hovering over any of the patches
	mouse_pos = pygame.mouse.get_pos()
	for c in clusters:
		c.highlight = False
		if collide_point_rect(mouse_pos[0], mouse_pos[1], c.x, c.y, c.w, c.h):
			c.highlight = True
	       

	screen.fill(background_colour)

	for c in clusters:
		c.draw_connections()

	for c in clusters:
		c.draw()
		for n in c.nodes:
			n.draw()

	pygame.display.flip()
	
	

pygame.quit()