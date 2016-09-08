
import math
import random

Earth = True # should you generate the Earth as closely as possible?
if Earth: 
	print "Generating the Earth as closely as possible"
else:
	print "Generating a new planet!"

Gravitational_Constant = 6.674e-11# Newtons Meters^2 / kg^2
Luminosity_of_our_sun = 3.846e26 #watts
Mass_of_our_sun = 1.989e30 #kg
Radius_of_our_sun = 6.96e8 #meters
Radius_of_the_earth = 6.371e6 #meters
Stephan = 5.67e-8 # Watts meters^-2 Kelvin^-4 constnat
hc = 1.98e-25 #planks constant time speed of light
hc2 = 5.95e-17 #planks constant times speed of light squared
kB = 1.38e-23 #Boltzmanns constant
wavelength_step = 5e-8 # 0.05 microns per step, there are 50 steps so this is 2.5 microns. 
#visible spectrum for humans is 0.38 - 0.75 microns
dimension_of_sample = 50 #the spectrum is defined by 50 points
small_delta = 0.01 #step size for the climate differential equation
albedo = 0.65 #base albedo value (planetary reflectivity)
base_max_orbital_diameter = 7.78e11 # meters (radius of jupiter)
base_min_orbital_diameter = 5.5e10 # meters (radius of mercury)
number_of_tests = 100 # number of different planetary locations to test
oxygen_param = 0.3 # amount of sunlght ozone can block if atmosphere is 100 oxgen
carbon_dioxide_param = 0.3 # same
water_vapour_param = 0.3 #same
detail = 3#number of different values of CO2 and O2 to check, more is better but very intensive
minimum_planet_radius = 5375699 #smallest radius allowed, see http://forum.revolutionarygamesstudio.com/t/planet-generation/182/10
maximum_planet_radius = 9191080 #largest radius allowed
density_of_earth = 5515.3 #kg m^-3, assume all planets are the same density as earth
percentage_atmopshere = 8.62357669e-7 #percentage of the earths mass which is atmosphere
percentage_ocean = 2.26054923e-7 #percentage that is ocean
percentage_lithosphere = 1.67448091e-7 #percentage that is rock, just a guess in line with others
fudge_factor_nitrogen = 7.28704114055e-10 #calibrate the spectral computations using earths atmosphere
fudge_factor_water = 6.34362956432e-09 #same
fudge_factor_carbon_dioxide = 1.55066500461e-08 #same
fudge_factor_oxygen = 3.42834549545e-09 #same
Avagadro = 6.022e23 #avagadros constant relating number of atoms to mass
molecular_mass_carbon_dioxide = 0.044 # kg mol^-1, mass of 1 mole of CO2
molecular_mass_oxygen = 0.032 # kg mol^-1, mass of 1 mole of O2
molecular_mass_nitrogen = 0.028 # kg mol^-1, mass of 1 mole of N2
molecular_mass_water = 0.018 # kg mol^-1, mass of 1 mole of H2O
diameter_water = 9.0e-11 #meters, size of a water molecule for interaction with light
diameter_nitrogen = 7.5e-11 # meters	
diameter_carbon_dioxide = 9e-11 #meters
diameter_oxygen = 7.3e-11 #meters



#list of compounds, see http://forum.revolutionarygamesstudio.com/t/cpa-master-list/167
compounds = ["Sulfur", "Hydrogen Sulfide", "Water", "Oxygen", "Nitrogen", 
			"Carbon Dioxide", "Ammonia", "Phosphates", "ATP", "Glucose",
			"Pyruvate", "Amino Acids", "Fat", "Protein", "Agents", "Nucleotide",
			"DNA"]

#from wikipedia table https://en.wikipedia.org/wiki/File:Representative_lifetimes_of_stars_as_a_function_of_their_masses.svg
def get_life_span(mass):
	return 1e10/(mass**3)

#from wikipedia https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
def get_luminosity(mass):
	return Luminosity_of_our_sun*(mass**3.5)

#from (7.14c) of http://physics.ucsd.edu/students/courses/winter2008/managed/physics223/documents/Lecture7%13Part3.pdf
def get_radius(mass):
	return Radius_of_our_sun*(mass**0.9)

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

#simple formula for surface area of a sphere
def compute_surface_area_from_radius(radius):
	return 4*math.pi*(radius**2) 

#how much gas is there in a column above 1sq meter of land?
def mass_of_gas_in_1sqm(radius, mass_of_gas):
	surface_area = compute_surface_area_from_radius(radius)
	mass_in_1sqm = float(mass_of_gas)/surface_area
	return mass_in_1sqm

#how many atoms are there in a column above 1sq m of land?
def atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass):
	mass_in_1sqm = mass_of_gas_in_1sqm(radius, mass_of_gas)
	number_of_moles = float(mass_in_1sqm)/molecular_mass
	number_of_atoms = number_of_moles*Avagadro
	return number_of_atoms

#what percentage of the light should make it through?
def attenuation_parameter(fudge_factor, radius, mass_of_gas, molecular_mass, molecular_area):
	number_of_atoms = atoms_of_gas_in_1sqm(radius, mass_of_gas, molecular_mass)
	exponent = -fudge_factor*number_of_atoms*molecular_area
	return math.exp(exponent)

#compute how the light is filtered through the atmosphere, values from http://irina.eas.gatech.edu/EAS8803_Fall2009/Lec6.pdf
def compute_light_filter(atmosphere, mass_of_atmosphere, planetary_radius):
	result = []
	for i in range(dimension_of_sample):
		result.append(1)
	#what percentage of light to block for different compounds?
	#this value is the base and on earth, for all of them, it should be 0.5
	#this base value is then, as below, multiplied by a scaling factor based on wavelength
	Water = attenuation_parameter(fudge_factor_water, planetary_radius, atmosphere["Water"],
					molecular_mass_water, diameter_water**2)
	Nitrogen = attenuation_parameter(fudge_factor_nitrogen, planetary_radius, atmosphere["Nitrogen"],
					molecular_mass_nitrogen, diameter_nitrogen**2)
	Oxygen = attenuation_parameter(fudge_factor_oxygen, planetary_radius, atmosphere["Oxygen"],
					molecular_mass_oxygen, diameter_oxygen**2) 
	Carbon_Dioxide = attenuation_parameter(fudge_factor_carbon_dioxide, planetary_radius, atmosphere["Carbon Dioxide"],
					molecular_mass_carbon_dioxide, diameter_carbon_dioxide**2)
	print "WNOC =", Water, Nitrogen, Oxygen, Carbon_Dioxide
	#which frequencies to filter. result[i] = i*0.05 microns (micrometers)
	free = max([Water, Nitrogen, Oxygen, Carbon_Dioxide])
	result[1] *= (Nitrogen**0.3)*(Oxygen**2.2)*Water
	result[2] *= (Nitrogen**0.3)*(Oxygen**2.2)*Water
	result[3] *= (Oxygen**2.2)*(Water**2.2)
	result[4] *= (Oxygen**2.2)*(Water**2.2)
	result[5] *= (Oxygen**2.2)
	result[6] *= (Oxygen**2.2)
	result[7] *= (Oxygen**2.2)
	result[8] *= Oxygen**1.7
	result[9] *= Oxygen**1.7
	result[10] *= Oxygen**1.7
	result[11] *= Oxygen**1.7
	result[12] *= (Oxygen**1.7)*(Water**2.2)
	result[13] *= (Oxygen**1.7)*(Water**2.2)
	result[14] *= (Water**2.2)*(Oxygen**1.7)
	result[15] *= (Oxygen**1.7)
	result[16] *= (Water**2.2)*1*Oxygen
	result[17] *= (Oxygen**1.7)
	result[18] *= free
	result[19] *= (Water**2.2)
	result[20] *= free
	result[21] *= (Oxygen**2.2)
	result[22] *= (Water**2.2)
	result[23] *= free
	result[24] *= free
	result[25] *= (Oxygen**2.2)
	result[26] *= free
	result[27] *= 1*Water
	result[28] *= Carbon_Dioxide**0.75
	result[29] *= free
	result[30] *= Carbon_Dioxide**2.3
	result[31] *= free
	result[32] *= (Oxygen**2.2)
	result[33] *= free
	result[34] *= free
	result[35] *= free
	result[36] *= free
	result[37] *= 1*Water
	result[38] *= free
	result[39] *= free
	result[40] *= 1*Carbon_Dioxide
	result[41] *= free
	result[42] *= free
	result[43] *= free
	result[44] *= free
	result[45] *= free
	result[46] *= free	
	result[47] *= free
	result[48] *= (Water**0.1)
	result[49] *= (Water**0.1)
	return result

#combine two light spectra (just multiply the elements)
def combine(spectrum1, spectrum2):
	result = []
	for i in range(len(spectrum1)):
		result.append(spectrum1[i]*spectrum2[i])
	return result

#compute the temperature change (dT/dt)
def compute_temp_change(incoming_sunlight, carbon_dioxide, oxygen, water_vapour, albedo, temperature):
	return ((1 - albedo)*(1 - oxygen*oxygen_param)*incoming_sunlight 
		- (1 - water_vapour*water_vapour_param)*
		(1 - carbon_dioxide*carbon_dioxide_param)*Stephan*temperature**4)

#compute the amount of sunlight that lands on the planet per m^2
def compute_incoming_sunlight(stellar_luminosity, radius_of_orbit):
	return stellar_luminosity/(4*math.pi*(radius_of_orbit**2))

#compute the warming effect from water vapour in the atmosphere
def compute_water_vapour(temperature):
	if temperature < 273:
		return 0
	if temperature > 373:
		return 1
	else:
		return (temperature - 273)/100

#compute the albedo (reflectiveness) of the planet based on temperature
def compute_albedo(temperature):
	if temperature < 273:
		return 0.7
	if temperature > 373:
		return 0.6
	else:
		return 0.7 - (0.1*(temperature - 273)/100)

#compute the temerature by running the ODE to an equilibrium
def compute_temperature(incoming_sunlight, carbon_dioxide, oxygen):
	temp = 200
	for l in range(1000):
		water_vapour = compute_water_vapour(temp)
		albedo = compute_albedo(temp)
		temp += compute_temp_change(incoming_sunlight, carbon_dioxide, oxygen, water_vapour, albedo, temp)*small_delta
	return temp

#compute the habitable zone for the planet to be in
def compute_temperate_zone(luminosity, min_orbital_diameter, max_orbital_diameter):
	print "Habitable zone calc completion percentage : ",
	#storing the values of how habitable that position is
	scores = [[0,0] for j in range(number_of_tests)]

	#step through the radii
	radius_step = float(max_orbital_diameter)/number_of_tests
	counter = 0
	for i in range(int(min_orbital_diameter), int(max_orbital_diameter), int(radius_step)):
		#record the radial diameter, meters
		scores[counter][0] = i
		#compute how much sunlight reachers the planet per sq meter
		incoming_sunlight = compute_incoming_sunlight(luminosity, i)
		#test "detail" different values of carbon dioxide
		for j in range(detail):
			carbon_dioxide = (float(1)/detail)*j
			#test 10 different values of oxygen
			for k in range(detail):
				oxygen = (float(1)/detail)*k
				temp = compute_temperature(incoming_sunlight, carbon_dioxide, oxygen)
				if temp < 373 and temp > 273:
					scores[counter][1] += 1

		counter += 1
		print counter,

	return scores

#class for the planet
class planet:
	def __init__(self, orbital_radius, parent_star):
		#inherit orbital radius and parent
		self.orbital_radius = orbital_radius[0]
		self.parent_star = parent_star
		#compute the planets radius and from it derive the mass
		if Earth:
			self.radius = Radius_of_the_earth
		else:
			self.radius = random.randint(minimum_planet_radius, maximum_planet_radius)
		self.mass = density_of_earth*4*math.pi*(self.radius**3)/3
		#compute the planets orbital period using Kepler's law https://en.wikipedia.org/wiki/Orbital_period
		self.orbital_period = 2*math.pi*math.sqrt((self.orbital_radius**3)/self.parent_star.gravitational_parameter)
		#create 3 bins, atmosphere, ocean and lithosphere
		self.atmosphere = {}
		self.ocean = {}
		self.lithosphere = {}
		for compound in compounds:
			self.atmosphere[str(compound)] = 0
			self.ocean[str(compound)] = 0
			self.lithosphere[str(compound)] = 0
		#decide the mass of the atmosphere
		self.atmosphere_mass = self.mass*percentage_atmopshere #kg
		self.ocean_mass = self.mass*percentage_ocean #kg
		self.lithosphere_mass = self.mass*percentage_lithosphere # kg, just a guess in line with the values for ocean and atm
		#use percentages to set the constituents of the atmosphere, ocean and lithosphere
		self.atmosphere["Nitrogen"] = self.atmosphere_mass*0.72
		self.atmosphere["Carbon Dioxide"] = self.atmosphere_mass*0.04
		self.atmosphere["Oxygen"] = self.atmosphere_mass*0.2
		self.atmosphere["Water"] = self.atmosphere_mass*0.04
		self.ocean["Water"] = self.ocean_mass*0.8
		self.ocean["Nitrogen"] = self.ocean_mass*0.2
		self.ocean["Carbon Dioxide"] = self.ocean_mass*0.1
		self.ocean["Phosphates"] = self.ocean_mass*0.1
		self.lithosphere["Hydrogen Sulfide"] = self.lithosphere_mass*0.5
		self.lithosphere["Carbon Dioxide"] = self.lithosphere_mass*0.5
		#use the atmospheric composition to compute the light filtering
		self.light_filter = compute_light_filter(self.atmosphere, self.atmosphere_mass, self.radius)
		#compute the light on the surface
		self.light_on_surface = combine(self.light_filter, self.parent_star.spectrum)

		print " "
		print "Created new planet."
		print "Orbital radius = ", '%.2e' % self.orbital_radius, " meters."
		print "Radius = ", '%.2e' % self.radius, " meters."
		print "Mass = ",'%.2e' % self.mass, " kg."
		print "Orbital period = ", '%.2e' % self.orbital_period, " seconds = ", self.orbital_period/3.154e+7, " earth years = 1 year for this planet."
		print "Atmosphere = ", self.atmosphere
		print "Ocean = ", self.ocean
		print "Lithosphere = ", self.lithosphere
		print "Spectrum on the surface = ", self.light_on_surface

#class for the star
class star:
	def __init__(self):
		#Measured in multiples of the the sun's mass
		if Earth:
			self.mass = 1
		else:
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
		#compute the inner and outer edge of the possible habitable zone
		self.min_orbital_diameter = self.mass*base_min_orbital_diameter
		self.max_orbital_diameter = self.mass*base_max_orbital_diameter
		#compute the habitable zone
		self.habitable_zone = compute_temperate_zone(self.luminosity, self.min_orbital_diameter, self.max_orbital_diameter)
		#put the planet in the habitable zone
		self.planet_orbital_radius = max(self.habitable_zone, key=lambda x:x[1])
		#calculate the gravitational parameter = GM = Gravitational_Constant*Mass
		self.gravitational_parameter = Gravitational_Constant*self.mass*Mass_of_our_sun

		print " "
		print "Created new main sequence star"
		print "Mass = ", self.mass, " solar masses."
		print "Life Span = ", '%.2e' % self.life_span, " of our years."
		print "Luminosity = ", '%.2e' % self.luminosity, " watts."
		print "Radius = ", '%.2e' % self.radius, " meters."
		print "Temperature = ", self.temperature, " Kelvin."
		print "Stellar spectrum = ", self.spectrum
		print "Habitable zone = ", self.habitable_zone

		#make the planet
		self.planet = planet(self.planet_orbital_radius, self)




our_star = star()
