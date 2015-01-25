from math import *
import pygame
from pygame.locals import *
from random import random

scrdim = (1000,700)

class Camera:
    def __init__(self, x=0,y=0):
        self.x, self.y = x, y
    def centerOn(self, stuff, offset = (scrdim[0] / 2, scrdim[1] / 2)):
        self.x = sum([obj.x * obj.mass for obj in stuff]) / sum([obj.mass for obj in stuff]) - offset[0]
        self.y = sum([obj.y * obj.mass for obj in stuff]) / sum([obj.mass for obj in stuff]) - offset[1]


camera = Camera()

sbconst = 5.670373 * 10 ** -8
tempfactor = (1 / (4 * pi * sbconst))
Rsun = 695800000 #meters
Lsun = 3.846 * 10 ** 26 # Watts

def TtoRGB(temp):
    """
    Converts temperature to blackbody color in RGB
    Adapted from http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    temp /= 100
    r = 0
    g = 0
    b = 0
    if temp <= 66:
        r = 255
    else:
        r = 329.698727446 * ((temp - 60) ** -0.1332047592)
        if r < 0: r = 0
        if r > 255: r = 255

    if temp <= 66:
        g = 99.4708025861 * log(temp) - 161.1195681661
        if g < 0: g = 0
        if g > 255: g = 255
    else:
        g = 288.1221695283 * ((temp - 60) ** -0.0755148492)
        if g < 0: g = 0
        if g > 255: g = 255
    
    if temp >= 66:
        b = 255
    elif temp <= 19:
        b = 0
    else:
        b = 138.5177312231 * log(temp - 10) - 305.0447927307
        if b < 0: b = 0
        if b > 255: b = 255
    return (int(r),int(g),int(b))

# Gravitational 
invsq = lambda r: r if r < 1 else 100.0 / (r*r)
lin = lambda r: r
k = 1 * 10 ** -4

class Star:
    def __init__(self, x, y, dx, dy, mass, glaw = invsq):
        self.x = x
        self.y = y
        self.x_ = x - dx
        self.y_ = y - dy
        self.g = glaw
        self.mass = mass
        r = mass ** (2.5/3) * Rsun
        self.rad = int(mass ** (2.5/3) * 2) + 2
        lumo = 1.5 * mass ** 3.5 * Lsun
        temp = (tempfactor * lumo * r ** -2) ** 0.25
        self.color = TtoRGB(temp)
    def move(self):
        # we move using Verlet integration
        self.x, self.x_ = 2*self.x - self.x_, self.x
        self.y, self.y_ = 2*self.y - self.y_, self.y
    def pull(self, other):
        # we push x_ and y_ away from attractor
        r = hypot(self.x - other.y, self.y - other.y)
        a = self.g(r) * k * other.mass
        ax = 0 if r == 0 else a * (self.x - other.x) / r
        ay = 0 if r == 0 else a * (self.y - other.y) / r
        self.x_ += ax
        self.y_ += ay

    def render(self, surface):
        try:
            pygame.draw.circle(surface, self.color, (int(self.x - camera.x), int(self.y - camera.y)), self.rad)
        except:
            print self.x - camera.x, self.y - camera.y

def spawnCluster(n, glaw = lin):
    stars = []
    w = scrdim[0] * 0.8
    h = scrdim[1] * 0.8
    for i in xrange(n):
        m = e ** -(random() * 15) * 15
        x = random() * w
        y = random() * h
        v = random() / (k * 300) * hypot(x - w/2, y - h/2) / hypot(w/2, h/2)
        ang = random() * 2 * pi
        dx = sin(ang) * v
        dy = cos(ang) * v
        star = Star(x, y, dx, dy, m, glaw = glaw)
        stars.append(star)
    return stars

stars = spawnCluster(12)

pygame.init()
screen = pygame.display.set_mode(scrdim)
bg = pygame.Surface(scrdim, flags = pygame.SRCALPHA)
bg.fill((0,0,0, 6))
screen.blit(bg, (0,0))
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
    ""##

    for star in stars:
        for star2 in stars:
            if star != star2:
                star.pull(star2)
    screen.blit(bg, (0,0))
    for star in stars:
        star.move()
    camera.centerOn(stars)
    p = pygame.mouse.get_pos()
    p = [p[0] + camera.x, p[1] + camera.y]
    stars[0].x, stars[0].y = p
    stars[0].x_, stars[0].y_ = p
    for star in stars:
        star.render(screen)
    pygame.display.update()
