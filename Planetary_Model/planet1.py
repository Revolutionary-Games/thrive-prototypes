import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Planetary Model')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

Luminosity_of_our_sun = 3.846e26 #watts
Radius_of_our_sun = 6.96e8 #meters
Stephan = 5.67e-8 # Watts meters^-2 Kelvin^-4 constnat
hc = 1.98e-25 #planks constant time speed of light
hc2 = 5.95e-17 #planks constant times speed of light squared
kB = 1.38e-23 #Boltzmanns constant
wavelength_step = 1e-7 # 0.05 microns per step, there are 50 steps so this is 2.5 microns. 
#visible spectrum for humans is 0.38 - 0.75 microns
dimension_of_sample = 50 #the spectrum is defined by 50 points

#from wikipedia table https://en.wikipedia.org/wiki/File:Representative_lifetimes_of_stars_as_a_function_of_their_masses.svg
def get_life_span(mass):
	return 1e10/(mass**3)

#from wikipedia https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
def get_luminosity(mass):
	return Luminosity_of_our_sun*(mass**3.5)

#from (7.14c) of http://physics.ucsd.edu/students/courses/winter2008/managed/physics223/documents/Lecture7%13Part3.pdf
def get_radius(mass):
	return Radius_of_our_sun*(mass**1)

#from the same page as luminosity using the formula for temperature and luminosity
def get_temperature(luminosity, radius):
	return (luminosity/(4*math.pi*Stephan*(radius**2)))**0.25

#planks law for black body radiations
def planks_law(temperature, wavelength):
	partial = math.exp(hc/(wavelength*kB*temperature)) - 1
	final = 2*hc2/(partial*(wavelength**5))
	return final

#work out the spectrum of the light emitted by the star as a pure black body
def generate_stellar_spectrum(temperature):
	result = []
	for i in range(dimension_of_sample):
		result.append(planks_law(temperature, wavelength_step*(i + 1)))
	return result

class star:
	def __init__(self):
		#Measured in multiples of the the sun's mass
		self.mass = random.uniform(0.5,3)
		#Number of our years the star will live for
		self.life_span = get_life_span(self.mass)
		#because the lifespans of the stars are so short there can be no life around
		#a star which may go supernova :(
		#power output of the star
		self.luminosity = get_luminosity(self.mass)
		#radius of the star
		self.radius = get_radius(self.mass)
		#what temperature is the star
		self.temperature = get_temperature(self.luminosity, self.radius)
		#get the light spectrum emitted
		self.spectrum = generate_stellar_spectrum(self.temperature)

		print "Created new main sequence star"
		print "Mass = ", self.mass, " solar masses."
		print "Life Span = ", '%.2e' % self.life_span, " of our years."
		print "Luminosity = ", '%.2e' % self.luminosity, " watts."
		print "Radius = ", '%.2e' % self.radius, " meters."
		print "Temperature = ", self.temperature, " Kelvin."
		print self.spectrum


our_star = star()

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        


	screen.fill(background_colour)

	pygame.display.flip()
	

pygame.quit()