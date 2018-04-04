import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Basic ai')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

cell_speed = 3
number_of_cells = 20

def distance(a,b,x,y):
	return ((a - x)**2 + (b - y)**2)**0.5

def norm(a,b):
	return distance(a,b,0,0)

def normalise(a,b):
	n = norm(a,b)
	if n != 0:
		return a/n, b/n 
	else:
		return 0,0

class cell:
	def __init__(self, max_str):
		self.strength = random.randint(0,max_str)
		self.x = random.randint(100,width - 100)
		self.y = random.randint(100,height - 100)
		self.dx = 0
		self.dy = 0
		self.angle = random.uniform(-3,3)

	def update(self):
		#move randomly
		self.angle += random.uniform(-0.1,0.1)
		des_angle = self.angle
		#you are hunting for food if you have not been scared
		hunting = True
		for c in cells:
			#if you are touching another cell
			if distance(self.x, self.y, c.x, c.y) < 10:
				if c.strength > self.strength:
					cells.remove(self)
			#if you can perceive another cell
			elif distance(self.x, self.y, c.x, c.y) < 100:
				#if you are stronger and want to eat them and are not scared
				if self.strength >= 2*c.strength and hunting == True:
					des_angle = math.atan2(-self.x + c.x, -self.y + c.y)
				#if you are not strong enough run away and get scared
				else:
					hunting = False
					des_angle = math.atan2(self.x - c.x, self.y - c.y)

		#work out which way to turn to get to your desired angle
		turn = des_angle - self.angle
		#keep all angles in [-pi, pi]
		if turn < -math.pi:
			turn += math.pi*2
		if turn > math.pi:
			turn -= math.pi*2
		#add some amount of the turn
		self.angle += 0.1*(turn)

		#keep angle in the right range
		if self.angle < -math.pi:
			self.angle += math.pi*2
		if self.angle > math.pi:
			self.angle -= math.pi*2

		self.d_x = math.sin(self.angle)
		self.d_y = math.cos(self.angle)

		#update your velocity and position
		self.dx, self.dy = normalise(self.d_x, self.d_y)
		self.x += cell_speed*self.dx
		self.y += cell_speed*self.dy
		#check for boundary collision

		if self.x > width:
			self.x -= width
		if self.x < 0:
			self.x += width
		if self.y > height:
			self.y -= height
		if self.y < 0:
			self.y += height


	def draw(self):
		colour = [10*self.strength, 255 - 10*self.strength, 0]
		pygame.draw.circle(screen, colour, (int(self.x), int(self.y)), 15)
		#textsurface = myfont.render(str(self.strength), True, [255,255,255])
		#screen.blit(textsurface,(int(self.x - 10), int(self.y - 10)))
		


cells = []
for i in range(number_of_cells):
	cells.append(cell(20))

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	       

	screen.fill(background_colour)

	for c in cells:
		c.update()
		c.draw()

	if len(cells) < number_of_cells:
		cells.append(cell(10))

	pygame.display.flip()

	clock.tick(60)
	
	

pygame.quit()