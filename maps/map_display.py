from math import *
import pygame
from pygame.locals import *

import sphube

scrdim = (400,300)

pygame.init()
screen = pygame.display.set_mode(scrdim)
pygame.display.set_caption("stretch")
bg = pygame.Surface(scrdim, flags = pygame.SRCALPHA)
bg.fill((0,0,0,255))
screen.blit(bg, (0,0))

pygame.display.update()
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

faces = {
    'A': sphube.Face('A', 50), # all 100x100
    'B': sphube.Face('B', 50),
    "C": sphube.Face('C', 50),
    "D": sphube.Face('D', 50),
    "E": sphube.Face('E', 50),
    "F": sphube.Face('F', 50),
}

#A
#BCDE
#F

offsets = {
    "A": (50, 50),
    "B": (50, 150),
    "C": (150, 150),
    "D": (250, 150),
    "E": (350, 150),
    "F": (50, 250),
}

ar = pygame.surfarray.pixels3d(screen)
# write stuff
for c in 'ABCDEF':
    offset = offsets[c]
    face = faces[c]
    for x in xrange(-50, 50):
        for y in xrange(-50, 50):
            p = ar[offset[0] + x][offset[1] - y - 1] # hack cuz pygame y is the wrong way
            s = int(face.area_metric(85, (x,y)))
            p[0] = s
            p[1] = 255 - s
            #l = int(face.latitude((x, y)) * 80) + 130
            #p[0] = l if l%8 in [0,1,2,3] else 0
            #p[1] = 255 - l if l%8 in [0,1,2,3] else 0
            #p[2] = l if l%8 in [4,5,6,7] else 0
del ar

run = True
while run:
    time_passed = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            run = False

    pygame.display.update()