#!/usr/bin/env python

from math import *
from numbers import Number
import pygame
from pygame.locals import *


EPSILON = 0.000001

scrdim = (1200,1000)

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
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
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
# uses a distance/length cutoff for how far lines should be before it's not worth
# calculating a precise distance
def ls2ls(p0,p1,q0,q1, dlc = 0.8):
    u = p1 - p0
    v = q1 - q0
    w0 = p0 - q0

    # Is this actually any cheaper than just doing the calculation
    s = max(v.length(), u.length()) * dlc
    l0 = w0.length()
    if l0 > s:
        w1, w2, w3 = p1 - q1, p0 - q1, p1 - q0
        l1, l2, l3 = w1.length(), w2.length(), w3.length()
        g = min(l0,l1,l2,l3)
        if g > s:
            if g == l0:
                return w0
            if g == l1:
                return w1
            if g == l2:
                return w2
            return w3

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
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, Vec3):
            x,y,z = x.x, x.y, x.z
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
    def target(self, pos, response = 0.3, topspeed = 3):
        d = self.pos - pos
        d = d * 0.3
        dl2 = d * d
        if dl2 > topspeed * topspeed:
            d = d * topspeed * topspeed / dl2
        self.prev += d


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

class MeshBuilder:
    def __init__(self, edge_props = {"elasticity": 2}):
        self.edge_props = edge_props
    def buildMesh(self, points = [], edges = [], origin = Vec3(0,0,0)):
        verlets = [Verlet(p + origin) for p in points]
        edges = [Edge(verlets[edge[0]], verlets[edge[1]], (points[edge[0]] - points[edge[1]]).length(), **self.edge_props) for edge in edges]
        return (verlets, edges)

class Skeleton:
    def __init__(self, joints, bones):
        self.joints = joints
        self.bones = bones
        self.feet = []
    def setFeet(self, indices):
        self.feet = indices
    def balance(self):
        pass

verlets = [Verlet(scrdim[0]/2 + (i % 4) * 50, scrdim[1]/2 + (i / 4) * 50, i) for i in xrange(16)]
edges = [Edge(verlets[i] , verlets[i/2], 140, 2) for i in xrange(1, 16)]
#verlets = []
#edges = []

planes = [PlaneConstraint(Vec3(0, scrdim[1] - 100, 0), Vec3(0, -1, 0))]

# edges = [Edge(verlets[i], verlets[i-4], 50, 2) for i in xrange(4, 16)]
# edges.extend([Edge(verlets[i], verlets[i-1], 50, 2) for i in xrange(16) if i % 4])
# edges.extend([Edge(verlets[i], verlets[i+3], 50 * 2 ** 0.5, 2) for i in xrange(12) if i % 4])
# edges.extend([Edge(verlets[i], verlets[i+5], 50 * 2 ** 0.5, 2) for i in xrange(12) if (i+1) % 4])

def all_pairs(x):
    out = []
    for i in xrange(x):
        for j in xrange(i):
            out.append((i, j))
    return out

builder = MeshBuilder({"elasticity":1.2})
v1, e1 = builder.buildMesh(
    [
    Vec3(  0,  0,  0),#A
    Vec3(200,  0,  0),#B
    Vec3(200,200,  0),#F
    Vec3(  0,200,  0),#E
    Vec3(  0,200,200),#G
    Vec3(200,200,200),#H
    Vec3(200,  0,200),#D
    Vec3(  0,  0,200),#C
    ],#all_pairs(8),
    [
    (0,1),
    (1,2),
    (2,3),
    (3,0),

    (4,5),
    (5,6),
    (6,7),
    (7,4),

    (7,0),
    (3,4),
    (2,5),
    (1,6),

    (0,5),

    (1,7),
    (7,3),
    (3,1),

    (2,4),
    (4,6),
    (6,2),
    ],
    Vec3(300,500))

verlets.extend(v1)
edges.extend(e1)

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
        p = Vec3(p[0], p[1], 0)
        active_pt[0].target(p, topspeed = 1000)

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

