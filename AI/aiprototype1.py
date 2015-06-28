import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 500)

screen = pygame.display.set_mode((width + 200, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Intelligent')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

def distance(x1,y1,x2,y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distance1(a,b):
	return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def direction(a,b):
	return [b.x - a.x, b.y - a.y]

# the other is all the microbes on screen that are not the player
class other:
	def __init__(self, number):
		self.x = random.randint(0, width)
		self.y = random.randint(0, height)
		self.dx = random.uniform(-0.1,0.1)
		self.dy = random.uniform(-0.1,0.1)
		self.type = random.choice(['predator','prey','neither'])
		if self.type == 'predator': self.colour = (255,0,0)
		elif self.type == 'prey': self.colour = (0,255,0)
		else: self.colour = (0,0,255)
		self.number = number

#draw yourself both on the screen and in the column on the right
	def display(self):
		pygame.draw.circle(screen, self.colour, (int(self.x),int(self.y)), 10)
		pygame.draw.circle(screen, self.colour, (width + 50,50 + 50*self.number), 10)
		guess = (0,0,0)
		if animala.memory[self.number] >= 1:
			guess = (255,0,0)
		elif animala.memory1[self.number] >= 1:
			guess = (0,255,0)
		elif animala.memory2[self.number] >= 1:
			guess = (0,0,255)
		pygame.draw.circle(screen, guess, (width + 100,50 + 50*self.number), 10)


	def move(self):
		self.x += self.dx
		self.y += self.dy
		if self.x >= width:
			self.x = width
			self.dx *= -1
		if self.x <= 0:
			self.x = 0
			self.dx *= -1
		if self.y >= height:
			self.y = height
			self.dy *= -1
		if self.y <= 0:
			self.y = 0
			self.dy *= -1

#if you are a predator move towards the animal, if prey move away
	def think(self):
		if self.type == 'predator':
			if distance1(self, animala) <= 200:
				direct = direction(self,animala)
				normed_direction = distance(direct[0],direct[1],0,0) * 5 + 0.01
				self.dx = direct[0] / normed_direction 
				self.dy = direct[1] / normed_direction
			if distance1(self, animala) <= 5:
				animala.kill(self.number)

		if self.type == 'prey':
			if distance1(self, animala) <= 200:
				direct = direction(self,animala)
				normed_direction = distance(direct[0],direct[1],0,0) * 5 + 0.01
				self.dx = -direct[0] / normed_direction 
				self.dy = -direct[1] / normed_direction


class animal:
	def __init__(self):
		self.x = random.randint(0, width)
		self.y = random.randint(0, height)
		self.dx = 0
		self.dy = 0
		#there are 3 memory banks which is a bit of a waste, it's easy to see how to make this 1
		self.memory = []
		self.memory1 = []
		self.memory2 = []
		self.distances = []
		for i in range(number_of_others):
			self.memory.append(0)
			self.memory1.append(0)
			self.memory2.append(0)
			self.distances.append(10)
		self.colour = (100,100,100)
		self.mode = 'hunting'

	def display(self):
		pygame.draw.circle(screen, self.colour, (int(self.x),int(self.y)), 15)

	def move(self):
		self.x += self.dx
		self.y += self.dy
		if self.x >= width:
			self.x = width
		if self.x <= 0:
			self.x = 0
		if self.y >= height:
			self.y = height
		if self.y <= 0:
			self.y = 0
		if ((self.x == width and self.y == height) or (self.x == 0 and self.y == height) 
			or (self.x == 0 and self.y == 0) or (self.x == width and self.y == 0)):
			self.x = width/2
			self.y = height/2

#what to do if you are killed by a predator
	def kill(self, number):
		self.x = random.randint(0, width)
		self.y = random.randint(0, height)
		self.memory[number] += 10

#the actual ai
	def think(self):
		#slowly forget the information you have
		if random.uniform(0,1) <= 0.003:
			for i in range(number_of_others):			
				self.memory[i] = self.memory[i]*0.95
				if self.memory[i] <= 1:
					self.memory[i] = 0
				self.memory1[i] = self.memory1[i]*0.95
				if self.memory1[i] <= 1:
					self.memory1[i] = 0
				self.memory2[i] = self.memory2[i]*0.95
				if self.memory2[i] <= 1:
					self.memory2[i] = 0
		#work out how much danger you think you are in, sum (50*remembered danger of n/distance to n)
		fear = 0
		for i in range(number_of_others):
			self.distances[i] = (distance1(self,others[i]))
			fear += 50*self.memory[i]/(self.distances[i] + 0.01)
		if fear >= 1:
			self.dx = 0
			self.dy = 0
			for i in range(number_of_others):
				fear_factor = 0
				fear_factor += self.memory[i]/(self.distances[i] + 0.01)
				direct = direction(others[i], self)
				self.dx += direct[0]*fear_factor
				self.dy += direct[1]*fear_factor
			norm = self.dx**2 + self.dy**2 + 0.01
			self.dx = self.dx*5/norm
			self.dy = self.dy*5/norm
			self.colour = (255,100,100)
			self.mode = 'fear'
		#if not afaid then hunt your closes neighbour, if you think they are tasty or unknown
		else:
			if self.x >= width/2: self.dx = -0.1
			else: self.dx = 0.1
			if self.y >= height/2: self.dy = -0.1
			else: self.dy = 0.1	
			self.colour = (100,100,100)
			self.mode = 'hunting'
			choice = 0
			choice_dist = 100000
			for i in range(len(self.distances)):
				if self.distances[i] <= choice_dist:
					choice = i
					choice_dist = self.distances[i]
			#this condition is for "not a predator and not a neither"
			if self.memory[choice] == 0 and self.memory2[choice] == 0:
				direct = direction(self, others[choice])
				self.dx = direct[0]
				self.dy = direct[1]
				norm = math.sqrt(self.dx**2 + self.dy**2 + 0.01)
				self.dx = self.dx*0.5/norm
				self.dy = self.dy*0.5/norm
				self.colour = (0,255,0)
				#what to do when you catch something, remember
				if self.distances[choice] <= 5:
					if others[choice].type == 'prey':
						self.memory1[choice] += 10
						others[choice].x = random.randint(0, width)
						others[choice].y = random.randint(0, height)
					elif others[choice].type == 'neither':
						self.memory2[choice] += 10




number_of_others = 9

#initialise when you press SPACE
def setup():
	global animala, others
	animala = False
	animala = animal()
	others = []
	for i in range(number_of_others):
		others.append(other(i))

setup()
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	            setup()



	        

	screen.fill(background_colour)

	animala.think()
	animala.move()
	animala.display()

	for i in others:
		i.think()
		i.move()
		i.display()

	pygame.display.flip()

pygame.quit()