import pygame
import math
import random
from pygame.locals import *

import timeit


#setup

hc = 1.98e-25 #planks constant time speed of light
hc2 = 5.95e-17 #planks constant times speed of light squared
kB = 1.38e-23 #Boltzmanns constant
wavelength_step = 1e-7 # 0.1 microns per step, there are 30 steps so this is 3 microns. 
#visible spectrum for humans is 0.38 - 0.75 microns

scaling = 0.2e-13 #scaling down the result so it can fit on the graph, bit of a fudge



background_colour = (255,255,255)
(width, height) = (1200, 600)

screen = pygame.display.set_mode((width, height + 200))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be LIGHT')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

#how many points the spectrum made of.
dimension_of_sample = 30

#take two spectra and multuply them pointwise
def combine_two_spectra(spectrum_1, spectrum_2):
	result = []
	for i in range(dimension_of_sample):
		result.append(spectrum_1[i]*spectrum_2[i])
	return result

#how much light does a black body put out at a certain temperature, standard formula
def planks_law(temperature, wavelength):
	partial = math.exp(hc/(wavelength*kB*temperature)) - 1
	final = 2*hc2/(partial*(wavelength**5))
	return final*scaling

#generate the spectrum coming out of the sun based on the termperature
def generate_stellar_spectrum(Earth = False):
	result = []
	global temperature 
	if Earth: temperature = 5778
	else: temperature = random.randint(3000,7000)
	for i in range(dimension_of_sample):
		result.append(planks_law(temperature, wavelength_step*(i + 1)))
	return result

#block some of the spectrum based on the atmospheric gasses
def generate_atmospheric_absorbtion():
	result = []
	global N2, O2, H2O, O3, CO2
	N2 = random.uniform(0.6,0.8)
	O2 = random.uniform(0.9,1)
	H2O = random.uniform(0.6,0.8)
	O3 = random.uniform(0.8,1)
	CO2 = random.uniform(0.9,1)
	for i in range(dimension_of_sample):
		result.append(1)
	result[0] *= N2*O2
	result[1] *= N2*O2*H2O
	result[2] *= O2*H2O*O3
	result[3] *= O3
	result[4] *= O3
	result[5] *= O3
	result[6] *= O3*H2O*O2
	result[7] *= O3*H2O*O2
	result[8] *= H2O*O2
	result[9] *= H2O
	result[10] *= O2
	result[11] *= H2O
	result[12] *= O2
	result[13] *= H2O
	result[14] *= CO2
	result[15] *= O2
	result[16] *= CO2
	result[18] *= H2O
	result[20] *= CO2
	result[27] *= H2O*CO2
	return result

#block some of the spectrum based on the pigment, currently none
def generate_pigment_absorbtion():
	result = []
	for i in range(dimension_of_sample):
		result.append(1)
	return result

#generate the spectra of the colour receptors in the eye, random or human RGB approximation
def generate_receptor_spectrum(colour = False):
	result = []
	if colour == "R":
		for i in range(dimension_of_sample):
			if i == 4: result.append(0.2)
			elif i == 5: result.append(0.6)
			elif i == 6: result.append(1)
			elif i == 7: result.append(0.4)
			else: result.append(0)
	elif colour == "G":
		for i in range(dimension_of_sample):
			if i == 5: result.append(0.6)
			elif i == 6: result.append(0.6)
			else: result.append(0)
	elif colour == "B":
		for i in range(dimension_of_sample):
			if i == 4: result.append(0.6)
			elif i == 5: result.append(0.6)
			else: result.append(0)
	else:
		shift = random.randint(0,30)
		for i in range(dimension_of_sample):
			result.append(max(0,2*(float(2*i - shift)/30 - (float(2*i - shift)/30)**2)))
	return result

#take the spectra of the receptors and of the light and compare them
def get_perceived_colour(receptor_spectrum_1, receptor_spectrum_2, receptor_spectrum_3, light):
	spectrum_in_eye_1 = combine_two_spectra(receptor_spectrum_1, light)
	spectrum_in_eye_2 = combine_two_spectra(receptor_spectrum_2, light)
	spectrum_in_eye_3 = combine_two_spectra(receptor_spectrum_3, light)
	R = sum(spectrum_in_eye_1)
	G = sum(spectrum_in_eye_2)
	B = sum(spectrum_in_eye_3)
	factor = float(255)/(max(R,G,B) + 0.1)
	R *= factor
	G *= factor
	B *= factor
	return [int(R),int(G),int(B)]

#cut the spectrum into pieces with lines of 1/wavelength**4 being constant
def generate_rayleigh_spectrum(receptor_spectrum_1, receptor_spectrum_2, receptor_spectrum_3, spectrum):
	result = []
	start_constant = 0
	working_spectrum = []
	for i in range(dimension_of_sample):
		working_spectrum.append(spectrum[i])
	for i in range(dimension_of_sample):
		constant = spectrum[i] - ((i+0.1)**-4)
		if constant >= start_constant:
			start_constant = constant
	for i in range(dimension_of_sample):
		current_constant = start_constant*(1-(float(i)/dimension_of_sample))
		current_spectrum = []
		for j in range(dimension_of_sample):
			value = max(0, working_spectrum[j] - (current_constant + ((j+0.1)**-4)))
			current_spectrum.append(value)
			working_spectrum[j] -= 0.3*value
		perceived_colour = get_perceived_colour(receptor_spectrum_1, receptor_spectrum_2, receptor_spectrum_3, current_spectrum)
		value = sum(current_spectrum)
		result.append([value, perceived_colour])
	return result

#draw the spectrum as a graph
def display_spectrum(spectrum, number, top, colour = False):
	Y_SHIFT = 0
	if not top: Y_SHIFT = height/2
	X_SHIFT = number*width/4
	true_height = height/2 - 20
	true_width = width/4 - 20
	#draw the axes
	pygame.draw.line(screen, [255,0,0], (X_SHIFT + 10,Y_SHIFT + 10), (X_SHIFT + 10, Y_SHIFT + true_height + 10), 1)
	pygame.draw.line(screen, [255,0,0], (X_SHIFT + true_width + 10, Y_SHIFT + true_height + 10), (X_SHIFT + 10, Y_SHIFT + true_height + 10), 1)
	#draw a thick red line for human visible spectrum
	pygame.draw.line(screen, [255,0,0], (X_SHIFT + 10 + true_width*3/dimension_of_sample, Y_SHIFT + true_height + 10), (X_SHIFT + 10 + true_width*8/dimension_of_sample, Y_SHIFT + true_height + 10), 5)
	colour_of_line = [0,0,255]
	if colour == "R": colour_of_line = [255,0,0]
	if colour == "G": colour_of_line = [0,255,0]
	for i in range(dimension_of_sample - 1):
		pygame.draw.line(screen, colour_of_line, (X_SHIFT + 10 + true_width*i/dimension_of_sample, height/2 - 10 - true_height*spectrum[i] + Y_SHIFT), (X_SHIFT + 10 + true_width*(i + 1)/dimension_of_sample, height/2 - 10 - true_height*spectrum[i + 1] + Y_SHIFT), 1)

#draw the box in the top righ
def display_colour(rgb, intensity):
	X_SHIFT = 3*width/4
	Y_SHIFT = height/2
	pygame.draw.polygon(screen, rgb*intensity, ([X_SHIFT + 10, 10], [width - 10, 10], [width - 10, Y_SHIFT - 10], [X_SHIFT + 10, Y_SHIFT - 10]))

#draw the bars of rayleigh spectrum along the bottom
def display_rayleigh(rayleigh_spectrum):
	number_of_samples = len(rayleigh_spectrum)
	scaling = 0
	for i in range(number_of_samples):
		if rayleigh_spectrum[i][0] >= scaling:
			scaling = rayleigh_spectrum[i][0]
	for i in range(number_of_samples):
		pygame.draw.line(screen, rayleigh_spectrum[i][1], (width - int(float((i+0.5)*width)/number_of_samples), height + 200), (width - int(float((i+0.5)*width)/number_of_samples), height), int(float(width)/number_of_samples))

def reset():
	global intensity
	intensity = 1
	screen.fill(background_colour)
	#start timer
	tic=timeit.default_timer()	
	#generate light from star
	stellar_spectrum = generate_stellar_spectrum(Earth = True)
	#generate bsorbtion bands for the atmosphere
	atmospheric_absorbtion = generate_atmospheric_absorbtion()
	#generate light that made it through the atmosphere
	light_in_atmosphere = combine_two_spectra(stellar_spectrum, atmospheric_absorbtion)
	#generate the pigment
	pigment = generate_pigment_absorbtion()
	#generate light that makes it past the pigment
	light_after_pigment = combine_two_spectra(pigment, light_in_atmosphere)
	#generate the receptor spectra
	receptor_spectrum_1 = generate_receptor_spectrum("R")
	receptor_spectrum_2 = generate_receptor_spectrum("G")
	receptor_spectrum_3 = generate_receptor_spectrum("B")

	#calculate perceived colour
	perceived_colour = get_perceived_colour(receptor_spectrum_1,receptor_spectrum_2,receptor_spectrum_3,light_after_pigment)

	#calculate the resulting rayleigh spectrum
	rayleigh = generate_rayleigh_spectrum(receptor_spectrum_1, receptor_spectrum_2, receptor_spectrum_3,light_after_pigment)

	toc=timeit.default_timer()
	#display all the spectra
	display_spectrum(stellar_spectrum,0,True)	
	display_spectrum(atmospheric_absorbtion,1,False)
	display_spectrum(light_in_atmosphere,1,True)
	display_spectrum(pigment,2,False)
	display_spectrum(light_after_pigment,2,True)
	display_spectrum(receptor_spectrum_1,3,False, colour = "R")
	display_spectrum(receptor_spectrum_2,3,False, colour = "G")
	display_spectrum(receptor_spectrum_3,3,False)

	display_colour(perceived_colour,intensity)

	#display all labels in the bottom left
	label = myfont.render("TEMPERATURE : " + str(temperature), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 60))
	label = myfont.render("TIME : " + str(toc - tic), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 40))
	label = myfont.render("N2 : " + str(N2), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 80))
	label = myfont.render("O2 : " + str(O2), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 100))
	label = myfont.render("CO2 : " + str(CO2), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 120))
	label = myfont.render("O3 : " + str(O3), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 140))
	label = myfont.render("H2O : " + str(H2O), 1, (0,0,0))
	screen.blit(label, (10, height/2 + 160))

	display_rayleigh(rayleigh)
	

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