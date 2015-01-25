from math import *
import pygame
from pygame.locals import *
from random import random
from voronoi import computeVoronoiDiagram as getVoronoi
from voronoi import computeDelaunayTriangulation as getDelaunay

scrdim = (1000,700)

class Point:
    def __init__(self,x,y):
        self.x, self.y = x, y
    def __add__(self, tup):
        self.x += tup[0]
        self.y += tup[1]
        return self
    def tup(self):
        return (int(self.x), int(self.y))

offsets = [
    (0          ,   0),
    (scrdim[0]  ,   0),
    (-scrdim[0] ,   0),
    (0          ,   scrdim[1]),
    (scrdim[0]  ,   scrdim[1]),
    (-scrdim[0] ,   scrdim[1]),
    (0          ,   -scrdim[1]),
    (scrdim[0]  ,   -scrdim[1]),
    (-scrdim[0] ,   -scrdim[1])
]

def makePoints(n):
    points = [Point(random() * scrdim[0] * 5 - 2*scrdim[0], random() * scrdim[1] * 5 - 2*scrdim[1]) for i in xrange(n * 30)]
    out = []
    for offset in offsets:
        out.extend([p + offset for p in points])
    return points

inpoints = makePoints(15)

def DisplayVoronoi(inpoints, voronoi, surface):
    for point in inpoints:
        pygame.draw.circle(surface, (255,125,0), point.tup(), 2)
    for line in voronoi[2]:
        v1 = None
        v2 = None
        if line[1] is -1:
            continue
        else:
            v1 = (int(voronoi[0][line[1]][0]), int(voronoi[0][line[1]][1]))
        if line[2] is -1:
            continue
        else:
            v2 = (int(voronoi[0][line[2]][0]), int(voronoi[0][line[2]][1]))
        pygame.draw.line(surface, (255,255,255), v1, v2)
    for point in voronoi[0]:
        pygame.draw.circle(surface, (255,125,0), (int(point[0]), int(point[1])), 2)

def DisplayDelaunay(inpoints, delaunay, surface):
    for triangle in delaunay:
        v1 = inpoints[triangle[0]].tup()
        v2 = inpoints[triangle[1]].tup()
        v3 = inpoints[triangle[2]].tup()
        pygame.draw.line(surface, (150,150,170), v1, v2)
        pygame.draw.line(surface, (170,150,150), v2, v3)
        pygame.draw.line(surface, (150,170,150), v3, v1)
    for point in inpoints:
        pygame.draw.circle(surface, (125,0,255), point.tup(), 2)
    

pygame.init()
screen = pygame.display.set_mode(scrdim)
pygame.display.set_caption("pytect")
bg = pygame.Surface(scrdim, flags = pygame.SRCALPHA)
bg.fill((0,0,0,1))
screen.blit(bg, (0,0))

DisplayVoronoi(inpoints, getVoronoi(inpoints), screen)
DisplayDelaunay(inpoints, getDelaunay(inpoints), screen)

pygame.display.update()
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

run = True
while run:
    time_passed = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            #inpoints = makePoints(15)
            p = pygame.mouse.get_pos()
            inpoints[0].x = p[0]
            inpoints[0].y = p[1]
            screen.blit(bg,(0,0))
            DisplayVoronoi(inpoints, getVoronoi(inpoints), screen)
            #DisplayDelaunay(inpoints, getDelaunay(inpoints), screen)
    ""##

    
    #screen.blit(bg, (0,0))

    #stars[0].x, stars[0].y = pygame.mouse.get_pos()

    pygame.display.update()
