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


// ------------------------------------ //
// Utility Functions
// ------------------------------------ //

//generate a random real number between two bounds
double fRand(double fMin, double fMax)
{
    srand(time(NULL));
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}
//multiply two spectra together to get a 3rd
void multiplyArrays(double* Array1, double* Array2, double* target){
    for (int i = 0; i < LENGTH_OF_ARRAYS; i++){
        target[i] = Array1[i]*Array2[i];
    }
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
    }
}

void Star::print()
{        
    //these would all be replaced with log info's
    std::cout << "The Star.\n";
    std::cout << "Star Mass = " << starMass << " Solar Masses.\n";
    std::cout << "Life Span = " << lifeSpan << " of our years.\n";
    std::cout << "Luminosity = " << luminosity << " watts.\n";
    std::cout << "Radius = " << radius << " meters.\n";
    std::cout << "Temperature = " << temperature << " Kelvin.\n";
    std::cout << "\n";
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
