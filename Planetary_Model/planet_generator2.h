#pragma once

#include <array>

#define LENGTH_OF_ARRAYS 50
#define NUMBER_OF_TESTS 100 // number of different planetary locations to test
#define PRINT true //should you print the results of the computations?
#define PRINT_VERBOSE true //should you print extra lines of info?

class Star{// : public Leviathan::PerWorldData{

public:
    //star properties
    double starMass;
    double lifeSpan;
    double luminosity;
    double radius;
    double temperature;
    std::array<double, LENGTH_OF_ARRAYS> stellarSpectrum;
    double minOrbitalDiameter;
    double maxOrbitalDiameter;
    std::array<double, NUMBER_OF_TESTS> orbitalDistances;
    std::array<double, NUMBER_OF_TESTS> habitabilityScore;
    double gravitationalParameter;

    Star()
    {
        generateProperties(0);
    }

    void setSol()
    {  
        starMass = 1.0; //solar masses 
        generateProperties(1);
    }

    void setMass(double mass)
    {  
        starMass = mass;
        generateProperties(1);
    }

    //! print the properties of the star
    void print();

    //! update the star each turn
    void update();

private:
    //! set all the properties of the star, if step == 0 mass will be randomised, if step == 1 it will not be
    void generateProperties(int step);

    void setLifeSpan();
    void setLuminosity();
    void setRadius();
    void setTemperature();
    void setStellarSpectrum();
    void computeHabitableZone();

};

class Planet{// : public Leviathan::PerWorldData{

public:
    //planet properties
    Star* orbitingStar;
    double orbitalRadius;
    double planetRadius;

    Planet(Star* star)
    {
        orbitingStar = star;
    }

    void print();

    void update();

};
