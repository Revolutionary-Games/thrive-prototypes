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
	if x + w + 5 > width or x - w < 0 or y + h + 5 > height or y - h < 0:
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

#lerp
def lerp(a,b,t):
	return [a[0]*t + b[0]*(1 - t), a[1]*t + b[1]*(1 - t)]

#cut a line into 3 pieces, horiztonal, vertical, horizontal and draw it
def draw_step_line(a,b):
	start = (int(a.x + 0.5*a.w), int(a.y + 0.5*a.h))
	end = (int(b.x + 0.5*b.w), int(b.y + 0.5*b.h))
	mid1 = (0.5*(start[0] + end[0]), start[1])
	mid2 = (0.5*(start[0] + end[0]), end[1])
	colour = [125,125,225]
	if a.highlight or b.highlight:
		colour = [125,225,125]			
	pygame.draw.line(screen, colour, start, mid1, 2)
	pygame.draw.line(screen, colour, mid1, mid2, 2)
	pygame.draw.line(screen, colour, mid2, end, 2)

#draw a line on the screen and check if it intersects with any other
def draw_line(l):
	colour = line_colour
	for k in lines:
		if intersect(l,k) and k != l:
			colour = [125,225,125]
	start = (int(l[0][0]), int(l[0][1]))
	end = (int(l[1][0]), int(l[1][1]))
	pygame.draw.line(screen, colour, start, end, 5)


def draw_rounded_box(x,y,w,h):
	arc_size = 0.5 #how rounded should the corners be? 0 = square, 1 = circle
	thickness = 5 #how thick should the lines be
	colour = line_colour
	#draw the 4 arcs in the corners
	z = min(w,h)
	offset = thickness/2
	for i in range(5):
		pygame.draw.arc(screen, colour, [x + w - arc_size*z,y,arc_size*z,arc_size*z], 0 + 0.01*i, math.pi/2, thickness)
		pygame.draw.arc(screen, colour, [x,y,arc_size*z,arc_size*z], math.pi/2 + 0.01*i, math.pi, thickness)
		pygame.draw.arc(screen, colour, [x,y + h - arc_size*z,arc_size*z,arc_size*z], -math.pi + 0.01*i, -math.pi/2, thickness)
		pygame.draw.arc(screen, colour, [x + w - arc_size*z,y + h - arc_size*z,arc_size*z,arc_size*z], -math.pi/2 + 0.01*i, 0, thickness)
	#draw the 4 lines connecting the sides
	offset = z/30
	pygame.draw.line(screen, colour, [x + 0.5*arc_size*z, y + offset], [x + w - 0.5*arc_size*z,y +  offset], thickness)
	pygame.draw.line(screen, colour, [x + 0.5*arc_size*z, y + h - offset], [x + w - 0.5*arc_size*z,y + h - offset], thickness)
	pygame.draw.line(screen, colour, [x + offset, y+ 0.5*arc_size*z], [x + offset,y+ h - 0.5*arc_size*z], thickness)
	pygame.draw.line(screen, colour, [x+ w - offset, y+ 0.5*arc_size*z], [x + w - offset,y+ h - 0.5*arc_size*z], thickness)



#get the center of a box
def center(box):
	return [box.x + 0.5*box.w, box.y + 0.5*box.h]

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

#connect two points with only diagonal or straight lines
def compute_subway_line(a,b):
	dy = b[1] - a[1] 
	dx = b[0] - a[0] 
	mid = [width/2,height/2]
	flipx = 1
	if dx < 0:
		flipx = -1
		dx = -dx
	if dy < -2*dx:
		t = dx
		mid = [a[0], a[1] + dy + t]
	elif dy < -0.5*dx:
		if dx > -dy:
			t = -dy
			c = dx - t
		else: 
			t = dx
			c = dy - t
		mid = [a[0] + flipx*t, a[1] - t]
	elif dy < 0.5*dx:
		t = abs(dy)
		mid = [a[0] + flipx*dx - flipx*t, a[1]]
	elif dy < 2*dx:
		if dx > dy:
			t = dy
			c = dx - t
		else: 
			t = dx
			c = dy - t
		mid = [a[0] + flipx*t, a[1] + t]
	else:
		t = dx
		mid = [a[0], a[1] + dy - t]
	
	#pygame.draw.line(screen,[100,100,200], a, mid, 10)
	#pygame.draw.line(screen,[100,100,200], mid, b, 10)
	return [[a,mid],[mid,b]]

#return points on the border of a box
def box_points(c1,c2):
	#get the right quadrant for each box
	dy = c2.y + 0.5*c2.h - c1.y - 0.5*c1.h
	dx = c2.x + 0.5*c2.w - c1.x - 0.5*c1.w
	offset = 0
	#top
	if dy < -abs(dx):
		return ((c1.x + 0.5*c1.w, c1.y - offset), (c2.x + 0.5*c2.w, c2.y + c2.h + offset))
	#left, right
	if dy < abs(dx):
		#right
		if dx > 0:
			return ((c1.x + c1.w + offset, c1.y + 0.5*c1.h), (c2.x - offset, c2.y + 0.5*c2.h))
		else:
			return ((c1.x - offset, c1.y + 0.5*c1.h), (c2.x + c2.w + offset, c2.y + 0.5*c2.h))
	#bottom
	return ((c1.x + 0.5*c1.w, c1.y + c1.h + offset), (c2.x + 0.5*c2.w, c2.y - offset))


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

	#this fn is not currently used
	def draw_connections(self):
		for n in self.neighbours:
			start = (int(self.x + 0.5*self.w), int(self.y + 0.5*self.h))
			end = (int(n.x + 0.5*n.w), int(n.y + 0.5*n.h))
			pygame.draw.line(screen, [125,125,225], start, end, 2)
			

	def draw(self):
		pygame.draw.rect(screen, background_colour, (int(self.x - 3), int(self.y - 3), int(self.w + 6), int(self.h + 6)))
		
		colour = line_colour
		if self.highlight:
			colour = [125,225,125]
		#pygame.draw.rect(screen, colour, (int(self.x), int(self.y), int(self.w), int(self.h)), 5)
		draw_rounded_box(int(self.x - 5), int(self.y - 5), int(self.w + 10), int(self.h + 10))

#a patch node
class node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.colour = random.choice(colours)

	def draw(self):
		pygame.draw.circle(screen, self.colour,(int(self.x), int(self.y)), 10)

node_size = 35
clusters = []
lines = []
def reset():
	#add some random clusters to the map
	global clusters
	global lines
	clusters = []
	lines = []
	counter = 0
	while counter < 10000:
		counter += 1
		#make the new cluster somewhat gridwise with the old one
		#pick a random size for the new cluster
		n = random.randint(1,5)
		m = random.randint(1,3)
		m = max(1,min(m,5-n))
		w = node_size*m
		h = node_size*n
		#pick a place for it
		x = random.randint(0,width)
		y = random.randint(0,height)
		#try to line it up with a previous box
		if (len(clusters) > 0):
			c = random.choice(clusters)
			if random.choice([True,False]):
				x = c.x
			else:
				y = c.y
		#if the cluster is fully on the screen
		if collide_rect_screen(x,y,w,h) == False:
			#check the cluster does not collide with any others
			collided = False		
			for c in clusters:	
				padding = 50		
				if collide_rects(x -padding,y-padding,w+2*padding,h+2*padding,c.x,c.y,c.w,c.h):
					collided = True
					break
			#check the cluster does not collide with any lines
			for l in lines:		
				if collide_line_box(l,cluster(x,y,w,h,n,m)):
					collided = True
					break
			#if it is on the screen and not colliding with any others
			if collided == False:
				#add all connections you can
				lines2 = []
				#for each other cluster
				for c in clusters:
					#if that cluster is close
					if distance(x,y,c.x,c.y) < 200: 
						#draw a line to that cluster
						#line = [center(cluster(x,y,w,h,n,m)), center(c)]
						#nlines = compute_subway_line(center(cluster(x,y,w,h,n,m)), center(c))
						bp = box_points(cluster(x,y,w,h,n,m),c)
						nlines = compute_subway_line(bp[0], bp[1])
						#check if that line intersects any lines already drawn
						intersection = False
						for l in lines:
							for k in nlines:
								if intersect(k,l):
									intersection = True
						for l in lines2:
							for k in nlines:
								if intersect(k,l):
									intersection = True
						#check if either line intersects any boxes
						for k in lines:
							for d in clusters:
								if d != c:
									if collide_line_box(k,d):
										intersection = True
						#if not then add that line to the map
						if intersection == False:
							for k in nlines:
								lines2.append(k)

				#add a cluster only if it is the first or it is connected to at lease one other
				if len(lines2) > 0 or len(clusters) == 0:
					clusters.append(cluster(x,y,w,h,n,m))
					lines = lines + lines2[:]

	#add patches to each random cluster
	for c in clusters:
		for i in range(c.m):
			x = c.x + i*node_size + node_size/2
			for j in range(c.n):
				y = c.y + j*node_size + node_size/2
				c.nodes.append(node(x,y))

	#add connections between clusters
	#for c in clusters:
	#	while 1:
	#		d = random.choice(clusters)
	#		if distance(d.x,d.y,c.x,c.y) < 300 and d != c and c not in d.neighbours:
	#			c.neighbours.append(d)
				#lines.append([center(d), center(c)])
	#			break


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

	#for c in clusters:
	#	c.draw_connections()

	for l in lines:
		draw_line(l)


	for c in clusters:
		c.draw()
		for n in c.nodes:
			n.draw()

	pygame.display.flip()
	
	

pygame.quit()