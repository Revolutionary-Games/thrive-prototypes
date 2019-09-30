#include <iostream>
#include <math.h>
#include <random>
#include <stdio.h>
#include <time.h>


static double const GravitationalConstant = 6.674e-11; // Newtons Meters^2 / kg^2
static double const LuminosityOfOurSun = 3.846e26; //watts


class Star{

    public:
    //star properties
    double StarMass;
    double LifeSpan;

    Star(){
        generateProperties(0);
    }

    void setSol(){  
        StarMass = 1; //solar masses 
        generateProperties(2);
    }

    void setMass(double mass){  
        StarMass = mass;
        generateProperties(2);
    }

    //set all the properties of the star starting only with the step given
    void generateProperties(int step){
        if (step <= 0){
            //make a random choice about if this star is sol or not
        }
        if (step <= 1){
            //randomly choose the mass of the star
        }
        if (step <= 2){
            //compute the other variables like lifespan, luminosity etc
        }
    }

    void print(){
        
        //these would all be replaced with log info's
        std::cout << "Star Mass: " << StarMass << std::endl;
        std::cout << "LifeSpan: " << LifeSpan << std::endl;
    }

};

class Planet{

    public:
    //planet properties
    double OrbitalRadius;
    double PlanetRadius;

    void print(){
        
        //these would all be replaced with log info's
        std::cout << "OrbitalRadius: " << OrbitalRadius << std::endl;
        std::cout << "PlanetRadius: " << PlanetRadius << std::endl;
    }

};



int main(){

    Star star;
    star.print();
    star.setSol();
    star.print();
    Planet planet;
    planet.print();
    return 0;
}
