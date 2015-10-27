import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1600, 800)
(X_shift, Y_shift) = (width/2, height)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Better Trees')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

definition = 100 #how many layers the mesh has, increase for more polys
rotary_definition = 8 #how many columns the mesh has, increse for more polys
naturalness = 3 #how randome the mesh is, decrese for a smoother mesh

def distance(a,b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

#if you know where a trunk starts and at what angle it is find where it ends
def get_end_point(length_range, angle_phi, angle_psi, angle_range, initial_point):
	length = random.uniform(length_range*1.1, 0.9*length_range)
	out_angle_phi = angle_phi + random.uniform(-angle_range, angle_range)
	out_angle_psi = angle_psi + random.uniform(-angle_range, angle_range)
	return [initial_point[0] + length*math.sin(out_angle_phi)*math.cos(out_angle_psi),
		initial_point[1] + length*math.sin(out_angle_phi)*math.sin(out_angle_psi),
		initial_point[2] + length*math.cos(out_angle_phi)]

#knowing the beginning and end of a branch put two midpoints in, shifted off centre
def get_intermediate_points(initial_point, end_point, percentage_bendy, number_of_intermediate = 2):
	length = distance(initial_point, end_point)
	intermediate_points = []
	for i in range(number_of_intermediate):
		bendy_angle = random.uniform(0,2*math.pi)
		bendy_distance = length*percentage_bendy*random.uniform(0,1)
		interp_1 = float(number_of_intermediate - (i+1))/(number_of_intermediate + 1)
		interp_2 = float(i+1)/(number_of_intermediate + 1)
		x = (interp_1*initial_point[0] + interp_2*end_point[0] 
			+ math.cos(bendy_angle)*bendy_distance*math.sin(math.pi*interp_2))
		y = (interp_1*initial_point[1] + interp_2*end_point[1] 
			+ math.sin(bendy_angle)*bendy_distance*math.sin(math.pi*interp_2))
		z = (interp_1*initial_point[2] + interp_2*end_point[2])
		intermediate_points.append([x,y,z])
	return intermediate_points

#knowing the 4 points (initial, mid1, mid2, end) return a smooth Bezier curve between them
def get_bezier(p1,p2,p3,p4,t):
	return [p1[0]*(1-t)**3 + 3*p2[0]*t*(1-t)**2 + 3*p3[0]*(1-t)*t**2 + p4[0]*t**3,
			p1[1]*(1-t)**3 + 3*p2[1]*t*(1-t)**2 + 3*p3[1]*(1-t)*t**2 + p4[1]*t**3,
			p1[2]*(1-t)**3 + 3*p2[2]*t*(1-t)**2 + 3*p3[2]*(1-t)*t**2 + p4[2]*t**3]

#class for the branches
class branch:
	def __init__(self):
		#initial constants
		self.initial_point = [0,0,0]
		self.angle_phi = 0
		self.angle_psi = 0
		self.length_range = 700
		self.layers = 10
		self.angle_range = random.uniform(0.1,0.3)
		self.percentage_bendy = random.uniform(0.1,0.3)
		self.thickness = 40
		#find the end point and intermediate points of the branch
		self.end_point = get_end_point(self.length_range, self.angle_phi, self.angle_psi, self.angle_range, self.initial_point)
		self.intermediate_points = get_intermediate_points(self.initial_point, self.end_point, self.percentage_bendy)
		#find the smooth curve which is the core of the branch
		self.bezier_points = []
		for i in range(definition + 1):
			self.bezier_points.append(get_bezier(self.initial_point,self.intermediate_points[0], self.intermediate_points[1], self.end_point, (float(i)/definition)))
		#wrap the branch in mesh_points
		self.mesh_points = []
		self.mesh_triangles = []
		for i in range(len(self.bezier_points)):
			for j in range(rotary_definition):
				self.mesh_points.append([self.bezier_points[i][0] + self.thickness*math.cos(2*math.pi*j/rotary_definition), 
					self.bezier_points[i][1] + self.thickness*math.sin(2*math.pi*j/rotary_definition), self.bezier_points[i][2]])
		#randomly shift the points a little bit
		for i in range(len(self.mesh_points)):
			self.mesh_points[i][0] += random.randint(0,naturalness)
			self.mesh_points[i][1] += random.randint(0,naturalness)
			self.mesh_points[i][2] += random.randint(0,naturalness)
		#create the mesh_triangles from the mesh_points
		for i in range(len(self.bezier_points) - 1):
			for j in range((rotary_definition)):
				self.mesh_triangles.append([self.mesh_points[rotary_definition*i + j], 
					self.mesh_points[rotary_definition*i + j + 1],
					self.mesh_points[rotary_definition*(i+1) + j]])
		for i in range(len(self.bezier_points) - 1):
			for j in range((rotary_definition - 1)):
				self.mesh_triangles.append([self.mesh_points[rotary_definition*(i + 1) + j], 
					self.mesh_points[rotary_definition*(i + 1) + j + 1],
					self.mesh_points[rotary_definition*i + ((j + 1) % rotary_definition)]])

	def display_points(self, rotation):
		ch_intermediate_points = self.intermediate_points
		ch_intermediate_points.append(self.end_point)
		ch_intermediate_points.append(self.initial_point)
		for pts in ch_intermediate_points:
			screen_x_0 = math.cos(rotation)*pts[0] - math.sin(rotation)*pts[1]
			pygame.draw.circle(screen, [255,0,0], (int(X_shift + screen_x_0), int(Y_shift - pts[2])), 10)


	def display_bezier(self,rotation):
		for i in range(definition):
			pts = self.bezier_points[i]
			screen_x_0 = math.cos(rotation)*pts[0] - math.sin(rotation)*pts[1]
			pygame.draw.circle(screen, [0,255,0], (int(X_shift + screen_x_0), int(Y_shift - pts[2])), 5)

	def display_mesh_points(self, rotation):
		for i in range(len(self.mesh_points)):
			pts = self.mesh_points[i]
			screen_x_0 = math.cos(rotation)*pts[0] - math.sin(rotation)*pts[1]
			pygame.draw.circle(screen, [0,0,255], (int(X_shift + screen_x_0), int(Y_shift - pts[2])), 1)

	def display_mesh_triangles(self, rotation, filled_triangles):
		for i in range(len(self.mesh_triangles)):
			#draw a line from self.mesh_triangles 1 -> 2, 2 -> 3 and 3 -> 1.
			pts = []
			for j in range(3):
				screen_x_0 = math.cos(rotation)*self.mesh_triangles[i][j][0] - math.sin(rotation)*self.mesh_triangles[i][j][1]
				screen_x_1 = math.cos(rotation)*self.mesh_triangles[i][(j + 1) % 3][0] - math.sin(rotation)*self.mesh_triangles[i][(j + 1) % 3][1]
				pygame.draw.line(screen, [0,0,255], (int(X_shift + screen_x_0), int(Y_shift - self.mesh_triangles[i][j][2])), (int(X_shift + screen_x_1), int(Y_shift - self.mesh_triangles[i][(j + 1) % 3][2])), 1)

				screen_x_0 = math.cos(rotation)*self.mesh_triangles[i][j][0] - math.sin(rotation)*self.mesh_triangles[i][j][1]
				pts.append([int(X_shift + screen_x_0), int(Y_shift - self.mesh_triangles[i][j][2])])
			if filled_triangles: pygame.draw.polygon(screen, [0,0,255], [pts[0], pts[1], pts[2]], 0)

def setup():
	global trunk
	trunk = branch()

setup()

points = True
bezier = True
mesh_points = True
mesh_triangles = True
filled_triangles = False
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_q:
	            points = not points
	        if event.key == K_w:
	            bezier = not bezier
	        if event.key == K_e:
	            mesh_points = not mesh_points
	        if event.key == K_r:
	            mesh_triangles = not mesh_triangles
	        if event.key == K_t:
	        	filled_triangles = not filled_triangles
	        if event.key == K_SPACE:
	        	setup()


	screen.fill(background_colour)

	pos = pygame.mouse.get_pos()
	rotation = float(pos[0])/300

	if points:
		trunk.display_points(rotation)

	if bezier:
		trunk.display_bezier(rotation)

	if mesh_points:
		trunk.display_mesh_points(rotation)

	if mesh_triangles:
		trunk.display_mesh_triangles(rotation, filled_triangles)

	pygame.display.flip()
	

pygame.quit()