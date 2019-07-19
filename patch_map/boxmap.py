import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,43,66)
line_colour = (0,196,162)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Node Map')
pygame.font.init()

myfont = pygame.font.SysFont("monospace",20,bold = True)
icons = pygame.image.load("icons.png")
icons = pygame.transform.rotozoom(icons, 0, 0.5)

clock = pygame.time.Clock()

colours = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 190), (0, 128, 128), (230, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255)]

#distance between two points
def distance(p1,p2):
	return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

#functions to work out if two lines cross
#cross product
#which side of b - a is c on?
def cross(ax, ay, bx, by, cx, cy):
    return (bx - ax)*(cy - ay) - (by - ay)*(cx - ax);
#get the sgn of a value
def sgn(x):
	if x > 0:
		return 1
	return -1
#check if the two lines intersect
def intersect(l1,l2):
	a = l1[0]
	b = l1[1]
	c = l2[0]
	d = l2[1]
	if ( sgn(cross(a[0],a[1],b[0],b[1],c[0],c[1])) != sgn(cross(a[0],a[1],b[0],b[1],d[0],d[1])) and
		sgn(cross(c[0],c[1],d[0],d[1],a[0],a[1])) != sgn(cross(c[0],c[1],d[0],d[1],b[0],b[1])) and
		a != c and a != d and b != c and b != d):
		return True
	return False

#check if a rectangle collides with the screen
def collide_rect_screen(x,y,w,h):
	if x + w + 5 > width or x < 5 or y + h + 5 > height or y < 5:
		return True
	else:
		return False

#check if two rectangles collide
def collide_rects(x1,y1,w1,h1,x2,y2,w2,h2):
	if x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2:
		return False
	else:
		return True

#check if a box collides with the screen or anything else
#return True if the box is in a valid place
def collide_rect_screen_and_rects(cluster, margin):
	if collide_rect_screen(cluster.x - margin,cluster.y-margin,cluster.w+2*margin,cluster.h+2*margin) == True:
		return False
	for c in clusters:
		if collide_rects(cluster.x-margin,cluster.y-margin,cluster.w+2*margin,cluster.h+2*margin,c.x,c.y,c.w,c.h) == True:
			return False
	return True

#check if a box and a line intersect
def collide_line_box(l,b):
	if intersect(l,[[b.x,b.y],[b.x + b.w, b.y]]):
		return True
	if intersect(l,[[b.x + b.w, b.y],[b.x + b.w, b.y + b.h]]):
		return True
	if intersect(l,[[b.x + b.w, b.y + b.h], [b.x, b.y + b.h]]):
		return True
	if intersect(l,[[b.x, b.y + b.h], [b.x, b.y]]):
		return True
	return False

#check if a box and a line overlap
def overlap_line_box(l,b):
	if lines_overlap(l,[[b.x,b.y],[b.x + b.w, b.y]]):
		return True
	if lines_overlap(l,[[b.x + b.w, b.y],[b.x + b.w, b.y + b.h]]):
		return True
	if lines_overlap(l,[[b.x + b.w, b.y + b.h], [b.x, b.y + b.h]]):
		return True
	if lines_overlap(l,[[b.x, b.y + b.h], [b.x, b.y]]):
		return True
	return False

#check if a box and a line intersect
def collide_line_box_with_gap(l,b,gap):
	if intersect(l,[[b.x-gap,b.y-gap],[b.x-gap + b.w+2*gap, b.y-gap]]):
		return True
	if intersect(l,[[b.x-gap + b.w+2*gap, b.y-gap],[b.x-gap + b.w+2*gap, b.y-gap + b.h+2*gap]]):
		return True
	if intersect(l,[[b.x-gap + b.w+2*gap, b.y-gap + b.h+2*gap], [b.x-gap, b.y-gap + b.h+2*gap]]):
		return True
	if intersect(l,[[b.x-gap, b.y-gap + b.h+2*gap], [b.x-gap, b.y-gap]]):
		return True
	return False

#check if two line segments overlap
def lines_overlap(l1,l2):
	#do they have they same gradient? all lines are either horizontal or vertical
	#horizontal
	if (l1[0][1] - l1[1][1] == 0 and l2[0][1] - l2[1][1] == 0):
		#do they have the same y value?
		if (l1[0][1] == l2[0][1]):
			#do the x segments overlap?
			l1x_min = min(l1[0][0], l1[1][0]) 
			l1x_max = max(l1[0][0], l1[1][0])
			l2x_min = min(l2[0][0], l2[1][0]) 
			l2x_max = max(l2[0][0], l2[1][0])  
			if not (l1x_max < l2x_min or l1x_min > l2x_max):
				return True
	#vertical
	elif(l1[0][0] - l1[1][0] == 0 and l2[0][0] - l2[1][0] == 0):
		#do they have the same x value?
		if (l1[0][0] == l2[0][0]):
			#do the y segments overlap?
			l1y_min = min(l1[0][1], l1[1][1]) 
			l1y_max = max(l1[0][1], l1[1][1])
			l2y_min = min(l2[0][1], l2[1][1]) 
			l2y_max = max(l2[0][1], l2[1][1])  
			if not (l1y_max < l2y_min or l1y_min > l2y_max):
				return True

	return False

#draw a line on the screen and check if it intersects with any other
def draw_line(l):
	colour = line_colour
	for k in lines:
		if intersect(l,k) and k != l:
			colour = [125,225,125]
	start = (int(l[0][0]), int(l[0][1]))
	end = (int(l[1][0]), int(l[1][1]))
	pygame.draw.line(screen, colour, start, end, 5)

#check there are no intersections between two sets of lines
def no_intersections_lines_lines(lines1, lines2):
	for l in lines1:
		for k in lines2:
			if intersect(l,k):
				return False
	return True

#check if there are any overlaps between two sets of lines
def no_overlaps_lines_lines(lines1, lines2):
	for l in lines1:
		for k in lines2:
			if lines_overlap(l,k):
				return False
				#colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
				#start = (int(l[0][0]), int(l[0][1]))
				#end = (int(l[1][0]), int(l[1][1]))
				#pygame.draw.line(screen, colour, start, end, 20)
				#start = (int(k[0][0]), int(k[0][1]))
				#end = (int(k[1][0]), int(k[1][1]))
				#pygame.draw.line(screen, colour, start, end, 20)
				#pygame.display.flip()
	return True

#check there are to intersections between a set of boxes and a set of lines
def no_intersections_lines_clusters(lines, clusters):
	for l in lines:
		for c in clusters:
			if collide_line_box(l,c):
				return False
	return True

#check there are to overlaps between a set of boxes and a set of lines
def no_overlaps_lines_clusters(lines, clusters):
	for l in lines:
		for c in clusters:
			if overlap_line_box(l,c):
				return False
	return True

#test if some new lines don't collide with anything
def lines_no_collides(lines, new_lines, add_lines, clusters, test_cluster):
	if (no_intersections_lines_lines(new_lines, lines) and
	no_overlaps_lines_lines(new_lines, lines) and 
	no_intersections_lines_lines(new_lines, add_lines) and
	no_overlaps_lines_lines(new_lines, add_lines) and 							
	no_intersections_lines_clusters(new_lines, clusters) and 
	no_overlaps_lines_clusters(new_lines, clusters) and
	no_intersections_lines_clusters(new_lines, [test_cluster]) and
	no_overlaps_lines_clusters(new_lines, [test_cluster])):
		return True
	return False

class cluster:
	def __init__(self):
		#make a random box
		grid_step = 50
		i,j = random.randint(1,width//grid_step), random.randint(1,height//grid_step)
		self.x,self.y = i*grid_step, j*grid_step
		self.w,self.h = random.randint(1,3)*grid_step,random.randint(1,3)*grid_step
		#center of the box
		self.xc = self.x + 0.5*self.w
		self.yc = self.y + 0.5*self.h

		#colour
		self.colour = random.choice(colours)
		self.connector_colour = self.colour
		while self.connector_colour == self.colour:
			self.connector_colour = random.choice(colours)

		#connectors
		self.connectors = []
		if True:#random.choice([True,False]):
			self.connectors.append([int(self.xc),int(self.y)])
		if True:# random.choice([True,False]):
			self.connectors.append([int(self.x + self.w), int(self.yc)])
		if True:# random.choice([True,False]):
			self.connectors.append([int(self.xc),int(self.y + self.h)])
		if True:# random.choice([True,False]):
			self.connectors.append([int(self.x), int(self.yc)])

		#which other clusters does this one connect to?
		self.neighbours = []


	def draw(self):
		pygame.draw.rect(screen,self.colour,[self.x,self.y,self.w,self.h])
		#draw the positions of your connectors
		for c in self.connectors:
			if c:
				pygame.draw.circle(screen, self.connector_colour, c, 8)



clusters = [] #list of all the boxes on the screen
lines = []; #list of all the current connectors
def reset():
	screen.fill(background_colour)
	global clusters
	global lines
	clusters = []
	lines = []
	for i in range(1000):
		#make a random box
		test_cluster = cluster()
		#check if it fits on the screen or collides with any other box
		if (collide_rect_screen_and_rects(test_cluster, 20) 
			and no_intersections_lines_clusters(lines, [test_cluster])
			and no_overlaps_lines_clusters(lines, [test_cluster])):
			#check if the cluster can be connected to at least one other
			#list of lines to add if this cluster is accepted
			add_lines = []
			#for each cluster
			for c in clusters:
				for co in c.connectors:
					for do in test_cluster.connectors:
						#check they are relatively close
						if distance(co,do) < 200:
							#draw a connection between any open connectors
							mid1 = [0.5*(co[0] + do[0]), co[1]]
							mid2 = [0.5*(co[0] + do[0]), do[1]]
							new_lines = [[co, mid1], [mid1,mid2], [mid2,do]]
							#if that connection doesn't cross any other
							if (co in c.connectors and do in test_cluster.connectors and
								lines_no_collides(lines, new_lines, add_lines, clusters, test_cluster)):
									#add those lines to the total connection
									add_lines += new_lines
									#add a neighbour to the test_cluster
									test_cluster.neighbours.append(c)
							#try the connection vertically instead
							else:
								mid1 = [co[0], 0.5*(co[1] + do[1])]
								mid2 = [do[0], 0.5*(co[1] + do[1])]
								new_lines = [[co, mid1], [mid1,mid2], [mid2,do]]
								if (co in c.connectors and do in test_cluster.connectors and
									lines_no_collides(lines, new_lines, add_lines, clusters, test_cluster)):
									#add those lines to the total connection
									add_lines += new_lines
									#add a neighbour to the test_cluster
									test_cluster.neighbours.append(c)
			#finally add the cluster to the screen
			if len(clusters) == 0 or  len(test_cluster.neighbours) > 0:
				clusters.append(test_cluster)
				lines += add_lines

	#if len(clusters) < 10:
	#	reset()

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
	       

	#screen.fill(background_colour)

	for c in clusters:
		c.draw()

	for l in lines:
		draw_line(l)

	pygame.display.flip()
	
	

pygame.quit()