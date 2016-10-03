#!/usr/bin/env python

from math import *
from numbers import Number
import pygame
from pygame.locals import *


EPSILON = 0.000001

scrdim = (1000,700)

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, Vec3):
            self.x, self.y, self.z = x.x, x.y, x.z
        else:
            self.x, self.y, self.z = x, y, z
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        # if isinstance(other, Number):
        return Vec3(self.x * other, self.y * other, self.z * other)
    def __rmul__(self, other): # We need an rmul for right-multiplying with numbers
        return self * other
    def __div__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)
    def proj(self, other):
        # return the projection of this onto the given vector
        return other * (self * other) / (other * other)
    def length(self):
        return sqrt(self * self)


# adapted from http://geomalgorithms.com/a02-_lines.html
# given point p and line segment p0:p1
# return vector from p to closest point on p0:p1
def p2ls(p, p0, p1):
    v = p1 - p0
    w = p - p0

    c1 = w * v
    c2 = v * v

    if c1 <= 0:
        return p0 - p
    if c2 <= c1:
        return p1 - p

    b = c1 / c2
    return p0 + b * v - p

# adapted from http://geomalgorithms.com/a07-_distance.html
# given line segment p defined by points p0, p1
# and line segment q defined by points q0, q1
# return shortest vector from point on p to a point on q
def ls2ls(p0,p1,q0,q1):
    u = p1 - p0
    v = q1 - q0
    w0 = p0 - q0

    a = float(u * u)
    b = float(u * v)
    c = float(v * v)
    d = float(u * w0)
    e = float(v * w0)

    disc = a * c - b * b
    if disc < EPSILON:
        return -w0

    becd = b * e - c * d
    aebd = a * e - b * d

    if becd < 0:
        pc = p0
    elif becd > disc:
        pc = p1
    else:
        pc = p0 + u * (becd / disc)
    
    if aebd < 0:
        qc = q0
    elif aebd > disc:
        qc = q1
    else:
        qc = q0 + v * (aebd / disc)

    return qc - pc


class Verlet:
    def __init__(self, x, y, z):
        self.pos = Vec3(x,y,z)
        self.prev = Vec3(x,y,z)
        self.edges = []
    def move(self, friction = 0.98):
        d = self.pos - self.prev
        d.y += 1
        self.prev = Vec3(self.pos)
        self.pos += d * friction
    def edgeCollision(self, edge):
        if edge in self.edges:
            return
        disp = p2ls(edge.v1.pos, edge.v2.pos, self.pos)
        distance = disp.length()
        if distance >= edge.thickness:
            return
        delta = (edge.thickness - distance) * edge.softness
        self.pos -= delta * disp * 0.5

        edge.v1.pos += delta * disp * 0.25
        edge.v2.pos += delta * disp * 0.25
    def render(self, surface):
        pygame.draw.circle(surface, (255,125,0), (int(self.pos.x), int(self.pos.y)), 2)


class Edge:
    def __init__(self, v1, v2, length, elasticity, thickness = 5, softness = 1.2):
        self.v1 = v1
        self.v2 = v2
        v1.edges.append(self)
        v2.edges.append(self)
        self.length = length
        self.elasticity = e ** -elasticity
        self.softness = e ** -softness
        self.thickness = thickness
    def move(self):
        scale = (self.v1.pos - self.v2.pos).length() / self.length - 1.0

        # d.x is negative when (v1 left of v2) xor (points too far apart)
        # analogous for y, z
        d = (self.v1.pos - self.v2.pos) * scale * self.elasticity * 0.5

        self.v1.pos -= d
        self.v2.pos += d
    def render(self, surface):        
        pygame.draw.line(surface, (255,255,255),
            (int(self.v1.pos.x), int(self.v1.pos.y)),
            (int(self.v2.pos.x), int(self.v2.pos.y)))
    def edgeCollision(self, other):
        if (self in other.v1.edges or
            self in other.v2.edges):
            return
        disp = ls2ls(self.v1.pos, self.v2.pos, other.v1.pos, other.v2.pos)
        if disp.length() >= self.thickness + other.thickness:
            return
        delta = (self.thickness + other.thickness - disp.length()) * self.softness * other.softness

        self.v1.pos -= delta * disp * 0.25
        self.v2.pos -= delta * disp * 0.25

        other.v1.pos += delta * disp * 0.25
        other.v2.pos += delta * disp * 0.25

class PlaneConstraint:
    def __init__(self, p, n):
        self.pos = p
        self.normal = n / n.length()
    def project(self, p):
        return p - (p - self.pos).proj(self.normal)
    def above(self, p):
        return (p - self.pos).proj(self.normal) * self.normal > -EPSILON
    def constrain(self, v):
        if not self.above(v.pos):
            v.pos = self.project(v.pos)
            v.prev = v.pos

verlets = [Verlet(scrdim[0]/2 + (i % 4) * 50, scrdim[1]/2 + (i / 4) * 50, i) for i in xrange(16)]
edges = [Edge(verlets[i] , verlets[i/2], 140, 2) for i in xrange(1, 16)]
planes = [PlaneConstraint(Vec3(0, 600, 0), Vec3(0, -1, 0))]

# edges = [Edge(verlets[i], verlets[i-4], 50, 2) for i in xrange(4, 16)]
# edges.extend([Edge(verlets[i], verlets[i-1], 50, 2) for i in xrange(16) if i % 4])
# edges.extend([Edge(verlets[i], verlets[i+3], 50 * 2 ** 0.5, 2) for i in xrange(12) if i % 4])
# edges.extend([Edge(verlets[i], verlets[i+5], 50 * 2 ** 0.5, 2) for i in xrange(12) if (i+1) % 4])

v2 = [Verlet(scrdim[0]/2 + (i % 4) * 50, scrdim[1]/2 + (i / 4) * 50, i) for i in xrange(4)]
e2 = [
    Edge(v2[0] , v2[1], 140, 2),
    Edge(v2[0] , v2[2], 140, 2),
    Edge(v2[0] , v2[3], 140, 2),
    Edge(v2[1] , v2[2], 140, 2),
    Edge(v2[1] , v2[3], 140, 2),
    Edge(v2[2] , v2[3], 140, 2),
]

verlets.extend(v2)
edges.extend(e2)


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
    screen_x = 0#sum([v.x for v in verlets]) / float(len(verlets)) - scrdim[0] / 2
    screen_y = 0#sum([v.y for v in verlets]) / float(len(verlets)) - scrdim[1] / 2

    time_passed = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            for v in verlets:
                if hypot(v.pos.x - screen_x - p[0], v.pos.y - screen_y - p[1]) < 15:
                    active_pt[0] = v
                    break
        if event.type == MOUSEBUTTONUP:
            active_pt[0] = None


    for i in xrange(len(edges)):
        edges[i].move()
        for j in xrange(0, i):
            edges[i].edgeCollision(edges[j])
    for v in verlets:
        v.move()
        for p in planes:
            p.constrain(v)
        # for e in edges:
            # v.edgeCollision(e)
    if active_pt[0] is not None:
        p = pygame.mouse.get_pos()
        active_pt[0].pos.x += ((p[0] - screen_x) - active_pt[0].pos.x) * 0.3
        active_pt[0].pos.y += ((p[1] - screen_y) - active_pt[0].pos.y) * 0.3

    screen.blit(bg, (0,0))

    for e in edges:
        e.render(screen)
        # pygame.draw.line(screen, (255,255,255),
        #     (int(e.v1.x - screen_x), int(e.v1.y - screen_y)),
        #     (int(e.v2.x - screen_x), int(e.v2.y - screen_y)))

    for v in verlets:
        v.render(screen)
        # pygame.draw.circle(screen, (255,125,0), (int(v.x - screen_x), int(v.y - screen_y)), 2)

    pygame.display.update()

