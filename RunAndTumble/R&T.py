import pygame
import math
import random

bacteria_radius = 7

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Run & Tumble')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

def compound_density(x,y):
	return math.fabs(math.sin(x*(math.pi/100))+math.sin(y*(math.pi/100)))
	
Compound = [[compound_density(x,y) for x in range(height)] for y in range(width)] 

def draw_compounds():
	for x in range(width):
		for y in range(height):
			screen.set_at((x,y), [255*Compound[x][y]/2,0,0])
	
def update_compounds(pos):
	px = int(pos[0])
	py = int(pos[1])
	for x in range(bacteria_radius+1):
		for y in range(bacteria_radius+1):
			screen.set_at(((px+x)%width, (py+y)%height), [255*Compound[(px+x)%width][(py+y)%height]/2,0,0])
			screen.set_at(((px-x)%width, (py-y)%height), [255*Compound[(px-x)%width][(py-y)%height]/2,0,0])
			screen.set_at(((px+x)%width, (py-y)%height), [255*Compound[(px+x)%width][(py-y)%height]/2,0,0])
			screen.set_at(((px-x)%width, (py+y)%height), [255*Compound[(px-x)%width][(py+y)%height]/2,0,0])
	
class bacteria:
	def __init__(self, position, speed, rot_speed):
		self.x = int(position[0])
		self.y = int(position[1])
		self.speed = speed
		self.angle = math.pi*2*random.uniform(0,1)
		self.compounds = Compound[self.x % width][self.y % height]
		self.rot_speed = rot_speed
	
	def update(self):
		b = Compound[self.x][self.y]
		if b <= self.compounds:
			self.turn()
			self.move()
		else:
			self.move()
		self.compounds = b
	
	def turn(self):
		self.angle+=random.uniform(-self.rot_speed,self.rot_speed)
		self.angle = self.angle % (2*math.pi)
	
	def move(self):
		self.x+=self.speed*math.cos(self.angle)
		self.y+=self.speed*math.sin(self.angle)
		self.x = int(self.x % width)
		self.y = int(self.y % height)
		
	def draw(self):
		pygame.draw.circle(screen, [0,255,0], (int(self.x), int(self.y)), bacteria_radius)
		
Bacteria=[]
consume = 0.01

for j in range(10):
	x = random.randint(0,1000)
	y = random.randint(0,600)
	speed = 2
	rot_speed = 45*math.pi/180
	Bacteria.append(bacteria((x,y),speed,rot_speed))
	
draw_compounds()
		
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == pygame.KEYDOWN:
	        if event.key == pygame.K_ESCAPE:
	            running = False

	for b in Bacteria:
		for x in range(bacteria_radius+1):
			for y in range(bacteria_radius+1):
				Compound[(b.x+x)%width][(b.y+y)%height]-=consume
				Compound[(b.x+x)%width][(b.y+y)%height] = max(consume,Compound[(b.x+x)%width][(b.y+y)%height])
				Compound[(b.x+x)%width][(b.y-y)%height]-=consume
				Compound[(b.x+x)%width][(b.y-y)%height] = max(consume,Compound[(b.x+x)%width][(b.y-y)%height])
				Compound[(b.x-x)%width][(b.y+y)%height]-=consume
				Compound[(b.x-x)%width][(b.y+y)%height] = max(consume,Compound[(b.x-x)%width][(b.y+y)%height])
				Compound[(b.x-x)%width][(b.y-y)%height]-=consume
				Compound[(b.x-x)%width][(b.y-y)%height] = max(consume,Compound[(b.x-x)%width][(b.y-y)%height])
				
		update_compounds((b.x,b.y))
		b.update()
		b.draw()

	pygame.display.flip()

	clock.tick(60)
	
pygame.quit()
		