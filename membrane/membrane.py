
#I have tried to put comments in the code to hopefully make it easier to understand in case anyone is reading it.

#make a cube around the organelles which is then smoothed into place, compute all triangles in the mesh

#setup

import pygame
import math
import sys
import random
from pygame.locals import *
import time
from pygame.mouse import get_pos
start_time = time.time()

print 'Time : ' , time.time() - start_time

# scale scales the canvas, essentially
scale = 0.5
(width, height) = (int(2000 * scale), int(1000 * scale))

# alpha values for making rendering smoother yay
pointalpha = 130
linealpha = 130
bgalpha = 130

background_colour = (0,0,0, bgalpha)
bg = pygame.Surface((width, height), flags = pygame.SRCALPHA)

#size is approximately how many vertices to use in total

size = 500
sidelength = int(math.sqrt(float(size) / 6))

print sidelength
truesize = 6*(sidelength**2)

print truesize

def within(a,b,lim=5):
    return abs(a-b) < lim

def dim2Color(dim, lower=-250, upper=250):
    a = int(255 * (dim-lower) / (upper - lower))
    a = 0 if a < 0 else 255 if a > 255 else a
    return a

#useful vector functions

def distance(x,y,z,i,j,k):
    return math.sqrt((x-i)**2 + (y-j)**2 + (z-k)**2)

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

#define control points (which are the organelles)

class controlpoint:
    def __init__(self):
        self.r = random.randint(200,300)
        self.theta = random.uniform(0, 2*math.pi)
        self.phi = random.uniform(0, math.pi)
        self.x = self.r*math.sin(self.theta)*math.cos(self.phi)
        self.y = self.r*math.sin(self.theta)*math.sin(self.phi)
        self.z = self.r*math.cos(self.theta)
        self.colour = (0,0,255,pointalpha)
        self.clicked = False

    def display(self):
        self.colour = (
            dim2Color(self.x),
            dim2Color(self.y),
            dim2Color(self.z),
            pointalpha)
        pygame.draw.circle(bg, self.colour,
                       (int(scale * (500 + self.x)),
                        int(scale * (500 + self.y))),
                           int(scale * 10))
        pygame.draw.circle(bg, (255-self.colour[0], # we outline it in the opposite color
                                255-self.colour[1],
                                255-self.colour[2],
                                bgalpha),
                       (int(scale * (500 + self.x)),
                        int(scale * (500 + self.y))),
                           int(scale * 10),
                           2)
        pygame.draw.circle(bg, self.colour,
                       (int(scale * (1500 + self.x)),
                        int(scale * (500 + self.z))),
                           int(scale * 10))
        pygame.draw.circle(bg, (255-self.colour[0],
                                255-self.colour[1],
                                255-self.colour[2],
                                bgalpha),
                       (int(scale * (1500 + self.x)),
                        int(scale * (500 + self.z))),
                           int(scale * 10),
                           2)

    def handleMouse(self, x, y, clicking_edge = False):
        # convert to internal render coords
        x /= scale
        y /= scale
        y -= 500
        mouseray = [None, None, None]
        # convert to effective 3D coordinates
        if x > 1000: # if click was on side view (ie, on xz plane)
            x -= 1500
            mouseray[0] = x
            mouseray[2] = y
        else: # click was on xy plane
            x -= 500
            mouseray[0] = x
            mouseray[1] = y
        # so mouseray holds a line, where the None coordinate is allowed to vary
        if clicking_edge: # runs if this was called on mouse-click-down
            if within(mouseray[0], self.x):
                if mouseray[1] is not None and within(mouseray[1], self.y):
                    self.clicked = True
                elif mouseray[2] is not None and within(mouseray[2], self.z):
                    self.clicked = True
        if self.clicked:
            self.x = mouseray[0]
            if mouseray[1]: self.y = mouseray[1]
            elif mouseray[2]: self.z = mouseray[2]


#define vertices

class vertex:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.r = distance(self.x,self.y,self.z,0,0,0)
        self.theta = math.acos(float(self.z)/self.r)
        self.phi = math.atan2(self.y,self.x)
        self.colour = (255,0,0, pointalpha)
        self.nbrs = []

    def display(self):
        pygame.draw.circle(bg, self.colour,
                       (int(scale * (500 + self.x)),
                        int(scale * (500 + self.y))),
                           int(scale * 5))
        pygame.draw.circle(bg, self.colour,
                       (int(scale * (1500 + self.x)),
                        int(scale * (500 + self.z))),
                           int(scale * 5))

# this is where the vertices get smoothed. They try sum the distances from their neighbours to the origin.
# then they subtract their own distance multiplied by the number of neighbours.
# this gives a measure of if they are above or below average. They then move to become more average

    def smooth(self):
        laplacian = 0
        for i in range(len(self.nbrs)):
            laplacian += self.nbrs[i].r
        laplacian -= len(self.nbrs)*self.r
        self.r += 0.1*laplacian
        self.x = self.r*math.sin(self.theta)*math.cos(self.phi)
        self.y = self.r*math.sin(self.theta)*math.sin(self.phi)
        self.z = self.r*math.cos(self.theta)

#if a vertex gets too close to an organelle is moves further away

    def checkdistance(self):
        for pt in controlpoints:
            if distance(self.x,self.y,self.z,pt.x,pt.y,pt.z) <= 150:
                self.r += 5

vertices = []
controlpoints = []
triangles = []

maxdist = 0

#place some random organelles

def makeOrganelles(n):
    controlpoints[:] = [] # clear contents of the list
    for i in range(0, n):
        controlpoints.append(controlpoint())
    controlpoints[0].r = 0

makeOrganelles(10)

for i in range(len(controlpoints)):
    if controlpoints[i].r >= maxdist:
        maxdist = controlpoints[i].r

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
        if (distance(vertices[i].x,vertices[i].y, vertices[i].z, vertices[j].x, vertices[j].y, vertices[j].z)
            <= 1.1*gap):
            if (distance(vertices[i].x,vertices[i].y, vertices[i].z, vertices[j].x, vertices[j].y, vertices[j].z)
                >= 0.5*gap):
                vertices[i].nbrs.append(vertices[j])

print 'neighbours complete'
print 'Time : ' , time.time() - start_time

#compute a list of triangles which connect the vertices

for i in range(len(vertices)):
    for j in range(len(vertices[i].nbrs)):
        for k in range(j, len(vertices[i].nbrs)):
            vector1 = [vertices[i].nbrs[j].x - vertices[i].x,
                       vertices[i].nbrs[j].y - vertices[i].y,
                       vertices[i].nbrs[j].z - vertices[i].z]
            vector2 = [vertices[i].nbrs[k].x - vertices[i].x,
                       vertices[i].nbrs[k].y - vertices[i].y,
                       vertices[i].nbrs[k].z - vertices[i].z]
            crossproduct = cross(vector1, vector2)
            if crossproduct >= 1:
                triangles.append((vertices[i],vertices[i].nbrs[j],vertices[i].nbrs[k]))

print 'triangles complete'
print 'Time : ' , time.time() - start_time

#remove duplicates from the list of triangles

triangles = list(set(triangles))

print 'triangle filter complete'
print 'Time : ' , time.time() - start_time

screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Membrane')
pygame.font.init()

def drawTriangle(triangle, xoff=0, yoff=0, wire=True):
    pygame.draw.polygon(bg, (255,125,0,linealpha),
                       [[int(scale * (xoff + triangle[0].x)),int(scale * (yoff + triangle[0].y))],
                        [int(scale * (xoff + triangle[1].x)),int(scale * (yoff + triangle[1].y))],
                        [int(scale * (xoff + triangle[2].x)),int(scale * (yoff + triangle[2].y))]],
                           1)

def drawTriangle2(triangle, xoff=0, yoff=0, wire=True):
    pygame.draw.polygon(bg, (255,125,0,linealpha),
                       [[int(scale * (xoff + triangle[0].x)),int(scale * (yoff + triangle[0].z))],
                        [int(scale * (xoff + triangle[1].x)),int(scale * (yoff + triangle[1].z))],
                        [int(scale * (xoff + triangle[2].x)),int(scale * (yoff + triangle[2].z))]],
                           wire)
      

toggle = False
lock = True
showVertices = True

#main loop  
running = True

while running:
    mousepos = get_pos()

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
        elif event.type == MOUSEBUTTONDOWN:
            for pt in controlpoints:
                pt.handleMouse(*mousepos, clicking_edge = True)
        elif event.type == MOUSEBUTTONUP:
            for pt in controlpoints:
                pt.clicked = False

    bg.fill(background_colour)

    #draw the control points and the triangles

    for pt in controlpoints:
        pt.handleMouse(*mousepos)
        pt.display()

    for i in range(len(triangles)):
        drawTriangle(triangles[i], xoff=500, yoff=500)
        drawTriangle2(triangles[i], xoff=1500, yoff=500)

    # draw and update the vertices
        

    for i in range(len(vertices)):
        if showVertices: vertices[i].display()
        if toggle:
            vertices[i].smooth()
            vertices[i].r = vertices[i].r*0.99
            vertices[i].checkdistance()


    if lock:
        # lock two of the vertices in place
        vertices[27].r = 600
        vertices[27].colour = (0,255,0)
        vertices[29].r = 600
        vertices[29].colour = (0,255,0)      

    screen.blit(bg, (0,0))
    pygame.display.flip()
    time.sleep(0.030)

pygame.quit()
