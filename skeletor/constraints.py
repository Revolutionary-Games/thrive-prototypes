#!/usr/bin/env python

from math import *
import pygame
from pygame.locals import *


scrdim = (1000,700)

class Verlet:
	def __init__(self, x, y):
		self.x = x
		self.x_ = x
		self.y = y
		self.y_ = y
	def move(self):
		dx = self.x - self.x_
		dy = self.y - self.y_
		self.x_ = self.x
		self.y_ = self.y
		self.x += dx
		self.y += dy

class Edge:
	def __init__(self, v1, v2, length, elasticity):
		self.v1 = v1
		self.v2 = v2
		self.length = length
		self.elasticity = e ** -elasticity
	def move(self):
		scale = hypot(self.v1.x - self.v2.x, self.v1.y - self.v2.y) / self.length - 1.0

		# dx is negative when (v1 left of v2) xor (points too far apart) 
		dx = (self.v1.x - self.v2.x) * scale * self.elasticity * 0.5
		dy = (self.v1.y - self.v2.y) * scale * self.elasticity * 0.5

		self.v1.x -= dx
		self.v2.x += dx

		self.v1.y -= dy
		self.v2.y += dy



verlets = [Verlet(scrdim[0]/2 + i, scrdim[1]/2 + i + 1) for i in xrange(16)]
edges = [Edge(verlets[i], verlets[i/2], 50, 2) for i in xrange(1, 16)]

pygame.init()
screen = pygame.display.set_mode(scrdim)
pygame.display.set_caption("verlet constraints")
bg = pygame.Surface(scrdim, flags = pygame.SRCALPHA)
bg.fill((0,0,0,12))
screen.blit(bg, (0,0))

pygame.display.update()
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

active_pt = [None]

run = True
while run:	
    screen_x = sum([v.x for v in verlets]) / float(len(verlets)) - scrdim[0] / 2
    screen_y = sum([v.y for v in verlets]) / float(len(verlets)) - scrdim[1] / 2

    time_passed = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            for v in verlets:
            	if hypot(v.x - screen_x - p[0], v.y - screen_y - p[1]) < 15:
            		active_pt[0] = v
            		break
        if event.type == MOUSEBUTTONUP:
        	active_pt[0] = None
            
    ""##

    for e in edges:
    	e.move()
    for v in verlets:
    	v.move()
    if active_pt[0] is not None:
    	p = pygame.mouse.get_pos()
    	active_pt[0].x += ((p[0] - screen_x) - active_pt[0].x) * 0.3 
    	active_pt[0].y += ((p[1] - screen_y) - active_pt[0].y) * 0.3

    screen.blit(bg, (0,0))

    for e in edges:
    	pygame.draw.line(screen, (255,255,255),
    		(int(e.v1.x - screen_x), int(e.v1.y - screen_y)),
    		(int(e.v2.x - screen_x), int(e.v2.y - screen_y)))

    for v in verlets:
    	pygame.draw.circle(screen, (255,125,0), (int(v.x - screen_x), int(v.y - screen_y)), 2)

    pygame.display.update()

