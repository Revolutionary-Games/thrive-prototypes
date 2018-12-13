import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,0,0)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Clade Diagram')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

#class for species in the diagram
class node:
	def __init__(self, parent, death_time):
		self.parent = parent
		self.death_time = death_time #at what time in history did you die off = where to draw on y axis
		self.x_pos = 0 #where should you be drawn on the x axis?
		self.circular_pos = [0,0] #stored in polar, angle, distance
		self.colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		#child nodes of this node
		self.left = False
		self.right = False

#recursively build a list of the nodes in left to right order
def append_nodes(nod):
	if nod.left is not False:
		append_nodes(nod.left)

	nodes.append(nod)

	if nod.right is not False:
		append_nodes(nod.right)

def polar_cart(angle, dist):
	return [int(0.5*width + dist*math.cos(-angle)), int(0.5*height + dist*math.sin(-angle))]

def scale_time(t):
	return 280*(t - 20)/height

def reset():

	#start a binary tree
	root = node(False, 20)

	#add 20 elements to the tree at random
	for i in range(20):
		current = root
		while 1:		
			if current.left is not False:
				current = random.choice([current.left, current.right])
			else:
				death_time = current.death_time + random.randint(70,100)
				current.left = node(current, death_time)
				current.right = node(current, death_time)
				break

	#get a list of the nodes in order of position
	global nodes
	nodes = []
	append_nodes(root)

	#find the xpos for each node
	x_pos = 20
	for i in range(len(nodes)):
		nodes[i].x_pos = x_pos
		next_node = nodes[(i + 1) % len(nodes)]
		#if the boxes are not close in y direction put them close in x
		if (next_node.death_time > nodes[i].death_time + box_width or 
			next_node.death_time < nodes[i].death_time - box_width):
			x_pos += 0.8*box_width
		else:
			x_pos += 1.2*box_width
		if nodes[i].left == False:
			nodes[i].death_time = height - 20 - box_width//2

	#find the circular positions for each node
	outer_diameter = math.pi*2*280
	x_step = outer_diameter/x_pos
	for n in nodes:
		dist = scale_time(n.death_time)
		angle = math.pi*2*n.x_pos*x_step/outer_diameter
		n.circular_pos = [angle, dist]


box_width = 20
reset()

draw_circular = True
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
	       

	screen.fill(background_colour)

	if draw_circular is True:
		for n in nodes:
			if n.parent is not False:
				avg_time = (n.parent.death_time + min(n.parent.left.death_time, n.parent.right.death_time))//2
				avg_time = scale_time(avg_time)
				pygame.draw.line(screen, [0,0,255], polar_cart(n.circular_pos[0], n.circular_pos[1]), 
						polar_cart(n.circular_pos[0], avg_time), 3)
				#pygame.draw.line(screen, [0,0,255], polar_cart(n.circular_pos[0], avg_time), 
				#		polar_cart(n.parent.circular_pos[0], avg_time), 1)
				a = n.circular_pos[0]
				b = n.parent.circular_pos[0]
				if a > b:
					b = a
					a = n.parent.circular_pos[0]
				pygame.draw.arc(screen, [0,0,255], 
					[0.5*width - avg_time,0.5*height - avg_time,2*avg_time, 2*avg_time], 
					a, b + 0.02, 3)
				pygame.draw.line(screen, [0,0,255], polar_cart(n.parent.circular_pos[0], avg_time), 
						polar_cart(n.parent.circular_pos[0], n.parent.circular_pos[1]), 3)

		for n in nodes:
			pygame.draw.circle(screen, n.colour, polar_cart(n.circular_pos[0], n.circular_pos[1]), 10)

	else:
		#draw lines between boxes
		for n in nodes:
			if n.parent is not False:
				avg_time = (n.parent.death_time + min(n.parent.left.death_time, n.parent.right.death_time))//2
				pygame.draw.line(screen, [0,0,255], [n.x_pos, n.death_time], [n.x_pos, avg_time], 1)
				pygame.draw.line(screen, [0,0,255], [n.x_pos, avg_time], [n.parent.x_pos, avg_time], 1)
				pygame.draw.line(screen, [0,0,255], [n.parent.x_pos, avg_time], [n.parent.x_pos, n.parent.death_time], 1)

		#draw the boxes themselves
		for n in nodes:
			pygame.draw.polygon(screen, n.colour, 
				[[n.x_pos - box_width//2, n.death_time - box_width//2],
				[n.x_pos + box_width//2, n.death_time - box_width//2],
				[n.x_pos + box_width//2, n.death_time + box_width//2],
				[n.x_pos - box_width//2, n.death_time + box_width//2]])

	pygame.display.flip()
	
	

pygame.quit()