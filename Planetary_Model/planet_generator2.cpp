#include "planet_generator2.h"

#include <iostream>
#include <math.h>
#include <random>
#include <stdio.h>
#include <time.h>

// ------------------------------------ //
// Constants
// ------------------------------------ //


constexpr double GRAVITATIONAL_CONSTANT = 6.674e-11; // Newtons Meters^2 / kg^2
constexpr double LUMINOSITY_OF_OUR_SUN = 3.846e26; //watts
constexpr double MASS_OF_OUR_SUN = 1.989e30; //kg
constexpr double RADIUS_OF_OUR_SUN = 6.96e8; //meters
constexpr double RADIUS_OF_THE_EARTH = 6.371e6; //meters
constexpr double STEPHAN = 5.67e-8; // Watts meters^-2 Kelvin^-4 constant
constexpr double PI = 3.14159265358979323846;
constexpr double HC = 1.98e-25; //planks constant time speed of light
constexpr double HC2 = 5.95e-17; //planks constant times speed of light squared
constexpr double KB = 1.38e-23; //Boltzmanns constant
constexpr double WAVELENGTH_STEP = 5e-8; // 0.05 microns per step, there are 50 steps so this is 2.5 microns.
constexpr double E = 2.71828182845904523536; // you all know and love it!
//visible spectrum for humans is 0.38 - 0.75 microns
constexpr double SMALL_DELTA = 0.01; //step size for the climate differential equation
constexpr double ALBEDO = 0.65; //base albedo value (planetary reflectivity)
constexpr double BASE_MAX_ORBITAL_DIAMETER = 7.78e11; // meters (radius of jupiter)
constexpr double BASE_MIN_ORBITAL_DIAMETER = 5.5e10; // meters (radius of mercury)
constexpr double OXYGEN_PARAMETER = 0.3; // amount of sunlght ozone can block if atmosphere is 100 oxgen
constexpr double CARBON_DIOXIODE_PARAMETER = 0.3; // same
constexpr double WATER_VAPOUR_PARAMETER = 0.3; //same
constexpr double NUMBER_OF_GAS_CHECKS = 10; //number of different values of CO2 and O2 to check, more is better but very intensive
constexpr double MIN_PLANET_RADIUS = 5375699.0; // smallest radius allowed, see http://forum.revolutionarygamesstudio.com/t/planet-generation/182/10
constexpr double MAX_PLANET_RADIUS = 9191080.0; // largest radius allowed
constexpr double DENSITY_OF_EARTH = 5515.3; // kg m^-3 assume all planets are the same density as earth
constexpr double PERCENTAGE_ATMOSPHERE = 8.62357669e-7; // percentage of the earths mass which is atmosphere
constexpr double PERCENTAGE_OCEAN = 2.26054923e-7; // percentage that is ocean
constexpr double PERCENTAGE_LITHOSPHERE = 1.67448091e-7; // percentage that is rock, just a guess in line with others
constexpr double FUDGE_FACTOR_NITROGEN = 7.28704114055e-10; // calibrate the spectral computations using earths atmosphere
constexpr double FUDGE_FACTOR_WATER = 6.34362956432e-09; // same
constexpr double FUDGE_FACTOR_CARBON_DIOXIDE = 1.55066500461e-08; // same
constexpr double FUDGE_FACTOR_OXYGEN = 3.42834549545e-09; // same
constexpr double AVOGADRO = 6.022e23; // avagadros constant relating number of atoms to mass
constexpr double MOLECULAR_MASS_CARBON_DIOXIDE = 0.044; // kg mol^-1, mass of 1 mole of CO2
constexpr double MOLECULAR_MASS_OXYGEN = 0.032; //  kg mol^-1, mass of 1 mole of O2
constexpr double MOLECULAR_MASS_NITROGEN = 0.028; //  kg mol^-1, mass of 1 mole of N2
constexpr double MOLECULAR_MASS_WATER = 0.018; //  kg mol^-1, mass of 1 mole of H2O
constexpr double DIAMETER_WATER = 9.0e-11; // meters, size of a water molecule for interaction with light
constexpr double DIAMETER_NITROGEN = 7.5e-11; //  meters
constexpr double DIAMETER_CARBON_DIOXIDE = 9e-11; // meters
constexpr double DIAMETER_OXYGEN = 7.3e-11; // meters

// ------------------------------------ //
// Utility Functions
// ------------------------------------ //

//4 functions for computing the temperature based on sunlight, CO2 and O2
//work out how reflective the planet is
float computeAlbedo(float temperature){
    if (temperature < 273){
        return 0.7;
    }
    if (temperature > 373){
        return 0.6;
    }
    else{
        return 0.7 - (0.1*(temperature - 273)/100);
    }
}

//compute the warming effect from water vapour in the atmosphere
float computeWaterVapour(float temperature){
	if (temperature < 273){
		return 0;
	}
	if (temperature > 373){
		return 1;
	}
	else{
		return (temperature - 273)/100;
	}
}

//compute the temperature change (dT/dt)
float computeTempChange(double incomingSunlight, float carbonDioxide,
                          float oxygen, float waterVapour, float albedo, float temperature){
	return ((1 - albedo)*(1 - oxygen*OXYGEN_PARAMETER)*incomingSunlight
        - (1 - waterVapour*WATER_VAPOUR_PARAMETER)*
        (1 - carbonDioxide*CARBON_DIOXIODE_PARAMETER)*STEPHAN*pow(temperature,4));
}

//compute the temerature by running the ODE to an equilibrium
float computeTemperature(double incomingSunlight, float carbonDioxide,float oxygen){
	float temperature = 200.0;
	for (int i = 0; i < 1000; i++){
		float waterVapour = computeWaterVapour(temperature);
		float albedo = computeAlbedo(temperature);
		temperature += computeTempChange(incomingSunlight, carbonDioxide, oxygen, waterVapour, albedo, temperature)*SMALL_DELTA;
	}
	return temperature;
}

//generate a random real number between two bounds
double fRand(double fMin, double fMax)
{
    std::random_device random_device;
    std::mt19937 random_engine(random_device());
    std::uniform_real_distribution<double> distribution(fMin, fMax);
    return distribution(random_engine);
}

//multiply two spectra together to get a 3rd
void multiplyArrays(const std::array<double, LENGTH_OF_ARRAYS>& Array1, const std::array<double, LENGTH_OF_ARRAYS>& Array2, std::array<double, LENGTH_OF_ARRAYS>& target){
    for (int i = 0; i < LENGTH_OF_ARRAYS; i++){
        target[i] = Array1[i]*Array2[i];
    }
}

double planksLaw(int temperature, double wavelength){
    double partial = pow(E,(HC/(wavelength*KB*temperature))) - 1;
    return 2*HC2/(partial*(pow(wavelength,5)));
}

void printSpectrum(const std::array<double, LENGTH_OF_ARRAYS>& Array1){
    std::cout << "Wavelength meters : Energy Watts \n";
    for (int i = 0; i < LENGTH_OF_ARRAYS; i++){
        std::cout << WAVELENGTH_STEP*(i + 1) << ": " <<  Array1[i] << "\n";
    }
    std::cout << "\n";
}


// ------------------------------------ //
// Star
// ------------------------------------ //

void Star::generateProperties(int step)
{
    if (step <= 0){
        //randomly choose the mass of the star
        starMass = fRand(0.5,3); // solar masses
    }
    if (step <= 1){
        //compute the other variables like lifespan, luminosity etc
        setLifeSpan();
        setLuminosity();
        setRadius();
        setTemperature();
        setStellarSpectrum();
        minOrbitalDiameter = starMass*BASE_MIN_ORBITAL_DIAMETER;
        maxOrbitalDiameter = starMass*BASE_MAX_ORBITAL_DIAMETER;
        computeHabitableZone();
        gravitationalParameter = GRAVITATIONAL_CONSTANT*starMass*MASS_OF_OUR_SUN;
    }
}

void Star::print()
{        
    if (PRINT)
    {
        //these would all be replaced with log info's
        std::cout << "The Star.\n";
        std::cout << "Star Mass = " << starMass << " Solar Masses.\n";
        std::cout << "Life Span = " << lifeSpan << " of our years.\n";
        std::cout << "Luminosity = " << luminosity << " watts.\n";
        std::cout << "Radius = " << radius << " meters.\n";
        std::cout << "Temperature = " << temperature << " Kelvin.\n";
        std::cout << "\n";

        if (PRINT_VERBOSE)
        {
            std::cout << "Stellar Spectrum. \n";  
            printSpectrum(stellarSpectrum);
            std::cout << "Habitability Scores in form Radius(m): Habitability Score. \n";
            for (int i = 0; i < NUMBER_OF_TESTS; i++){
                std::cout << orbitalDistances[i] << " : " << habitabilityScore[i] << "\n";
            }
        }
    }
}

//from wikipedia table https://en.wikipedia.org/wiki/File:Representative_lifetimes_of_stars_as_a_function_of_their_masses.svg
void Star::setLifeSpan()
{
    lifeSpan = 1e10/(pow(starMass,3));
}

//from wikipedia https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
void Star::setLuminosity()
{
    luminosity = LUMINOSITY_OF_OUR_SUN*(pow(starMass,3.5));
}

//from (7.14c) of http://physics.ucsd.edu/students/courses/winter2008/managed/physics223/documents/Lecture7%13Part3.pdf
void Star::setRadius()
{
    radius =  RADIUS_OF_OUR_SUN*(pow(starMass,0.9));
}

//from the same page as luminosity using the formula for temperature and luminosity
void Star::setTemperature()
{
    temperature = pow((luminosity/(4*PI*STEPHAN*(pow(radius,2)))),0.25);
}

void Star::setStellarSpectrum(){
    for (int i = 0; i < LENGTH_OF_ARRAYS; i++){
        stellarSpectrum[i] = planksLaw(temperature , WAVELENGTH_STEP*(i + 1));
    }
}

//compute how habitable a planet would be at different radii
void Star::computeHabitableZone(){
    double diameterStep = (maxOrbitalDiameter - minOrbitalDiameter) / NUMBER_OF_TESTS;
    int counter = 0;
    //start at a close distance
    double currentDiameter = minOrbitalDiameter;
    while (currentDiameter < maxOrbitalDiameter ){
        habitabilityScore[counter] = 0;
        //work out incoming sunlight
        double incomingSunlight = luminosity/(4*PI*(pow(currentDiameter,2)));
        //test different values of CO2 and O2 in the atmosphere
        for (int i = 0; i <= NUMBER_OF_GAS_CHECKS; i++){
            float carbonDioxide = i*((float)1 / (float)NUMBER_OF_GAS_CHECKS);
            for (int j = 0; j <= NUMBER_OF_GAS_CHECKS; j++){
                float oxygen = j*((float)1 / (float)NUMBER_OF_GAS_CHECKS);
                float temp = computeTemperature(incomingSunlight, carbonDioxide, oxygen);
                if (temp < 373 && temp > 273)
                {
                    habitabilityScore[counter]++;
                }
            }
        }
        orbitalDistances[counter] = currentDiameter;
        //increase the distance
        counter++;
        currentDiameter += diameterStep;
    }
    habitabilityScore[0] = 0; //fixing a weird bug I found, sorry :(

}

void Star::update()
{
    starMass++;
}

// ------------------------------------ //
// Planet
// ------------------------------------ //

void Planet::print()
{
        
    //these would all be replaced with log info's
    std::cout << "Info about the current planet." << std::endl;
    std::cout << "Orbiting star with mass: " << orbitingStar->starMass << std::endl;   
    std::cout << "OrbitalRadius: " << orbitalRadius << std::endl;
    std::cout << "PlanetRadius: " << planetRadius << std::endl;
}

void Planet::update()
{
    orbitalRadius++;
}



int main(){

    Star star;
    Planet planet(&star);
    star.print();
    planet.print();
    star.setSol();
    star.print();
    star.update();
    star.print();
    planet.update();
    planet.print();
    return 0;
}
