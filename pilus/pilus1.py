import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be LIGHT')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

#return distance
def distance(point1, point2):
	return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#define the points which make up the pilus
points = []

for i in range(10):
	points.append([width/2, height])

springyness = 0.1 #how taught the pilus is
mouse = False
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        elif event.key == K_SPACE:
	            mouse = not mouse

	#get the mouse position to follow
	pos = [width/2, height]    
	if mouse:   
		pos = pygame.mouse.get_pos()

	screen.fill(background_colour)

	for i in range(len(points)):

		#work out the direction to the mouse pointer and move in that direction
		if i == len(points) - 1:
			direction = [pos[0] - points[i][0], pos[1] - points[i][1]]
			points[i][0] += 0.1*direction[0]
			points[i][1] += 0.1*direction[1]
			#check you haven't gone too far out
			length = distance(points[0], points[len(points) - 1])
			if length > height/2:
				#if you have gone too far out normalise your length to height/2
				direction = [points[len(points) - 1][0] - points[0][0], 
					points[len(points) - 1][1] - points[0][1]]
				points[i][0] = points[0][0] + (height/2)*(direction[0]/length)
				points[i][1] = points[0][1] + (height/2)*(direction[1]/length)
			
		#have each joint intersperce itself with its neighbours
		if i > 0:
			if distance(points[i], points[i-1]) > 10:
				points[i][0] -= springyness*(points[i][0] - points[i-1][0])
				points[i][1] -= springyness*(points[i][1] - points[i-1][1])
		if i < len(points) - 1:
			if distance(points[i], points[i+1]) > 10:
				points[i][0] -= springyness*(points[i][0] - points[i+1][0])
				points[i][1] -= springyness*(points[i][1] - points[i+1][1])

		#anchor the pilus
		points[0][0] = width/2
		points[0][1] = height

		#draw everything
		if i < len(points) - 1:
			pygame.draw.line(screen, [0,0,255], [int(points[i][0]), int(points[i][1])],
							[int(points[i + 1][0]), int(points[i + 1][1])], 3)
		pygame.draw.circle(screen, [255,0,0], [int(points[i][0]), int(points[i][1])], 10)
	

	pygame.display.flip()
	

pygame.quit()