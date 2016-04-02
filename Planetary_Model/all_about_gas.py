import math
import random

radius_of_earth = 6.37e6 #meters
mass_of_mercury = 3.285e23 #kg
mass_of_earth = 5.972e24 #kg
mass_of_mars = 6.39e23 #kg
mass_of_jupiter = 1.898e27 #kg
gravity_constant = 6.674e-11 # N m^2/kg^2
gas_constant = 8.3144598 # J mol^-1 K^-1
molecular_mass_nitrogen = 0.028 # kg mol^-1
molecular_mass_helium = 0.004 # kg mol^-1
Boltzmann = 1.3803e-23 # J K^-1
Avagadro =  6.0221e23

#assuming all rocky planets are the same density as earth radius and mass are directly related
def compute_radius_from_mass(mass):
	radius = (float(3*mass)/(4*math.pi*5515.3))**0.333
	return radius

print "Radius of earth calculated = ", compute_radius_from_mass(mass_of_earth), " should be = ", radius_of_earth

#compute the escape velocity in ms^-1 using purely newtonian gravity
def compute_escape_velocity(mass):
	radius = compute_radius_from_mass(mass)
	return math.sqrt(2*gravity_constant*mass/radius)

#root mean square velocity of a gas
def compute_gas_velocity(temperature, gas_molecular_weight):
	return math.sqrt(3*gas_constant*temperature/gas_molecular_weight)

#the speed at the equator (the fastest part of the planet)
def compute_surface_velocity(mass, period_of_rotation):
	radius = compute_radius_from_mass(mass)
	return 2*math.pi*radius/period_of_rotation

print "For the earth:"
print "Escape Velocity = ", compute_escape_velocity(mass_of_earth), " should be 11,200 ms^-1"
print "Gas Velocity of Nitrogen = ", compute_gas_velocity(310, molecular_mass_nitrogen)
print "Gas Velocity of Helium = ", compute_gas_velocity(310, molecular_mass_helium), " should be 1390."
print "Surface Velocity = ", compute_surface_velocity(mass_of_earth, 24*60*60), " should be 460 ms^-1"

def compute_maxwell_boltzmann(mass, temperature, velocity):
	return (math.sqrt((float(mass)/float(2*math.pi*Boltzmann*temperature))**3)*
			4*math.pi*(velocity**2)*math.exp(-float(mass*(velocity**2))/float(2*Boltzmann*temperature)))


print "Maxwell Boltzmann at 310K"
print "Mercury, Nitrogen:", compute_maxwell_boltzmann(molecular_mass_nitrogen/Avagadro, 
				310, compute_escape_velocity(mass_of_mercury))
print "Mercury, Helium:", compute_maxwell_boltzmann(molecular_mass_helium/Avagadro, 
				310, compute_escape_velocity(mass_of_mercury))
print "Earth, Nitrogen:", compute_maxwell_boltzmann(molecular_mass_nitrogen/Avagadro, 
				310, compute_escape_velocity(mass_of_earth))
print "Earth, Helium:", compute_maxwell_boltzmann(molecular_mass_helium/Avagadro, 
				310, compute_escape_velocity(mass_of_earth))
print "Mars, Nitrogen:", compute_maxwell_boltzmann(molecular_mass_nitrogen/Avagadro, 
				310, compute_escape_velocity(mass_of_mars))
print "Mars, Helium:", compute_maxwell_boltzmann(molecular_mass_helium/Avagadro, 
				310, compute_escape_velocity(mass_of_mars))
print "Jupiter, Nitrogen:", compute_maxwell_boltzmann(molecular_mass_nitrogen/Avagadro, 
				310, compute_escape_velocity(mass_of_jupiter))
print "Jupiter, Helium:", compute_maxwell_boltzmann(molecular_mass_helium/Avagadro, 
				310, compute_escape_velocity(mass_of_jupiter))