import pygame
import math
import random
from pygame.locals import *
from operator import attrgetter

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Creatures')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

draw_scaling = 0.5
Hooke_constant = 0.2
t = 0
pressure_coefficient = 0
drag_tangent = 1
drag_normal = 1

def distance(a,b):
	return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def direction(a,b,c):
	vec1 = [b.x - a.x, b.y - a.y]
	vec2 = [c.x - a.x, c.y - a.y]
	cross = vec1[0]*vec2[1] - vec1[1]*vec2[0]
	return cross

def dot(a,b,c):
	vec1x = b.x - a.x
	vec1y = b.y - a.y
	vec2x = c.x - a.x
	vec2y = c.y - a.y
	norm1 = distance(a,b)
	norm2 = distance(a,c)
	return (vec1x*vec2x + vec1y*vec2y)/(norm2*norm1 + 0.0001)

def check_inside_tri(tri, cell):
	if ((math.copysign(1,direction(tri.verts[0], tri.verts[1], cell)) != 
			math.copysign(1,direction(tri.verts[0], tri.verts[2], cell)))
		and (math.copysign(1,direction(tri.verts[0], tri.verts[1], cell)) == 
			math.copysign(1,direction(tri.verts[1], tri.verts[2], cell)))):
			return True
	else:
		return False

class triangle:
	def __init__(self, a, b, c):
		self.verts = []
		self.verts.append(a)
		self.verts.append(b)
		self.verts.append(c)
		self.colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

	def draw(self):
		for i in range(len(self.verts)):
			pygame.draw.line(screen, 
				self.colour, 
				[int(width/2 + draw_scaling*(self.verts[i].x)), 
				int(height/2 + draw_scaling*self.verts[i].y)], 
				[int(width/2 + draw_scaling*self.verts[(i + 1) % len(self.verts)].x), 
				int(height/2 + draw_scaling*self.verts[(i + 1) % len(self.verts)].y)], 3)
		
		#pygame.draw.line(screen, 
		#	self.colour, [self.verts[0].x + offset, self.verts[0].y], [self.verts[1].x + offset, self.verts[1].y], 3)
		#pygame.draw.line(screen, 
		#	self.colour, [self.verts[1].x + offset, self.verts[1].y], [self.verts[2].x + offset, self.verts[2].y], 3)
		#pygame.draw.line(screen, 
		#	self.colour, [self.verts[0].x + offset, self.verts[0].y], [self.verts[2].x + offset, self.verts[2].y], 3)



class cell:
	def __init__(self, parent, location):
		self.parent = parent
		self.x = location[0] + random.randint(-200,200)
		self.y = location[1] + random.randint(-200,200)
		self.colour = [255,0,0]
		self.included = False
		self.amplitude = random.uniform(0,3)
		self.frequency = random.uniform(1,2)
		self.offset = random.uniform(0, 6.26) #0 to 2 pi
		self.forces = []

	def draw(self):
		temp_colour = self.colour
		if self in self.parent.external_cells: #or self in self.parent.hull:
			temp_colour = [0,0,255]
		pygame.draw.circle(screen, temp_colour, 
			[int(width/2 + draw_scaling*self.x), 
			int(height/2 + draw_scaling*self.y)], 10)

class edge:
	def __init__(self, a, b):
		self.nodes = [a,b]
		self.colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
		self.x = (a.x + b.x)/2
		self.y = (a.y + b.y)/2
		self.rest_length = 0

	def draw(self):
		pygame.draw.line(screen, 
			self.colour, [int( width/2 + draw_scaling*self.nodes[0].x), 
						int( height/2 + draw_scaling*self.nodes[0].y)], 
						[int( width/2 + draw_scaling*self.nodes[1].x), 
						int(height/2 + draw_scaling*self.nodes[1].y)], 3)

class chamber:
	def __init__(self, parent, cells):
		self.parent = parent
		self.cells = cells
		self.edges = []
		#when sent a list of cells you are made from go and find the edges they are connected to
		for Edge in parent.edges:
			if Edge.nodes[0] in self.cells and Edge.nodes[1] in self.cells:
				self.edges.append(Edge)
		self.initial_volume = self.compute_volume()
		self.x = 0
		self.y = 0

	def compute_volume(self):
		vol = 0
		for i in range(len(self.cells) - 2):
			vol += 0.5*abs(direction(self.cells[i], self.cells[i + 1], self.cells[i + 2]))
		return vol

	def compute_center(self):
		self.x = 0
		self.y = 0
		for Cell in self.cells:
			self.x += Cell.x
			self.y += Cell.y
		self.x /= len(self.cells)
		self.y /= len(self.cells)


	def draw(self):
		for Edge in self.edges:
			Edge.draw()



class creature:
	def __init__(self):
		#layout some cells in the creature
		self.location = [0,0] #location in space of the creature
		self.external_cells = [] #list of cells which are exposed to the environment
		self.cells = [] #list of cells which make up the creature 
		self.chambers = [] #list of pressure chambers inside the creature, each chamber is formed of edges
		self.edges = [] #list of edges in the creature, each edge connects 2 cells

		for i in range(15):
			self.cells.append(cell(self, self.location))

		#if the cells are too close move them a litte
		done = False
		counter = 0
		while not done:
			counter += 1
			found = False
			for Cell in self.cells:
				for Cell2 in self.cells:
					if distance(Cell, Cell2) <= 80 and Cell is not Cell2:
						Cell.x += random.randint(-10,10)
						Cell.y += random.randint(-10,10)
						found = True

			if not found or counter >= 100000:
				done = True

		#compute the convex hull of the cells
		#sort the cells in order of their x coord
		self.cells.sort(key = attrgetter('x'))

		self.hull = [] 
		self.hull.append(self.cells[0])

		#go around the top of the set adding each new point to the set
		#this is the gift wrapping algorithm, you shoudl never turn left if you go clockwise around the edge
		#if you turn right it's ok, if you turn left then delete the previous point added and try again
		for i in range(1, len(self.cells)):
			while ((len(self.hull) >= 2) and 
				(direction(self.hull[-2], self.hull[-1], self.cells[i]) <= 0)):
				self.hull = self.hull[:-1]
			self.hull.append(self.cells[i])

		#do the same for going around the bottom of the set
		self.hull2 = []
		self.hull2.append(self.cells[-1])

		#no left turns allowed
		for i in range(1, len(self.cells)):
			while ((len(self.hull2) >= 2) and 
				(direction(self.hull2[-2], self.hull2[-1], self.cells[-(i + 1)]) <= 0)):
				self.hull2 = self.hull2[:-1]
			self.hull2.append(self.cells[-(i + 1)])

		self.hull2 = self.hull2[1:]
		self.hull = self.hull + self.hull2

		#cover the set in triangles
		self.tris = []

		for i in range(2, len(self.hull) - 1):
			self.tris.append(triangle(self.hull[i], self.hull[i-1], self.hull[0]))

		#work out the centre of the shape
		counter = 0
		av_x = 0
		av_y = 0
		for Cell in self.cells:
			av_x += Cell.x
			av_y += Cell.y
			counter+=1 

		av_x/=counter
		av_y/=counter

		self.centre_of_gravity = [av_x, av_y]

		#make a triangulation
		done = False
		while not done:
			all_included = True
			for Cell in self.cells:		
				if Cell not in self.hull and not Cell.included:
					#find the triangle you are in
					for Tri in self.tris:
						if check_inside_tri(Tri, Cell):
							#if you are inside a triangle remove that triangle and make 3 new ones
							a = Tri.verts[0]
							b = Tri.verts[1]
							c = Tri.verts[2]
							self.tris.remove(Tri)
							self.tris.append(triangle(a,b,Cell))
							self.tris.append(triangle(b,c,Cell))
							self.tris.append(triangle(a,c,Cell))
							Cell.included = True
				#if there are cells which are not included they may be on a straight line, if so move them
				if Cell not in self.hull and not Cell.included:
					all_included = False
					Cell.x += random.uniform(0.01,0.02)*(av_x - Cell.x)
					Cell.y += random.uniform(0.01,0.02)*(av_y - Cell.y)
			if all_included == True:
				done = True

		#flip any triangles such that the arrangement is Delauny
		doing = True
		while doing:
			done = True
			working = True
			#for each pair of triangles
			for Tri in self.tris:
				if working:
					for Tri2 in self.tris:
						if working:
							#work out how many vertices they share
							shared_verts = []
							for Vert in Tri.verts:
								if Vert in Tri2.verts:
									shared_verts.append(Vert)
							#if they share 2 vertices then they are adjactent
							if len(shared_verts) == 2:
								#work out which vertices they do not share, these are the roots
								for Vert in Tri.verts:
									if Vert not in shared_verts:
										left_root = Vert
								for Vert in Tri2.verts:
									if Vert not in shared_verts:
										right_root = Vert
								#compute the angle of the triangles at their roots
								angle_a = math.acos(dot(left_root, shared_verts[0], shared_verts[1]))
								angle_b = math.acos(dot(right_root, shared_verts[0], shared_verts[1]))
								#print angle_a, ", ", angle_b
								#if this angle is greater than pi then the triangle needs to be flipped
								if angle_a + angle_b > math.pi:
									working = False
									done = False
									self.tris.remove(Tri)
									self.tris.remove(Tri2)
									self.tris.append(triangle(left_root, right_root, shared_verts[0]))
									self.tris.append(triangle(left_root, right_root, shared_verts[1]))

			if done:
				doing = False

		#create the list of pressure chambers
		self.chambers = self.tris[:]
		#create the list of external cells
		self.external_cells = self.hull[:]

		#compute the gabriel graph from the delauny triangulation
		#this means removing any edges ab such that any other point lies in the circle of diameter(ab)
		#add all edges

		for Tri in self.tris:
			for Vert in Tri.verts:
				for Vert2 in Tri.verts:
					found = False
					for Edge in self.edges:
						if (Edge.nodes[0] == Vert and Edge.nodes[1] == Vert2 or
							Edge.nodes[1] == Vert and Edge.nodes[0] == Vert2):
							found = True
					if not found:
						self.edges.append(edge(Vert, Vert2))

		edges2 = []
		#remove edges which do not satisfy the gabriel condition
		for Edge in self.edges:
			dist = distance(Edge.nodes[0], Edge.nodes[1])/2
			removed = False
			for Cell in self.cells:
				if (distance(Cell, Edge) <= dist and Cell is not Edge.nodes[0] 
					and Cell is not Edge.nodes[1] and not removed):
					removed = True
					#if the edge is on the inside then combine the chambers it divides
					connected = []
					for Tri in self.chambers:
						if (Edge.nodes[0] in Tri.verts and
								Edge.nodes[1] in Tri.verts):
							connected.append(Tri)
					if len(connected) == 2:
						for Vert in connected[1].verts:
							if Vert not in connected[0].verts:
								connected[0].verts.append(Vert)
						self.chambers.remove(connected[1])
					#else the edge is on the outside remove the chamber and mark it's nodes as external
					else:
						for Tri in self.chambers:
							if (Edge.nodes[0] in Tri.verts and
								Edge.nodes[1] in Tri.verts):
								for Vert in Tri.verts:
									if (Vert not in self.external_cells):
										self.external_cells.append(Vert)
								self.chambers.remove(Tri)
			if not removed:
				edges2.append(Edge)

		self.edges = edges2

		#reset the chambers list so it is made of chambers objects
		chambers_old = self.chambers[:]
		self.chambers = []
		for Chamber in chambers_old:
			self.chambers.append(chamber(self, Chamber.verts))

		#get each edge to calculate it's resting length
		for Edge in self.edges:
			Edge.rest_length = distance(Edge.nodes[0], Edge.nodes[1])


	def draw(self):
		for Cell in self.cells:
			Cell.draw()
		#for Tri in self.tris:
		#	Tri.draw()
		for Edge in self.edges:
			Edge.draw()
		#for Chamber in self.chambers:
		#	Chamber.draw()

	def move(self):
		#move cells based on forces
		for Cell in self.cells:
			Cell.forces = [0,0]
		#compute the forces from the springs
		for Edge in self.edges:
			a = Edge.nodes[0]
			b = Edge.nodes[1]
			Edge.x = (a.x - b.x)/2
			Edge.y = (a.y - b.y)/2
			#work out how long the spring wants to be
			new_rest_length = ((1 + a.amplitude*math.sin(a.frequency*t + a.offset) 
				+ b.amplitude*math.sin(b.frequency*t + b.offset)))*Edge.rest_length
			#work out it's current length
			current_length = distance(a,b)
			#work out the direction and magnitude of the force this produces
			force_magnitude = Hooke_constant*(new_rest_length - current_length)
			force_direction = [(a.x - b.x)/(current_length + 0.0001), 
								(a.y - b.y)/(current_length + 0.0001)]
			#add it onto the forces of each end
			a.forces[0] += force_direction[0]*force_magnitude
			a.forces[1] += force_direction[1]*force_magnitude
			b.forces[0] -= force_direction[0]*force_magnitude
			b.forces[1] -= force_direction[1]*force_magnitude

		#compute the forces from the compression of the chambers
		for Chamber in self.chambers:
			Chamber.compute_center()
			vol = Chamber.compute_volume()
			force_magnitude = pressure_coefficient*(1 - vol/Chamber.initial_volume)
			for Edge in Chamber.edges:
				dist = distance(Edge, Chamber)
				force_direction = [(Edge.x - Chamber.x)/dist, (Edge.y - Chamber.y)/dist]
				Edge.nodes[0].forces[0] += force_direction[0]*force_magnitude*0.5*Edge.rest_length
				Edge.nodes[0].forces[1] += force_direction[1]*force_magnitude*0.5*Edge.rest_length
				Edge.nodes[1].forces[0] += force_direction[0]*force_magnitude*0.5*Edge.rest_length
				Edge.nodes[1].forces[1] += force_direction[1]*force_magnitude*0.5*Edge.rest_length

		#compute the fluid drag forces
		for Edge in self.edges:
			a = Edge.nodes[0]
			b = Edge.nodes[1]
			if a in self.external_cells and b in self.external_cells:
				pass


		#move the cells based on the net force after all has been added up
		for Cell in self.cells:
			Cell.x += 0.01*Cell.forces[0]
			Cell.y += 0.01*Cell.forces[0]

		#recalculate edge positions
		for Edge in self.edges:
			Edge.x = (Edge.nodes[0].x + Edge.nodes[1].x)/2
			Edge.y = (Edge.nodes[0].y + Edge.nodes[1].y)/2

worm = creature()


running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        


	screen.fill(background_colour)

	worm.move()
	worm.draw()
	t += 0.05
	if t > 1000000:
		t = 0

	for i in range(10):
		for j in range(10):
			X = (width/2) -500 + 100*i - worm.location[0]
			Y = (height/2) -500 + 100*j - worm.location[0]
			pygame.draw.circle(screen, [0,0,0], [int(X), int(Y)], 2)

	pygame.display.flip()
	

pygame.quit()