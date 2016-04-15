#how much is light attenuated as it passes through a gas?

import math

Avagadro = 6.022e23
molecular_mass_carbon_dioxide = 0.044 # kg mol^-1
molecular_mass_oxygen = 0.032 # kg mol^-1
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
print " "

def attenuation_parameter(fudge_factor, radius, mass_of_gas, molecular_mass, molecular_area):
	number_of_atoms = atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass)
	exponent = -fudge_factor*number_of_atoms*molecular_area
	return math.exp(exponent)

def compute_fudge_factor(desired_transmittance, radius, mass_of_gas, molecular_mass, molecular_area):
	number_of_atoms = atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass)
	exponent = -number_of_atoms*molecular_area
	print "Current exponent = ", exponent
	print "Desired exponent = ", math.log(desired_transmittance)
	fudge_factor = float(math.log(desired_transmittance))/exponent
	print "Fudge Factor = ", fudge_factor
	return fudge_factor

print "Compute fudge for nitrogen to get 0.5 transmittance"

fudge_nitrogen = compute_fudge_factor(0.5, radius_of_earth, mass_of_earth_atmosphere*0.78, 
			molecular_mass_nitrogen, Nitrogen_diameter**2)

attenuation_nitrogen = attenuation_parameter(fudge_nitrogen, radius_of_earth, mass_of_earth_atmosphere*0.78, 
			molecular_mass_nitrogen, Nitrogen_diameter**2)

print "Nitrogen transmittance = ", attenuation_nitrogen
print " "

print "Compute fudge for oxygen to get 0.5 transmittance"

fudge_oxygen = compute_fudge_factor(0.5, radius_of_earth, mass_of_earth_atmosphere*0.2, 
			molecular_mass_oxygen, Oxygen_diameter**2)

attenuation_oxygen = attenuation_parameter(fudge_oxygen, radius_of_earth, mass_of_earth_atmosphere*0.2, 
			molecular_mass_oxygen, Oxygen_diameter**2)

print "Oxygen transmittance = ", attenuation_oxygen
print " "

print "Compute fudge for water to get 0.5 transmittance"

fudge_water = compute_fudge_factor(0.5, radius_of_earth, mass_of_earth_atmosphere*0.04, 
			molecular_mass_water, Water_diameter**2)

attenuation_water = attenuation_parameter(fudge_water, radius_of_earth, mass_of_earth_atmosphere*0.04, 
			molecular_mass_water, Water_diameter**2)

print "Water transmittance = ", attenuation_water
print " "

print "Compute fudge for carbon dioxide to get 0.5 transmittance"

fudge_carbon_dioxide = compute_fudge_factor(0.5, radius_of_earth, mass_of_earth_atmosphere*0.04, 
			molecular_mass_carbon_dioxide, Carbon_dioxide_diameter**2)

attenuation_carbon_dioxide = attenuation_parameter(fudge_carbon_dioxide, radius_of_earth, mass_of_earth_atmosphere*0.04, 
			molecular_mass_carbon_dioxide, Carbon_dioxide_diameter**2)

print "Carbon dioxide transmittance = ", attenuation_carbon_dioxide
print " "