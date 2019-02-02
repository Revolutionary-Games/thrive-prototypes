import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,0,0)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be Books')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

# a spine is made of a sequence of vertebrae, each can be a different size
class vertebra:
	def __init__(self, x, y, angle, parent_size):
		self.x = x #location of the vertabra
		self.y = y
		self.angle = angle #only the angle of the first vertebra matters atm
		self.size = random.randint(2,parent_size) #how big is this section of the fish?
		self.offset = 0 # how much is this section wiggling right now?
		self.skin_right = [x,y] #where is the skin in relation to the spinr
		self.skin_left = [x,y]

class fish:
	def __init__(self):
		self.size = random.randint(5,15)#how fat is this fish
		self.length = random.randint(3,10)#how long is this fish
		#keep an array of the spine pieces
		self.spine = [vertebra(random.randint(0,width), random.randint(0,height), random.uniform(-3,3), self.size)] #the pieces of the fish
		self.colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)] #what colour is this fish?
		
		self.frequency = random.uniform(0.005,0.03) #frequency is how fast you wiggle
		self.turn = 0 #turn is how much the whole fish is turning over time

		#add some spine pieces
		for i in range(self.length):
			x = self.spine[0].x
			y = self.spine[0].y
			#add them in a straight line along the angle of the fish, though they will be updated every time step
			self.spine.append(vertebra(x + 2*self.size*(i + 1)*math.cos(self.spine[0].angle), y + 2*self.size*(i + 1)*math.sin(self.spine[0].angle), self.spine[0].angle, self.size))


	def update(self):
		head = self.spine[0]
		#every 100ms frames change how much the fish is turning
		if t % 100 == 0:
			self.turn = random.uniform(-0.02, 0.02)
		head.angle += self.turn
		#move the whole fish, faster frequency means faster movement
		head.x -= 200*self.frequency*math.cos(head.angle)
		head.y -= 200*self.frequency*math.sin(head.angle)
		#offset is the smount of wiggle, it gets propagated through the fish
		head.offset = 20*math.sin(self.frequency*t)
		#keep the fish on the screen
		head.x = head.x % width
		head.y = head.y % height
		#start the skin at the side of the head
		head.skin_right = [head.x + head.size*math.sin(self.spine[0].angle),head.y - head.size*math.cos(self.spine[0].angle)]
		head.skin_left = [head.x - head.size*math.sin(self.spine[0].angle),head.y + head.size*math.cos(self.spine[0].angle)]
		#for each piece of spine in reverse
		for i in range(len(self.spine) - 1):
			j = len(self.spine) - 1 - i
			r = self.spine[j - 1]
			s = self.spine[j]
			#work out you position if offset = 0
			x = self.spine[0].x + 2*self.size*j*math.cos(self.spine[0].angle)
			y = self.spine[0].y + 2*self.size*j*math.sin(self.spine[0].angle)
			#work out a normalised vector between this ideal position and the head
			vx = (self.spine[0].x - x)/(2*self.size*(j + 1))
			vy = (self.spine[0].y - y)/(2*self.size*(j + 1))
			#the offset is inherited from the piece ahead of you
			s.offset += 0.3*(r.offset - s.offset)
			s.offset *= 1.07 #boost offset so it doesn't die out
			#your position is your ideal position when offset = 0 + your offset perpendicular to the spine
			s.x = x - vy*s.offset
			s.y = y + vx*s.offset
			#work out your skin positions relative to the spine
			multiplier = 5
			if i == 0:
				multiplier = 1
			s.skin_right = [s.x - multiplier*vy*s.size, s.y + multiplier*vx*s.size]
			s.skin_left = [s.x + multiplier*vy*s.size, s.y - multiplier*vx*s.size]


			

	def draw(self):
		for i in range(len(self.spine)):
			s = self.spine[i]
			#draw a circle for each spine piece
			pygame.draw.circle(screen, self.colour, [int(s.x), int(s.y)], int(s.size))
			if i > 0:
				r = self.spine[i - 1]
				#draw a line between consective skin positions
				pygame.draw.line(screen, self.colour, [int(s.skin_right[0]), int(s.skin_right[1])], [int(r.skin_right[0]), int(r.skin_right[1])], 2)
				pygame.draw.line(screen, self.colour, [int(s.skin_left[0]), int(s.skin_left[1])], [int(r.skin_left[0]), int(r.skin_left[1])], 2)




my_fish = []
for i in range(10):
	my_fish.append(fish())
t = 0

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	       

	screen.fill(background_colour)

	for f in my_fish:
		f.update()
		f.draw()

	pygame.display.flip()

	t += clock.tick(60)
	
	

pygame.quit()