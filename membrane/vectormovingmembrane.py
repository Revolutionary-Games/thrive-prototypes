
import pygame
import math
import sys
import random
from pygame.locals import *
import time
from pygame.mouse import get_pos
start_time = time.time()

# scale scales the canvas, essentially
scale = 0.5
(width, height) = (int(2000 * scale), int(1000 * scale))

# alpha values for making rendering smoother yay
pointalpha = 130
linealpha = 130
bgalpha = 130

background_colour = (255,255,255, bgalpha)
bg = pygame.Surface((width, height), flags = pygame.SRCALPHA)

screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Membrane')
pygame.font.init()

# I wrote a vector mathematics class just to make things easier

class Vector:
    'Represents a 2D vector.'
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def __add__(self, val):
        return Vector(self.x + val.x, self.y + val.y, self.z + val.z )
    
    def __sub__(self,val):
        return Vector(self.x - val.x, self.y - val.y, self.z - val.z )

    def __div__(self, val):
        return Vector(self.x / val, self.y / val, self.z / val)
    
    def __mul__(self, val):
        return Vector( self.x * val, self.y * val, self.z*val)

    def normalise(self):
        norma = norm(self)
        self = self/norma
        

def dot(a,b):
    return a.x*b.x + a.y*b.y + a.z*b.z

def cross(a,b):
    return Vector(a.y*b.z - a.z*b.y, a.x*b.z - a.z*b.x, a.x*b.y - a.y*b.x)

def norm(a):
    value = math.sqrt(a.x**2 + a.y**2 + a.z**2)
    if abs(value) >= 0.01:
        return value
    else:
        return 0.01

def distance(a,b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)

def tocartesian(a):
    return Vector(a.x*math.sin(a.y)*math.cos(a.z),
                a.x*math.sin(a.y)*math.sin(a.z),
                a.x*math.cos(a.y))

def tospherical(a):
    return Vector(norm(a), math.acos(a.z/norm(a)), math.atan2(a.y,a.x))

def direction(a,b):
    return Vector(b.x - a.x, b.y - a.y, b.z - a.z)

def drawTriangle(colour, triangle, xoff=0, yoff=0):
    pygame.draw.polygon(bg, colour,
                       [[int(scale * (xoff + triangle[0].pos.x)),int(scale * (yoff + triangle[0].pos.y))],
                        [int(scale * (xoff + triangle[1].pos.x)),int(scale * (yoff + triangle[1].pos.y))],
                        [int(scale * (xoff + triangle[2].pos.x)),int(scale * (yoff + triangle[2].pos.y))]],
                           1)



#Setup

size = 500
sidelength = int(math.sqrt(float(size) / 6))

print sidelength
truesize = 6*(sidelength**2)

print truesize

def within(a,b,lim=5):
    return abs(a-b) < lim

#organelles

class controlpoint:
    def __init__(self):
        self.pos = Vector(random.randint(300,700),random.randint(300,700),random.randint(-200,200))
        self.mass = random.randint(5,10)
        self.spos = tospherical(self.pos)
        self.colour = (0,0,255)
        self.norm = norm(self.pos)

    def display(self):
        pygame.draw.circle(bg, self.colour,
                    (int(scale * (self.pos.x)),
                    int(scale * (self.pos.y))),
                    int(scale * self.mass))

    def move(self):
        threshold = 150
        movement = Vector(0,0,0)
        for i in range(len(controlpoints)):
            towards = direction(self.pos, controlpoints[i].pos)
            movement += (towards*(1 - (1 / norm(towards / threshold))**2))*controlpoints[i].mass
        self.pos += movement*0.001
        self.norm = norm(self.pos)


#define vertices

class vertex:
    def __init__(self, x,y,z):
        self.pos = Vector(x,y,z)
        self.r = tospherical(self.pos).x
        self.colour = (255,0,0, pointalpha)
        self.nbrs = []

    def display(self):
        pygame.draw.circle(bg, self.colour,
                       (int(scale * (centre[0] + self.pos.x)),
                        int(scale * (centre[1] + self.pos.y))),
                           int(scale * 5))

# this is where the vertices get smoothed. They try sum the distances from their neighbours to the origin.
# then they subtract their own distance multiplied by the number of neighbours.
# this gives a measure of if they are above or below average. They then move to become more average

    def smooth(self):
        laplacian = 0
        spherical = tospherical(self.pos)
        for i in range(len(self.nbrs)):
            laplacian += self.nbrs[i].r
        laplacian -= len(self.nbrs)*self.r
        spherical.x += 0.1*laplacian
        self.r = spherical.x
        self.pos = tocartesian(spherical)
        self.norm = norm(self.pos)


#if a vertx gets too close to an organelle is moves further away

    def checkdistance(self):
        truelocation = self.pos + Vector(centre[0],centre[1],centre[2])
        for pt in controlpoints:
            if distance(truelocation, pt.pos) <= 100:
                spherical = tospherical(self.pos)
                spherical.x += 30
                self.pos = tocartesian(spherical)


#initialise
        

vertices = []
controlpoints = []
triangles = []

#place some random organelles

def makeOrganelles(n):
    controlpoints[:] = [] # clear contents of the list
    for i in range(0, n):
        controlpoints.append(controlpoint())
        controlpoints[0].pos = Vector(500,500,0)
        controlpoints[0].mass = 20

makeOrganelles(10)

maxdist = 0

for i in range(len(controlpoints)):
    if distance(controlpoints[i].pos, controlpoints[0].pos) >= maxdist:
        maxdist = distance(controlpoints[i].pos, controlpoints[0].pos)

maxdist += 30

#compute the size of gaps between vertices

print 'maxdist', maxdist
gap = float(2*maxdist)/sidelength
print 'gap', gap

#put vertices on the top and bottom of the cube

for i in range(sidelength + 1):
    for j in range(sidelength + 1):
        vertices.append(vertex(-maxdist + i*gap, -maxdist + j*gap, -maxdist))
        vertices.append(vertex(-maxdist + i*gap, -maxdist + j*gap, +maxdist))

print 'top and bottom complete'
print 'Time : ' , time.time() - start_time

#put vertices on the sides of the cube

for i in range(sidelength):
    for j in range(sidelength - 1):
        vertices.append(vertex(-maxdist + i*gap , -maxdist, -maxdist + gap + j*gap))
        vertices.append(vertex(+maxdist - i*gap, +maxdist, -maxdist + gap + j*gap))
        vertices.append(vertex(+maxdist, -maxdist + i*gap , -maxdist + gap + j*gap))
        vertices.append(vertex(-maxdist, +maxdist - i*gap , -maxdist + gap + j*gap))

print 'sides complete'
print 'Time : ' , time.time() - start_time

#compute a list of neighbours for each vertex

for i in range(len(vertices)):
    for j in range(len(vertices)):
        if (distance(vertices[i].pos,vertices[j].pos)
            <= 1.1*gap):
            if (distance(vertices[i].pos, vertices[j].pos)
                >= 0.5*gap):
                vertices[i].nbrs.append(vertices[j])


print 'neighbours complete'
print 'Time : ' , time.time() - start_time

#compute a list of triangles which connect the vertices

for i in range(len(vertices)):
    for j in range(len(vertices[i].nbrs)):
        for k in range(j, len(vertices[i].nbrs)):
            vector1 = direction( vertices[i].pos, vertices[i].nbrs[j].pos )
            vector2 = direction( vertices[i].pos, vertices[i].nbrs[k].pos )
            crossproduct = cross(vector1, vector2)
            if norm(crossproduct) >= 1:
                triangles.append((vertices[i],vertices[i].nbrs[j],vertices[i].nbrs[k]))

print 'triangles complete'
print 'Time : ' , time.time() - start_time

#remove duplicates from the list of triangles

triangles = list(set(triangles))

print 'triangle filter complete'
print 'Time : ' , time.time() - start_time

print len(triangles), 'triangles'

    
counter = 0
running = True
toggle = False
lock = True
showVertices = True
while running:
    mousepos = get_pos()
    vecmousepos = Vector(mousepos[0], mousepos[1], 0)
    waytogo = vecmousepos - (controlpoints[0].pos * scale)
    centre = [controlpoints[0].pos.x, controlpoints[0].pos.y, controlpoints[0].pos.z]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RCTRL:
                toggle = not toggle
            elif event.key == K_RSHIFT:
                lock = not lock
            elif event.key == K_RETURN:
                makeOrganelles(10)
            elif event.key == K_LSHIFT:
                showVertices = not showVertices
            elif event.key == K_LCTRL:
                for pt in controlpoints:
                    pt.clicked = False

    bg.fill(background_colour)

    for i in range(len(controlpoints)):
        controlpoints[i].display()
        if not lock:
            controlpoints[i].move()
            if counter <= 10:
                controlpoints[i].pos += (waytogo*0.8)/controlpoints[i].mass
            else:
                controlpoints[i].pos += (waytogo*0.3)/controlpoints[i].mass

    for i in range(len(triangles)):
        drawTriangle((0,0,100,linealpha), triangles[i], xoff=centre[0], yoff=centre[1])

    for i in range(len(vertices)):
        if showVertices: vertices[i].display()
        if toggle:
            vertices[i].smooth()
            vertices[i].pos = vertices[i].pos*0.99
            vertices[i].checkdistance()


    counter += 1            
    if counter >= 15:
        counter = 0
    
    
    screen.blit(bg, (0,0))
    pygame.display.flip()
    time.sleep(0.030)

pygame.quit()



