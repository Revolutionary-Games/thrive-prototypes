import pygame
import math
import random
from pygame.locals import *

import timeit


#setup

background_colour = (255,255,255)
(width, height) = (1200, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be LIGHT')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

dimension_of_sample = 30

def combine_two_spectra(spectrum_1, spectrum_2):
	result = []
	for i in range(dimension_of_sample):
		result.append(spectrum_1[i]*spectrum_2[i])
	return result

def generate_stellar_spectrum():
	result = []
	for i in range(dimension_of_sample):
		result.append(random.uniform(0.3,0.6))
	return result

def generate_atmospheric_absorbtion():
	result = []
	for i in range(dimension_of_sample):
		if i == 3 or i == 10 or i == 20: result.append(0)
		else: result.append(1)
	return result

def generate_pigment_absorbtion():
	result = []
	for i in range(dimension_of_sample):
		if i == 6 or i == 9 or i == 15: result.append(0)
		else: result.append(1)
	return result

def generate_receptor_spectrum():
	result = []
	for i in range(dimension_of_sample):
		result.append(float(i)/30 - (float(i)/30)**2)
	return result

#draw the spectrum as a graph
def display_spectrum(spectrum, number, top):
	Y_SHIFT = 0
	if not top: Y_SHIFT = height/2
	X_SHIFT = number*width/4
	true_height = height/2 - 20
	true_width = width/4 - 20
	pygame.draw.line(screen, [255,0,0], (X_SHIFT + 10,Y_SHIFT + 10), (X_SHIFT + 10, Y_SHIFT + true_height + 10), 1)
	pygame.draw.line(screen, [255,0,0], (X_SHIFT + true_width + 10, Y_SHIFT + true_height + 10), (X_SHIFT + 10, Y_SHIFT + true_height + 10), 1)
	for i in range(dimension_of_sample - 1):
		pygame.draw.line(screen, [0,0,255], (X_SHIFT + 10 + true_width*i/dimension_of_sample, height/2 - 10 - true_height*spectrum[i] + Y_SHIFT), (X_SHIFT + 10 + true_width*(i + 1)/dimension_of_sample, height/2 - 10 - true_height*spectrum[i + 1] + Y_SHIFT), 1)

def reset():
	screen.fill(background_colour)
	#start timer
	tic=timeit.default_timer()	
	#generate light from star
	stellar_spectrum = generate_stellar_spectrum()
	#generate bsorbtion bands for the atmosphere
	atmospheric_absorbtion = generate_atmospheric_absorbtion()
	#generate light that made it through the atmosphere
	light_in_atmosphere = combine_two_spectra(stellar_spectrum, atmospheric_absorbtion)
	#generate the pigment
	pigment = generate_pigment_absorbtion()
	#generate light that makes it past the pigment
	light_after_pigment = combine_two_spectra(pigment, light_in_atmosphere)
	#generate the receptor spectrum
	receptor_spectrum = generate_receptor_spectrum()
	#calculate if the receptor fires
	spectrum_in_eye = combine_two_spectra(receptor_spectrum, light_after_pigment)
	answer = sum(spectrum_in_eye)
	toc=timeit.default_timer()
	#display all the spectra
	display_spectrum(stellar_spectrum,0,True)	
	display_spectrum(atmospheric_absorbtion,1,False)
	display_spectrum(light_in_atmosphere,1,True)
	display_spectrum(pigment,2,False)
	display_spectrum(light_after_pigment,2,True)
	display_spectrum(receptor_spectrum,3,False)

	if answer >= 1.7:
		label = myfont.render("SEEN : " + str(answer), 1, (0,0,0))
		screen.blit(label, (3*width/4 + 10, 20))
	else:
		label = myfont.render("NOT SEEN : " + str(answer), 1, (0,0,0))
		screen.blit(label, (3*width/4 + 10, 20))
	label = myfont.render("TIME : " + str(toc - tic), 1, (0,0,0))
	screen.blit(label, (3*width/4 + 10, 40))

	pygame.display.flip()
	


reset()

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	        	reset() 
	        
pygame.quit()