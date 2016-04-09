#how much is light attenuated as it passes through a gas?

import math

Avagadro = 6.022e23
molecular_mass_nitrogen = 0.028 # kg mol^-1
molecular_mass_water = 0.018 # kg mol^-1
molecular_mass_methane = 0.016 # kg mol^-1
molecular_mass_helium = 0.004 # kg mol^-1
radius_of_earth = 6.37e6 #meters
mass_of_earth_atmosphere = 5.14e18 #kg
#from https://en.wikipedia.org/wiki/Kinetic_diameter
Water_diameter = 9.0e-11 #meters
Nitrogen_diameter = 7.5e-11 # meters	
Carbon_dioxide_diameter = 9e-11 #meters
Oxygen_diameter = 7.3e-11 #meters


def compute_surface_area_from_radius(radius):
	return 4*math.pi*(radius**2) 

def mass_of_gas_in_1sqm(radius, mass_of_gas):
	surface_area = compute_surface_area_from_radius(radius)
	mass_in_1sqm = float(mass_of_gas)/surface_area
	return mass_in_1sqm

def atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass):
	mass_in_1sqm = mass_of_gas_in_1sqm(radius, mass_of_gas)
	number_of_moles = float(mass_in_1sqm)/molecular_mass
	number_of_atoms = number_of_moles*Avagadro
	return number_of_atoms

print "Atoms of gas in a 1sqm column of air, ",
print atoms_of_gas_in_1sqm(radius_of_earth, mass_of_earth_atmosphere, molecular_mass_nitrogen)

def attenuation_parameter(radius, mass_of_gas, molecular_mass, molecular_area):
	number_of_atoms = atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass)
	exponent = -number_of_atoms*molecular_area
	print "Light getting through = exp(", exponent, ") = ",
	return math.exp(exponent)

print attenuation_parameter(radius_of_earth, 0.7*mass_of_earth_atmosphere, 
			molecular_mass_nitrogen, Nitrogen_diameter**2)
