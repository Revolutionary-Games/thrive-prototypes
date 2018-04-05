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

start_number_of_cells = 8
num_plants = 5
max_number_of_cells = 20
max_str = 20
max_spd = 4
max_view = 100
min_reproduce_age = 2
max_max_age = 30

FPS = 60

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
	def __init__(self, start_pos, stats):
		self.strength = stats[0] #random.uniform(0,max_str)
		self.x = start_pos[0]#random.randint(100,width - 100)
		self.y = start_pos[1]#random.randint(100,height - 100)
		self.dx = 0
		self.dy = 0
		self.angle = random.uniform(-3,3)
		self.cell_speed = stats[1]#random.uniform(0,4)
		self.aggression = stats[2]#random.randint(0,100)
		self.perception = stats[3]#random.randint(25,100)
		self.age = 0
		self.max_age = stats[4]
		self.reproduce_age = stats[5]
		if self.max_age < self.reproduce_age:
			self.reproduce_age = min(self.max_age-2,min_reproduce_age)
			self.max_age = max(self.max_age,min_reproduce_age+2)

	def update(self):
		#move randomly
		self.angle += random.uniform(-0.1,0.1)
		des_angle = self.angle
		self.age += 1/FPS
		if self.age > self.max_age:
			cells.remove(self)
		#you are hunting for food if you have not been scared
		hunting = True
		for c in cells:
			#if you are touching another cell
			if distance(self.x, self.y, c.x, c.y) < 5:
				if c.strength > self.strength and self.age > 1/FPS*0.25:
					cells.remove(self)
					if c.age>c.reproduce_age:
						c.reproduce()
			#if you can perceive another cell
			elif distance(self.x, self.y, c.x, c.y) < self.perception:
				#if you are stronger and want to eat them and are not scared
				attack = self.aggression+100*(self.strength-c.strength)/self.strength
				if attack>100 and hunting == True:
					des_angle = math.atan2(-self.x + c.x, -self.y + c.y)
				#if you are not strong enough run away and get scared
				elif attack<0:
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
		self.angle += 0.2*(turn)

		#keep angle in the right range
		if self.angle < -math.pi:
			self.angle += math.pi*2
		if self.angle > math.pi:
			self.angle -= math.pi*2

		self.d_x = math.sin(self.angle)
		self.d_y = math.cos(self.angle)

		#update your velocity and position
		self.dx, self.dy = normalise(self.d_x, self.d_y)
		self.x += self.cell_speed*self.dx
		self.y += self.cell_speed*self.dy
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
		colour = [int(10*self.strength), int(255 - 10*self.strength), 0]
		pygame.draw.circle(screen, colour, (int(self.x), int(self.y)), 15)
		if self.perception > 3:
			pygame.draw.circle(screen, colour, (int(self.x), int(self.y)), int(self.perception), 3)
		textsurface = myfont.render(str(int(self.aggression)), True, [0,0,0])
		screen.blit(textsurface,(int(self.x - 10), int(self.y - 10)))
		
	def reproduce(self):
		child_strength = max(min(random.gauss(self.strength,1),max_str),0)
		child_speed = max(min(random.gauss(self.cell_speed,0.2),max_spd),0)
		child_aggression = max(min(random.gauss(self.aggression,5),100),0)
		child_perception = max(min(random.gauss(self.perception,5),max_view),0)
		child_pos = (self.x+random.randint(5,10)*random.choice([-1,1]),self.y+random.randint(5,10)*random.choice([-1,1]))
		child_max_age = max(min(random.gauss(self.perception,5),max_max_age),0)
		child_reproduce_age = max(min(random.gauss(self.perception,5),max_max_age),min_reproduce_age)
		if len(cells) < max_number_of_cells:
			cells.append(cell(child_pos,[child_strength,child_speed,child_aggression,child_perception,child_max_age,child_reproduce_age]))
		


cells = []

for i in range(start_number_of_cells):
	pos = (random.randint(100,width - 100),random.randint(100,height - 100))
	stats = [random.uniform(0,max_str),random.uniform(0,max_spd),random.randint(0,100),random.randint(0,max_view),
	random.uniform(0,max_max_age),random.uniform(min_reproduce_age,max_max_age)]
	cells.append(cell(pos,stats))
	
for i in range(num_plants):
	pos = (random.randint(10,width - 100),random.randint(10,height - 100))
	stats = [0,0,0,0,100,12]
	cells.append(cell(pos,stats))

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	       

	screen.fill(background_colour)
	n_plant = 0
	for c in cells:
		c.update()
		c.draw()
		if c.strength==0 and c.cell_speed == 0 and c.aggression == 0 and c.perception == 0:
			n_plant+=1

	for i in range(num_plants-n_plant):
		pos = (random.randint(10,width - 100),random.randint(10,height - 100))
		stats = [0,0,0,0,100,12]
		cells.append(cell(pos,stats))
	
	pygame.display.flip()

	clock.tick(FPS)
	
	

pygame.quit()