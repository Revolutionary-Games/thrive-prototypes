import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 800)

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

def norm(a,b):
	return math.sqrt(a**2 + b**2 + 0.01)

def fight(i,j):
	#determine the outcome of the fight
	choice = random.randint(0, animals[i].strength + animals[j].strength)
	if choice <= animals[i].strength:
		animals[i].memory_events[j].append(1)
		animals[j].memory_events[i].append(0)
		animals[j].x = random.randint(0, width)
		animals[j].y = random.randint(0, height) 
		animals[j].target = False
		winner = i
		loser = j
	else:
		animals[i].memory_events[j].append(0)
		animals[j].memory_events[i].append(1)
		animals[i].x = random.randint(0, width)
		animals[i].y = random.randint(0, height)
		animals[i].target = False
		winner = j
		loser = i
	#check to see if you have the right strength value and learn if not
	expectation = animals[winner].memory_strength[winner] / (animals[winner].memory_strength[winner] + 
		animals[winner].memory_strength[loser] + 0.01)
	observed = sum(animals[winner].memory_events[loser])/(len(animals[winner].memory_events[loser]) + 0.01)
	faster_learning = 10*(observed - expectation)**2
	if observed >= expectation:
		if animals[winner].memory_strength[loser] >= 5*faster_learning:
			animals[winner].memory_strength[loser] -= 5*faster_learning
		animals[winner].memory_strength[winner] += 5*faster_learning
	else:
		animals[winner].memory_strength[loser] += 5*faster_learning
		if animals[winner].memory_strength[winner] >= 5*faster_learning:
			animals[winner].memory_strength[winner] -= 5*faster_learning

	#loser learns less
	animals[loser].memory_strength[winner] += 1
	if animals[loser].memory_strength[loser] >= 5*faster_learning:
		animals[loser].memory_strength[loser] -= 5*faster_learning
	


class animal:
	def __init__(self, number):
		self.x = random.randint(0, width)
		self.y = random.randint(0, height)
		self.dx = 0
		self.dy = 0 
		self.colour = (100,100,100)
		self.number = number
		self.strength = random.randint(0,100)
		self.memory_strength = []
		self.memory_events = []
		self.mode = 'neutral'
		self.speed = random.uniform(base_speed/2,base_speed)
		self.target = False
		self.distances = []
		self.memory_full = False
		for i in range(number_of_animals):
			self.distances.append(0)
		for i in range(number_of_animals):
			self.memory_strength.append(50)
			self.memory_events.append([])

	def display(self, see_in_brain = 0):
		if self.mode == 'neutral': 
			self.colour = (100,100,100)
		elif self.mode == 'fear': 
			self.colour = (255,100,100)
		elif self.mode == 'hunt': 
			self.colour = (100,255,100)
		if self.number == see_in_brain:
			self.colour = (100,100,255)
		pygame.draw.circle(screen, self.colour, (int(self.x),int(self.y)), 15)
		message = str(self.strength)
		label = myfont.render(message, 1, (0,0,0))
		screen.blit(label, (int(self.x - 12),int(self.y - 35)))
		if self.number == see_in_brain:
			colour = (0,0,0)
			if self.memory_full: colour = (255,0,0)
			message = str(see_in_brain)
			label = myfont.render(message, 1, colour)
			screen.blit(label, (width + 50, 50))
			deviation = 0
			for i in range(number_of_animals):
				colour = (0,0,0)
				if i == see_in_brain: colour = (255,0,0)
				message = str(animals[i].strength)
				label = myfont.render(message, 1, colour)
				screen.blit(label, (width + 50, 100 + 25*i))
				message = str(self.memory_strength[i])
				label = myfont.render(message, 1, colour)
				screen.blit(label, (width + 100, 100 + 25*i))
				deviation += abs(animals[i].strength - self.memory_strength[i])
			message = 'Sd = ' + str(deviation/number_of_animals)
			label = myfont.render(message, 1, colour)
			screen.blit(label, (width + 50, 100 + 25*number_of_animals + 50))




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

	def think(self):
		# forget
		for i in range(len(self.memory_events)):
			if len(self.memory_events[i]) >= amount_of_memory:
				self.memory_events[i].remove(self.memory_events[i][0])
				self.memory_full = True

		#check for low self esteem
		choice = random.uniform(0,1)
		if choice <= 0.003 and self.memory_strength[self.number] <= 50:
			self.memory_strength[self.number] += 1
			#compensate for drift
			sum_of_memory = 0
			for i in range(number_of_animals):
				sum_of_memory += self.memory_strength[i]
			if sum_of_memory >= number_of_animals*50:
				for i in range(number_of_animals):
					self.memory_strength[i] = self.memory_strength[i]*number_of_animals*50/(sum_of_memory + 0.01)


		#check for fear
		fear = 0
		for i in range(number_of_animals):
			self.distances[i] = (distance1(self,animals[i]))
			if i != self.number and i != self.target:
				fear += 30*self.memory_strength[i]/(self.distances[i] + 0.01)
		if fear >= self.memory_strength[self.number]:
			self.dx = 0
			self.dy = 0
			for i in range(number_of_animals):
				fear_factor = 0
				if i != self.number:
					fear_factor += self.memory_strength[i]/(self.distances[i] + 0.01)
				direct = direction(animals[i], self)
				self.dx += direct[0]*fear_factor
				self.dy += direct[1]*fear_factor
			normed = norm(self.dx, self.dy)
			self.dx = self.dx*self.speed/normed
			self.dy = self.dy*self.speed/normed
			self.mode = 'fear'
			return

		#check for hunt
		closest = False
		distance = 10000
		for i in range(number_of_animals):
				temp_distance = distance1(self, animals[i])
				if temp_distance <= distance and i != self.number:
					distance = temp_distance
					closest = animals[i]
					closest_number = i
		if distance <= 1000 and self.memory_strength[closest_number] <= self.memory_strength[self.number]:
			self.mode = 'hunt'
			self.target = closest_number
			direction_towards = direction(self, closest)
			self.dx = direction_towards[0]
			self.dy = direction_towards[1]
			normed = norm(self.dx, self.dy)
			self.dx = self.dx*self.speed/normed
			self.dy = self.dy*self.speed/normed
			return

		#be neutral
		else: 
			self.mode = 'neutral'
			self.target = False 
			if distance <= 20:
				direction_away = direction(closest, self)
				self.dx = direction_away[0]
				self.dy = direction_away[1]
				normed = norm(self.dx, self.dy)
				self.dx = self.dx*self.speed/normed
				self.dy = self.dy*self.speed/normed
			else:
				chance = random.uniform(0,1)
				if chance <= 0.005:
					self.dx = random.uniform(-0.5,0.5)
					self.dy = random.uniform(-0.5,0.5)


number_of_animals = 10
amount_of_memory = 50
base_speed = 5

#initialise when you press SPACE
def setup():
	global animals
	animals = []
	for i in range(number_of_animals):
		animals.append(animal(i))

setup()
see_in_brain = 0
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
	        if event.key == K_DOWN and see_in_brain <= (number_of_animals - 2):
	            see_in_brain += 1
	        if event.key == K_UP and see_in_brain >= 1:
	            see_in_brain -= 1


	screen.fill(background_colour)

	for i in animals:
		i.think()
		i.move()
		i.display(see_in_brain)

	for i in range(number_of_animals):
		for j in range(i, number_of_animals):
			if distance1(animals[i], animals[j]) <= 5 and i !=j:
				fight(i, j)

	pygame.display.flip()

pygame.quit()