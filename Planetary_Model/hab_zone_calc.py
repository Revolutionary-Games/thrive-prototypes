import math
import random


small_delta = 0.01
albedo = 0.65
Stephan = 5.67e-8 # Watts meters^-2 Kelvin^-4 constnat
luminosity_of_sun = 3.85e+26 # watts
orbital_diameter = 1.496e11 # meters
max_orbital_diameter = 7.78e11 # meters (radius of jupiter)
min_orbital_diameter = 5.5e10 # meters (radius of mercury)
number_of_tests = 100 # number of different locations to test
oxygen_param = 0.3 # amount of sunlght ozone can block if atmosphere is 100 oxgen
carbon_dioxide_param = 0.3 # same
water_vapour_param = 0.3 #same

def compute_temp_change(incoming_sunglight, carbon_dioxide, oxygen, water_vapour, albedo, temperature):
	return ((1 - albedo)*(1 - oxygen*oxygen_param)*incoming_sunglight 
		- (1 - water_vapour*water_vapour_param)*
		(1 - carbon_dioxide*carbon_dioxide_param)*Stephan*temperature**4)

def compute_incoming_sunlight(stellar_luminosity, radius_of_orbit):
	return stellar_luminosity/(4*math.pi*(radius_of_orbit**2))

def compute_water_vapour(temperature):
	if temperature < 273:
		return 0
	if temperature > 373:
		return 1
	else:
		return (temperature - 273)/100

def compute_albedo(temperature):
	if temperature < 273:
		return 0.7
	if temperature > 373:
		return 0.6
	else:
		return 0.7 - (0.1*(temperature - 273)/100)


def compute_temperature(carbon_dioxide, oxygen):
	temp = 200
	for l in range(1000):
		water_vapour = compute_water_vapour(temp)
		albedo = compute_albedo(temp)
		temp += compute_temp_change(incoming_sunglight, carbon_dioxide, oxygen, water_vapour, albedo, temp)*small_delta
	return temp


#storing the values of how habitable that position is
scores = [0 for j in range(100)]

#step through the radii
radius_step = float(max_orbital_diameter)/number_of_tests
counter = 0
for i in range(int(min_orbital_diameter), int(max_orbital_diameter), int(radius_step)):
	#compute how much sunlight reachers the planet per sq meter
	incoming_sunglight = compute_incoming_sunlight(luminosity_of_sun, i)
	#test 10 different values of carbon dioxide
	for j in range(10):
		carbon_dioxide = 0.1*j
		#test 10 different values of oxygen
		for k in range(10):
			oxygen = 0.1*k
			temp = compute_temperature(carbon_dioxide, oxygen)
			if temp < 373 and temp > 273:
				scores[counter] += 1

	counter += 1
	print counter, " percent complete."

print scores

