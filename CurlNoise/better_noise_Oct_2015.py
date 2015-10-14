import pygame
import math
import random
from pygame.locals import *

clock = pygame.time.Clock()

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Noise')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

scale = 1

persistence = 0.3;
frequency = 0.7;
amplitude = 3;
octaves = 4;
randomseed = random.randint(10,200);


time = 0

class ValueNoise:
    @classmethod
    def Noise(self, x, y):
         n = x + y * 57
         n = (n << 13) ^ n
         t = (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff
         return 1.0 - float(t) * 0.931322574615478515625e-9

    @classmethod
    def Interpolate(self, x, y, a):
        negA = 1.0 - a
        negASqr = negA * negA
        fac1 = 3.0 * (negASqr)-2.0 * (negASqr * negA)
        aSqr = a * a
        fac2 = 3.0 * aSqr - 2.0 * (aSqr * a)
        return x * fac1 + y * fac2

    @classmethod
    def GetValue(self, x, y):
        Xint = int(x)
        Yint = int(y)
        Xfrac = x - Xint
        Yfrac = y - Yint
        #noise values
        n01 = ValueNoise.Noise(Xint - 1, Yint - 1)
        n02 = ValueNoise.Noise(Xint + 1, Yint - 1)
        n03 = ValueNoise.Noise(Xint - 1, Yint + 1)
        n04 = ValueNoise.Noise(Xint + 1, Yint + 1)
        n05 = ValueNoise.Noise(Xint - 1, Yint)
        n06 = ValueNoise.Noise(Xint + 1, Yint)
        n07 = ValueNoise.Noise(Xint, Yint - 1)
        n08 = ValueNoise.Noise(Xint, Yint + 1)
        n09 = ValueNoise.Noise(Xint, Yint)
        n12 = ValueNoise.Noise(Xint + 2, Yint - 1)
        n14 = ValueNoise.Noise(Xint + 2, Yint + 1)
        n16 = ValueNoise.Noise(Xint + 2, Yint)
        n23 = ValueNoise.Noise(Xint - 1, Yint + 2)
        n24 = ValueNoise.Noise(Xint + 1, Yint + 2)
        n28 = ValueNoise.Noise(Xint, Yint + 2)
        n34 = ValueNoise.Noise(Xint + 2, Yint + 2)
        #find the noise values of the four corners
        x0y0 = 0.0625*(n01 + n02 + n03 + n04) + 0.125*(n05 + n06 + n07 + n08) + 0.25*(n09)
        x1y0 = 0.0625*(n07 + n12 + n08 + n14) + 0.125*(n09 + n16 + n02 + n04) + 0.25*(n06)
        x0y1 = 0.0625*(n05 + n06 + n23 + n24) + 0.125*(n03 + n04 + n09 + n28) + 0.25*(n08)
        x1y1 = 0.0625*(n09 + n16 + n28 + n34) + 0.125*(n08 + n14 + n06 + n24) + 0.25*(n04)
        #interpolate between those values according to the x and y fractions
        v1 = ValueNoise.Interpolate(x0y0, x1y0, Xfrac) #interpolate in x direction (y)
        v2 = ValueNoise.Interpolate(x0y1, x1y1, Xfrac) #interpolate in x direction (y+1)
        fin = ValueNoise.Interpolate(v1, v2, Yfrac)  #nterpolate in y direction
        return fin

    @classmethod
    def Total(self, i, j):
        #properties of one octave (changing each loop)
        t = 0.0
        _amplitude = 1
        freq = frequency
        for k in range(0, octaves):
            t += ValueNoise.GetValue(j * freq + randomseed, i * freq + randomseed) * _amplitude
            _amplitude *= persistence
            freq *= 2
        return t
    
    @classmethod
    def GetHeight(self, x, y):
        return amplitude * ValueNoise.Total(x, y)

#calculates the change in the potential psi between two points
def get_derivative(point1, point2):
	return (point2.psi - point1.psi)*10

#class for the points in the grid, i,j are there coordinates, x,y are their positions
class point:
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.x = 10*i
		self.y = 10*j
		self.psi = 0
		self.dx = 0
		self.dy = 0

	def display(self):
		factor = 1
		#the line to draw is the underlying noise (self.dx & dy) reduced by the mask
		x_length = factor*self.dx
		y_length = factor*self.dy
		pygame.draw.line(screen, (0,0,255), 
			(int(scale*self.x), int(scale*self.y)), 
			(int(scale*self.x + x_length), int(scale*self.y + y_length)), 1)

	#get the vector field from the potential field, turns out it's super simple
	def generate_vector_field(self):
		self.dy = -get_derivative(self, points[self.i + 1][self.j])
		self.dx = get_derivative(self, points[self.i][self.j + 1])

	#generate noise for the potential field, this is where I don't really know what I'm doing
	def generate_psi(self):
		noise = ValueNoise.GetHeight(self.i, self.j)
		self.psi = noise

#initialise
points = []

x_size = 40
y_size = 40

for i in range(x_size):
	points.append([])
	for j in range(y_size):
		points[i].append(point(i,j))

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False

	screen.fill(background_colour)

	clock.tick()


	#generate the potential field and from it the vector field
	for i in range(x_size - 1):
		for j in range(y_size - 1):
			points[i][j].generate_psi()
			points[i][j].generate_vector_field()

	#set mask for each point and then display
	for i in range(len(points)):
		for j in range(len(points[i])):
			points[i][j].display()

	#time is what causes the noise to change
	time += 1
	if time >= 50:
		time = 0
		print clock.get_fps()


	pygame.display.flip()

pygame.quit()