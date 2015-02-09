# A prototype for gameplay as a photosynthesizing microbe for Thrive

import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1600, 800)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Photosynthesizing')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

#Take over control and render a message

def rendermessage(message):
	message.append(' ')
	message.append('Press SPACE to dismiss this message')
	X = 100
	Y = 100
	pygame.draw.polygon(screen, (0,255,255), [(X,Y), (X + width - 200,Y), 
		(X + width - 200,Y + height - 200), (X,Y + height - 200)], 0)
	for i in range(len(message)):
		label = myfont.render(message[i], 1, (0,0,0))
		screen.blit(label, (X + 100, Y + 100 + 20*i))
	pygame.display.flip()
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
				if event.key == K_SPACE:
					run = False

#show the values of compounds along the bottom

def displaybar(name, number, value, control, state):
	colour = (0,0,255)
	if state == False:
		colour = (255,0,0)
	X = int(100 + number*100)
	Y = int(height - 50)
	value = int(value)
	pygame.draw.polygon(screen, colour, [(X,Y), (X , Y - value), (X + 10,Y - value), (X + 10,Y)], 0)
	label = myfont.render(name, 5, colour)
	screen.blit(label, (X - 10, Y  + 10))
	label = myfont.render(control, 5, colour)
	screen.blit(label, (X , Y  + 25))
	label = myfont.render(str(int(value)), 5, colour)
	screen.blit(label, (X - 5, Y  - 20 - value))

#show the sun and the time

def displaytime(hour,sunlight, season):
	X_increment = (width - 200)/24
	X = int(100 + X_increment*hour)
	Y = int(100)
	pygame.draw.circle(screen, (255,255,0), (X,Y), int(sunlight*100))
	X = 100
	Y = 100
	label = myfont.render('Time : ' + str(int(hour)) + ':00', 5, (0,0,0))
	screen.blit(label, (X , Y ))
	if season == 0:
		label = myfont.render('spring', 5, (0,0,0))
		screen.blit(label, (X , Y + 20))
	elif season == 1:
		label = myfont.render('summer', 5, (0,0,0))
		screen.blit(label, (X , Y + 20))
	elif season == 2:
		label = myfont.render('autumn', 5, (0,0,0))
		screen.blit(label, (X , Y + 20))
	elif season == 3:
		label = myfont.render('winter', 5, (0,0,0))
		screen.blit(label, (X , Y + 20))
	label = myfont.render('Age : ' + str(int(age)) + ' / ' + str(int(max_age)), 5, (0,0,0))
	screen.blit(label, (X , Y + 40 ))

#DIE

def gameoverfail():
	rendermessage(['You died without reproducing!', 
		'You only got ' + str(int(reproductase)) + ' reproductase.',
		'Youll never make it to the space stage with performace like that!'])
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
				if event.key == K_SPACE:
					run = False
	pygame.quit()

#live

def gameoverwin():
	rendermessage(['You did it!', 
		'Good Job Buddy.',
		'Your descendants will cross the stars!'])
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
				if event.key == K_SPACE:
					run = False
	pygame.quit()

#random events stack

def event1():
	global health 
	rendermessage(['Under attack!',
					'Lose 20 Health'])
	health -= 20

def event2():
	global reproductase
	rendermessage(['Sprung a leak!',
					'Lose half your reproductase!'])
	reproductase = 0.5*reproductase

def event3():
	global toxin
	global health
	if toxin >= 20:
		rendermessage(['Attacked',
					'Good thing you had Toxin!'])
		toxin -= 15
		return
	else:
		rendermessage(['Attacked',
					'Without Toxin to defend yourself you got hurt bad!'])
		health -= 50
		return

listofevents = [event1, event2, event3]


#days run from 0-19, seasons 0-3 with spring = 0
#lots of variables!
# to change speed change timestep, max age is death criteria, wincondition is the win condition for reproductase

age = 0
max_age = 40
timestep = 0.02
hour = 0
sunlight = 0
day = 0
season = 0
season_modifier = 1
nutrients = 200
base_nutrients = 300
max_nutirents = 2*base_nutrients
nutrients_stored = 0
size = 5
max_health = size * 20
health = size * 20
compounds_stored_max = size*20 
running = True
storing = False
making_cytoplasm = False
cytoplasm = 0
making_protein = False
protein = 0
making_toxin = False
toxin = 0
making_reproductase = False
reproductase = 0
growing = False
repairing = False
wincondition = 50
pause = False

rendermessage(['Hi',
	'This is a prototype for gameplay as a photosynthesizing microbe.',
	'Nutrients can be stored and then turned into Protein and Cytoplasm.',
	'Cytoplasm can be turned into growth and repair.',
	'Protein can be turned into Toxin.',
	'Both protein and cytoplasm are needed to make reproductase',
	'Random events will happen and you must adapt to them as the seasons change.',
	'Your goal is to make ' + str(wincondition) + ' reproductase before you die of old age at age = ' + str(max_age),
	'Nutrients are most available in the Spring and Autumn',
	'Youll need to grow to be able to store more compounds',
	'You need sunlight to make protein, the amount of sunlight is that big yellow ball in the sky!',
	'Producing protein in the night wastes resources! You have been warned.',
	'Press SPACE to pause',
	'Good Luck!'])

while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_s:
	        	storing = not storing
	        if event.key == K_c:
	        	making_cytoplasm = not making_cytoplasm
	        if event.key == K_p:
	        	making_protein = not making_protein
	        if event.key == K_g:
	        	growing = not growing
	        if event.key == K_r:
	        	repairing = not repairing
	        if event.key == K_t:
	        	making_toxin = not making_toxin
	        if event.key == K_x:
	        	making_reproductase = not making_reproductase
	        if event.key == K_SPACE:
	        	pause = not pause
	
	
	if pause:
		label = myfont.render('PAUSE', 5, (0,0,0))
		screen.blit(label, (780 , 400))
		pygame.display.flip()
		while pause:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pause = False
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						pause = False
					if event.key == K_SPACE:
						pause = False

	choice = random.randint(0,10000)
	if choice <= 1:
		i = random.choice(listofevents)
		i()
    

	screen.fill(background_colour)

	displaytime(hour, sunlight, season)

	
	displaybar('Nut.',1,nutrients,' ', True)

	displaybar('Nut. In', 2, nutrients_stored, 'S', storing)

	displaybar('Cyto.', 3, cytoplasm, 'C', making_cytoplasm)

	displaybar('Size', 4, size, 'G', growing)

	displaybar('Health', 5, health, 'R', repairing)

	displaybar('Prot.', 6, protein, 'P', making_protein)

	displaybar('Toxin', 7, toxin, 'T', making_toxin)

	displaybar('Repro.', 8, reproductase, 'X', making_reproductase)

	pygame.display.flip()

	if reproductase >= wincondition:
		gameoverwin()
	if health <= 0:
		gameoverfail()

	
	hour += timestep
	if hour >= 24:
		hour = 0
		day += 1
		age += 1
		if age >= max_age:
			gameoverfail()
		if day >= 20:
			day = 0
		season = int(day/5)
		season_modifier = math.sin((math.pi/3) + season*(math.pi/6))
		nutrients = base_nutrients*(1 + (math.cos(day*math.pi/7)))/((day/4) + 1)
	
	if storing and nutrients >= 0 and nutrients_stored >= 0 and nutrients_stored <= compounds_stored_max:
		difference = - nutrients_stored + nutrients
		nutrients -= 0.01*difference
		nutrients_stored += 0.01*difference


	if making_cytoplasm and (nutrients_stored >= 1) and cytoplasm <= compounds_stored_max:
		nutrients_stored -= 0.1
		cytoplasm += 0.1

	if making_protein and (nutrients_stored >= 1) and protein <= compounds_stored_max:
		nutrients_stored -= 0.3
		protein += 0.2*sunlight

	if making_reproductase and (protein >= 1) and (cytoplasm >= 1):
		protein -= 0.1
		cytoplasm -= 0.1
		reproductase += 0.01

	if making_toxin and (protein >= 1) and toxin <= compounds_stored_max:
		protein -= 0.3
		toxin += 0.1

	if growing and (cytoplasm >= 1):
		cytoplasm -= 0.2
		size += 0.01
		compounds_stored_max = size*20

	if repairing and (cytoplasm >= 1) and (health <= max_health):
		cytoplasm -= 0.3
		health += 0.1

	if protein >= 5*nutrients_stored and protein >= 10:
		protein -= 0.1
		nutrients_stored += 0.1

	if cytoplasm >= 5*nutrients_stored and cytoplasm >= 10:
		cytoplasm -= 0.1
		nutrients_stored += 0.1
	
	sunlight = max(0,season_modifier*math.sin((hour - 4)*math.pi/16))

pygame.quit()
