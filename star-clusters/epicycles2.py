# I did a bit of messing around with the hill spheres idea
# it's setup so no two hillspheres intersect (so you are always in one and only one)
# and the planets + satellites trace out equal areas in equal time (I think)


import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1600, 800)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Epicycles')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

# scale changes so your spaceship is always on the screen
scale = 0.5

def hill(dist, m_c, m_p):
    '''
    Returns the full Hill radius of the child body.
    '''
    return dist * (m_c / (3.0 * m_p)) ** (1/3.0)

#calculate the x,y coordinates from angle and radius
def calculate_xy(body):
	if body.parent is not None:
		body.x = body.parent.x + body.r*math.cos(body.phase)
		body.y = body.parent.y + body.r*math.sin(body.phase)
	else:
		body.x = 0
		body.y = 0

# when adding a new planet this finds the closest you can put it so the hill spheres wont cross
def findradius(body):
	offset = 0
	running = True
	while running:
		r = body.parent.used_space + offset
		ourhill = hill(r, body.m, body.parent.m)
		if r - ourhill <= body.parent.used_space:
			offset += 10
		elif r + ourhill >= body.parent.hill:
				body.r = 0
				body.hill = 0
				running = False
		else: 
			body.r = r
			body.hill = ourhill
			body.parent.used_space += r + ourhill 
			running = False

#usual euclidean distance
def distance(x,y,x1,y1):
	return math.sqrt((x-x1)**2 + (y - y1)**2)

# change the scale if the spaceship is off the screen
def checkdisplay():
	global scale
	distsun = distance(spaceship.positions[-1][0], bodies[0].x, spaceship.positions[-1][1], bodies[0].y)
	if distsun*scale >= (min(width,height)/2):
		scale = scale*0.99
	if distsun*scale <= (min(width,height)/4):
		scale = scale*1.01
	scale = min(scale, 1)

# class of planets and satellistes
class body:
	def __init__(self, mass = 10, phase = 0, parent = None, name = None):
		self.name = name
		self.parent = parent
		self.m = mass
		if parent is not None:
			findradius(self)
		else:
			self.r = 0
			self.hill = 4000 # the orbital radius, not radius of the body itself
		self.phase = phase	
		self.x = 0
		self.y = 0
		calculate_xy(self)
		self.speed = 10.0/(self.r + 1)**2
		self.used_space = 0
		
		
# draw self
	def display(self):
		pygame.draw.circle(screen, (255,0,0), (int(self.x*scale) + width/2,int(self.y*scale) + height/2), int(scale*self.m/2))

#orbit the parent
	def update(self):
		self.phase += self.speed
		if self.phase >= math.pi*2:
			self.phase -= math.pi*2
		calculate_xy(self)

# spaceship class, changel velocity and the initial positions append for new initial conditions
class particle:
	def __init__(self):
		self.positions = []
		self.positions.append([100, 0])
		self.velocity = [-0.1, -1]
		self.ingravityofname = ''

#draw the last 500 positions you were in
	def display(self):
		for i in self.positions[-500:]:
			pygame.draw.circle(screen, (0,0,255), (int(i[0]*scale) + width/2,int(i[1]*scale) + height/2), 1)

#check which hillsphere you are in
	def whichgravity(self):
		body = None
		for i in bodies:
			dist = distance(self.positions[-1][0], self.positions[-1][1], i.x, i.y)
			if dist <= i.hill:
				body = i
				finaldist = dist
		return (body, dist)

#move and display the name of which hillspere you are in, if something goes wrong accelerate based on the sun
	def move(self):
		currentposx = self.positions[-1][0]
		currentposy = self.positions[-1][1]
		inhillof = self.whichgravity()
		if inhillof[0] != None:
			accelx = 100*inhillof[0].m*(inhillof[0].x - currentposx)/(inhillof[1]**3)
			accely = 100*inhillof[0].m*(inhillof[0].y - currentposy)/(inhillof[1]**3)
			self.velocity[0] += accelx
			self.velocity[1] += accely
		else:
			distsun = distance(currentposx, currentposy,0,0)
			accelx = (- currentposx)/distsun**3
			accely = (- currentposy)/distsun**3
			self.velocity[0] += accelx
			self.velocity[1] += accely
		if inhillof[0] != None and inhillof[0].name != self.ingravityofname:
			print 'in gravity of ' + inhillof[0].name
			self.ingravityofname = inhillof[0].name
		currentposx += self.velocity[0]
		currentposy += self.velocity[1]
		self.positions.append([currentposx,currentposy])


#initialise
bodies = []
bodies.append(body( mass = 50, parent = None, name = 'Sun'))
numberofplanets = 5
numberofsatellites = 20
for i in range(numberofplanets):
	phase = random.uniform(0, 2*math.pi)
	bodies.append(body(mass = 20 ,phase = phase, parent = bodies[0], name = 'planet ' + str(i)))
for i in range(numberofsatellites):
	choice = random.randint(1,numberofplanets)
	phase = random.uniform(0, 2*math.pi)
	bodies.append(body(mass = 10 ,phase = phase, parent = bodies[choice], name = 'satellite ' + str(i)))

#cleanup any planets and satellites there wasn't room for
for i in bodies:
	if i.r == 0 and i.hill == 0:
		bodies.remove(i)

spaceship = particle()


#main loop

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False

	screen.fill(background_colour)

	for i in bodies:
		i.display()
		i.update()
	spaceship.display()
	spaceship.move()

	checkdisplay()

	pygame.display.flip()

pygame.quit()