import pygame
import math
import random
from pygame.locals import *

clock = pygame.time.Clock()

#setup

background_colour = (255,255,255)
(width, height) = (1100, 800)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Noise')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

trade_factor = 8
bonus_factor = 5
increment = 0.1
nearby = 400
number_of_towns = 20
number_of_people = 5
migration_threshold = 1

text = False

def distance(town1, town2):
	return math.sqrt((town1.x - town2.x)**2 + (town1.y - town2.y)**2)

def average_happiness(town):
	total_happiness = 0
	number_of_people = len(town.people)
	if number_of_people == 0:
		return random.randint(0,3)
	else:
		for i in range(number_of_people):
			total_happiness += town.people[i].happiness
		return total_happiness/number_of_people

class town:
	def __init__(self, identity):
		self.x = random.randint(50,width - 50)
		self.y = random.randint(50,height - 50)
		self.price_point = [5,4,3,1,-1]
		self.bonus = random.randint(0,3)
		if self.bonus == 0:
			self.colour = (0,255,0)
		elif self.bonus == 1: 
			self.colour = (255,0,0)
		elif self.bonus == 2: 
			self.colour = (0,0,255)
		elif self.bonus == 3: 
			self.colour = (100,100,100)
		self.id = identity 
		self.neighbours = []
		self.link_strength = []
		self.people = []
		for i in range(number_of_people):
			self.people.append(person(self))

	def display_trade(self):
		for i in range(len(self.neighbours)):
			pygame.draw.line(screen, (200,200,200), (self.x,self.y), 
				(self.neighbours[i].x, self.neighbours[i].y), self.link_strength[i])

	def display_map(self):		
		pygame.draw.circle(screen, self.colour, (self.x, self.y), 2*len(self.people), 0)
		label = myfont.render(str(self.id) , 1, (0,0,0))
		screen.blit(label, (self.x + 10 + 2*len(self.people), self.y + 10 + 2*len(self.people)))
		

	def display_chart(self, count):
		label = myfont.render(str(self.id) + ":", 1, (0,0,0))
		screen.blit(label, (50 + 100*count, 40))
		for i in range(len(self.price_point)):
			label = myfont.render(str(self.price_point[i]), 1, (0,0,0))
			screen.blit(label, (50 + 100*count, 60 + 20*i))

	def display_people(self, count, base):
		for i in range(len(self.people)):
			label = myfont.render(str(int(self.people[i].money))  + " : " + str(self.people[i].happiness), 1, (0,0,0))
			screen.blit(label, (50 + 100*count, base + 60 + 20*i))

	def set_neighbourd(self):
		close = nearby
		while self.neighbours == []:
			for town in towns:
				if distance(self, town) <= close and town != self:
					self.neighbours.append(town)
					self.link_strength.append(1)
			close += 10

class person:
	def __init__(self, town):
		self.money = 0
		self.happiness = 0
		self.town = town

	def work(self):
		chosen_produce = 0
		best_price_produce = 0
		number_produced = 0
		for i in range(len(town.price_point)):
			is_bonus = False
			if self.town.bonus == i:
				value = math.exp(town.price_point[i])*bonus_factor
				is_bonus = True
			else:
				if i == 4: value = (math.exp(town.price_point[4]) 
					- math.exp(town.price_point[1] + increment)
					- math.exp(town.price_point[2] + increment)	
					- math.exp(town.price_point[3] + increment))	
				else: value = math.exp(town.price_point[i])				
			if value >= best_price_produce:
				best_price_produce = value
				chosen_produce = i
				if is_bonus: number_produced = bonus_factor
				else: number_produced = 1

		best_price_trade = 0
		chosen_trade = 0
		chosen_neighbour = 0
		chosen_trade_factor = 0
		for j in range(len(self.town.neighbours)):
			temp_trade_factor = max(0,trade_factor 
				- int(distance(self.town, self.town.neighbours[j])/100))
			for i in range(len(self.town.neighbours[j].price_point)):
				value = -1*temp_trade_factor*(math.exp(self.town.neighbours[j].price_point[i] + increment) - math.exp(self.town.price_point[i]))
				if value >= best_price_trade:
					best_price_trade = value
					chosen_trade = i
					chosen_neighbour = j
					chosen_trade_factor = temp_trade_factor

		if best_price_produce >= best_price_trade:
			if chosen_produce != 4:
				for i in range(number_produced):
					self.money += math.exp(self.town.price_point[chosen_produce])
					self.town.price_point[chosen_produce] -= increment
			else: 
				self.money += best_price_produce
				self.town.price_point[4] -= increment
				self.town.price_point[3] += increment
				self.town.price_point[2] += increment
				self.town.price_point[1] += increment
			if text: print "Produce " + str(chosen_produce) + " in town " + str(self.town.id) 

		else:
			for i in range(chosen_trade_factor):
				self.money += math.exp(self.town.price_point[chosen_trade]) - math.exp(self.town.neighbours[chosen_neighbour].price_point[chosen_trade] + increment)
				self.town.price_point[chosen_trade] -= increment
				self.town.neighbours[chosen_neighbour].price_point[chosen_trade] += increment
			self.town.link_strength[chosen_neighbour] += chosen_trade_factor
			if text: print "Trade " + str(chosen_trade) + " in town " + str(self.town.id) + " with town " + str(self.town.neighbours[chosen_neighbour].id)


	def buy(self):
		self.happiness = 0
		shopping = True
		while shopping:
			for i in range(len(self.town.price_point)):
				cost = math.exp(self.town.price_point[i] + increment)
				if self.money >= cost:
					self.money -= cost
					self.happiness += 1
					self.town.price_point[i] += increment
			if self.money <= math.exp(self.town.price_point[0] + increment) + 1:
				shopping = False

towns = []

for i in range(number_of_towns):
	towns.append(town(i))

for town in towns:
	town.set_neighbourd()

map_mode = True
pause = True
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	        	map_mode = not map_mode
	        if event.key == K_RETURN:
	        	pause = not pause


	screen.fill(background_colour)

	#pygame.time.wait(1000)

	if map_mode:
		for town in towns:
			town.display_trade()
		for town in towns:
			town.display_map()
	else:
		label = myfont.render("Towns", 1, (0,0,0))
		screen.blit(label, (50, 10))
		count = 0
		for town in towns:
			town.display_chart(count)
			count += 1
		base =  60 + 20*count
		label = myfont.render("People", 1, (0,0,0))
		screen.blit(label, (50, base + 20))
		count = 0
		for town in towns:
			town.display_people(count, base)
			count += 1

	if not pause:
		for town in towns:
			random.shuffle(town.people)
			for i in range(len(town.link_strength)):
				town.link_strength[i] = int(math.ceil(0.7*town.link_strength[i]))
			for people in town.people:
				people.work()

		for town in towns:
			for people in town.people:
				people.buy()

		migrant_town = random.choice(towns)
		target_town = random.choice(towns)
		if average_happiness(target_town) >= average_happiness(migrant_town) + 1:
			if len(migrant_town.people) >= 2:
				migrant = random.choice(migrant_town.people)
				migrant_town.people.remove(migrant)
				target_town.people.append(migrant)
				migrant.town = target_town
		

	pygame.display.flip()

pygame.quit()