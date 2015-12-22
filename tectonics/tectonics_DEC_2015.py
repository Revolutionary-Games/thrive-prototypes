#a simple test for collisions of a sphere
#the quaternion rotation method is used for the rotation
#and pure Euclidean distance is used for collisions.
#a quaternion is represented as a 4 vector, [a,b,c,d]

import pygame
import math
import random
from pygame.locals import *

#pygame setup
background_colour = (255,255,255)
(width, height) = (700, 700)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Collisions on a Sphere')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

#distance in space between two points, not distance on a sphere
def euclidean_distance(quat1, quat2):
	return math.sqrt((quat1[0] - quat2[0])**2 +
					(quat1[1] - quat2[1])**2 + 
					(quat1[2] - quat2[2])**2 + 
					(quat1[3] - quat2[3])**2)

#the size of a quaternion
def norm(quat):
	return euclidean_distance([0,0,0,0], quat)

#make a quaternion unit size
def normalise(quat):
	this_norm = norm(quat)
	if this_norm == 0:
		this_norm += 0.001
	return [float(quat[0])/this_norm,
			float(quat[1])/this_norm,
			float(quat[2])/this_norm,
			float(quat[3])/this_norm]

#find the conjugate of a quaternion (same process as complex conjugate)
def conjugate(quat):
	return [quat[0], -quat[1], -quat[2], -quat[3]]

#find the inverse of a quat, q = p^-1 such that pq = [1,0,0,0]
def invert(quat):
	this_norm = norm(quat)
	if this_norm == 0:
		this_norm += 0.001
	this_conjugate = conjugate(quat)
	return [float(this_conjugate[0])/(this_norm**2),
			float(this_conjugate[1])/(this_norm**2),
			float(this_conjugate[2])/(this_norm**2),
			float(this_conjugate[3])/(this_norm**2)]

#multiply two quaternions using Hamiltons method
def multiply(quat1, quat2):
	return [quat1[0]*quat2[0] - quat1[1]*quat2[1] - quat1[2]*quat2[2] - quat1[3]*quat2[3],
			quat1[0]*quat2[1] + quat1[1]*quat2[0] + quat1[2]*quat2[3] - quat1[3]*quat2[2],
			quat1[0]*quat2[2] - quat1[1]*quat2[3] + quat1[2]*quat2[0] + quat1[3]*quat2[1],
			quat1[0]*quat2[3] + quat1[1]*quat2[2] - quat1[2]*quat2[1] + quat1[3]*quat2[0]]

#class for the points
class point:
	def __init__(self):
		#begin at a random point, the last three components are x,y,z coord
		self.pos = [0, random.uniform(-1,1),  random.uniform(-1,1),  random.uniform(-1,1)]
		#ensure this point is on the sphere
		self.pos = normalise(self.pos)
		#make a random axis of rotation
		self.axis_of_rotation = [0, 
						random.uniform(-1,1),  
						random.uniform(-1,1),  
						0]
		if self.pos[3] == 0:
			self.pos[3] += 0.001
		#ensure the axis of rotation is perpendicular to the point
		#this is to ensure the point travels along a great circle
		self.axis_of_rotation[3] = -1*(self.pos[1]*self.axis_of_rotation[1] + 
									self.pos[2]*self.axis_of_rotation[2])/self.pos[3]
		self.axis_of_rotation = normalise(self.axis_of_rotation)
		#set speed of rotation
		self.speed = 0.01
		self.axis_of_rotation[0] = self.speed
		self.colour = [255,0,0]

	def move(self):
		#use the rotation forumula to move the point
		#p' = qpq^-1, p = self.pos, q = self.axis_of_rotation
		q_minus_one = invert(self.axis_of_rotation)
		p_q_minus_one = multiply(self.pos, q_minus_one)
		self.pos = multiply(self.axis_of_rotation, p_q_minus_one)

	#display the point
	def display(self):
		pygame.draw.circle(screen, self.colour, 
			[int((300*self.pos[1]) + (float(width)/2)), 
			int((300*self.pos[2]) + (float(height)/2))], 5)

	#check for collisions using only euclidean distance
	def collide(self):
		collide = False
		for point in points:
			if euclidean_distance(self.pos,point.pos) <= 0.3 and point != self:
				collide = True	

		if collide: 
			self.colour = [0,0,255]
		else:
			self.colour = [255,0,0]

#initialise
points= []
for i in range(5):
	points.append(point())

pause = False
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	            pause = not pause


	if not pause:
		for point in points:
			point.move()
			point.collide()
			point.display()

	pygame.display.flip()

	clock.tick(60)
	        
pygame.quit()