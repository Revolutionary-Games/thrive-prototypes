#include <iostream>
#include <math.h>
#include <random>
#include <stdio.h>
#include <time.h>

bool const ExtraDetail = true; //print light spectra and habitable zone calcs

//in this program 0 = randomly generate an answer, 1 = False and 2 = True

//list of constants
double const GravitationalConstant = 6.674e-11; // Newtons Meters^2 / kg^2
double const LuminosityOfOurSun = 3.846e26; //watts
double const MassOfOurSun = 1.989e30; //kg
double const RadiusOfOurSun = 6.96e8; //meters
double const RadiusOfTheEarth = 6.371e6; //meters
double const Stephan = 5.67e-8; // Watts meters^-2 Kelvin^-4 constant
int const LengthOfArrays = 50;
double const hc = 1.98e-25; //planks constant time speed of light
double const hc2 = 5.95e-17; //planks constant times speed of light squared
double const kB = 1.38e-23; //Boltzmanns constant
double const WavelengthStep = 5e-8; // 0.05 microns per step, there are 50 steps so this is 2.5 microns.
double const e = 2.71828182845904523536; // you all know and love it!
double const pi = 3.14159265358979323846;
//visible spectrum for humans is 0.38 - 0.75 microns
double const SmallDelta = 0.01; //step size for the climate differential equation
double const Albedo = 0.65; //base albedo value (planetary reflectivity)
double const BaseMaxOrbitalDiameter = 7.78e11; // meters (radius of jupiter)
double const BaseMinOrbitalDiameter = 5.5e10; // meters (radius of mercury)
int const NumberOfTests = 100; // number of different planetary locations to test
double const OxygenParam = 0.3; // amount of sunlght ozone can block if atmosphere is 100 oxgen
double const CarbonDioxideParam = 0.3; // same
double const WaterVapourParam = 0.3; //same
int const Detail = 10; //number of different values of CO2 and O2 to check, more is better but very intensive
double const MinimumPlanetRadius = 5375699; // smallest radius allowed, see http://forum.revolutionarygamesstudio.com/t/planet-generation/182/10
double const MaximumPlanetRadius = 9191080; // largest radius allowed
double const DensityOfEarth = 5515.3; // kg m^-3 assume all planets are the same density as earth
double const PercentageAtmopshere = 8.62357669e-7; // percentage of the earths mass which is atmosphere
double const PercentageOcean = 2.26054923e-7; // percentage that is ocean
double const PercentageLithosphere = 1.67448091e-7; // percentage that is rock, just a guess in line with others
double const FudgeFactorNitrogen = 7.28704114055e-10; // calibrate the spectral computations using earths atmosphere
double const FudgeFactorWater = 6.34362956432e-09; // same
double const FudgeFactorCarbonDioxide = 1.55066500461e-08; // same
double const FudgeFactorOxygen = 3.42834549545e-09; // same
double const Avagadro = 6.022e23; // avagadros constant relating number of atoms to mass
double const MolecularMassCarbonDioxide = 0.044; // kg mol^-1, mass of 1 mole of CO2
double const MolecularMassOxygen = 0.032; //  kg mol^-1, mass of 1 mole of O2
double const MolecularMassNitrogen = 0.028; //  kg mol^-1, mass of 1 mole of N2
double const MolecularMassWater = 0.018; //  kg mol^-1, mass of 1 mole of H2O
double const DiameterWater = 9.0e-11; // meters, size of a water molecule for interaction with light
double const DiameterNitrogen = 7.5e-11; //  meters
double const DiameterCarbonDioxide = 9e-11; // meters
double const DiameterOxygen = 7.3e-11; // meters


//struct to hold computed variables
struct System{
    System() : Earth(0), StarMass(0), OrbitalRadius(0), PlanetRadius(0), AtmosphereWater(0) {}
    //these values are the ones the player can interact with.
    int Earth;
    //star properties
    double StarMass;
    double LifeSpan;
    double Luminosity;
    double Radius;
    double Temperature;
    double StellarSpectrum[LengthOfArrays];
    double MinOrbitalDiameter;
    double MaxOrbitalDiameter;
    double OrbitalDistances[NumberOfTests];
    double HabitabilityScore[NumberOfTests];
    double GravitationalParameter;
    //planet properties
    double OrbitalRadius;
    double PlanetRadius;
    double PlanetMass;
    double PlanetOrbitalPeriod;
    double LithosphereMass;
    double AtmosphereMass;
    double OceanMass;
    double AtmosphereWater;
    double AtmosphereCarbonDioxide;
    double AtmosphereOxygen;
    double AtmosphereNitrogen;
    double AtmosphericFilter[LengthOfArrays];
    double TerrestrialSpectrum[LengthOfArrays];
    double PlanetTemperature;
};
//generate a random real number between two bounds
double fRand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}
//multiply two spectra together to get a 3rd
void multiply(double* Array1, double* Array2, double* target){
    for (int i = 0; i < LengthOfArrays; i++){
        target[i] = Array1[i]*Array2[i];
    }
}

double PlanksLaw(int temperature, double wavelength){
    double partial = pow(e,(hc/(wavelength*kB*temperature))) - 1;
    return 2*hc2/(partial*(pow(wavelength,5)));
}

void GenerateStellarSpectrum(System &GeneratedSystem){
    for (int i = 0; i < LengthOfArrays; i++){
        GeneratedSystem.StellarSpectrum[i] = PlanksLaw(GeneratedSystem.Temperature , WavelengthStep*(i + 1));
    }
}

void PrintSpectrum(double* Array1){
    std::cout << "Wavelength meters : Energy Watts \n";
    for (int i = 0; i < LengthOfArrays; i++){
        std::cout << WavelengthStep*(i + 1) << ": " <<  Array1[i] << "\n";
    }
    std::cout << "\n";
}

//from wikipedia table https://en.wikipedia.org/wiki/File:Representative_lifetimes_of_stars_as_a_function_of_their_masses.svg
void SetLifeSpan(System &GeneratedSystem){
    GeneratedSystem.LifeSpan = 1e10/(pow(GeneratedSystem.StarMass,3));
}

//from wikipedia https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
void SetLuminosity(System &GeneratedSystem){
    GeneratedSystem.Luminosity = LuminosityOfOurSun*(pow(GeneratedSystem.StarMass,3.5));
}

//from (7.14c) of http://physics.ucsd.edu/students/courses/winter2008/managed/physics223/documents/Lecture7%13Part3.pdf
void SetRadius(System &GeneratedSystem){
    GeneratedSystem.Radius =  RadiusOfOurSun*(pow(GeneratedSystem.StarMass,0.9));
}

//from the same page as luminosity using the formula for temperature and luminosity
void SetTemperature(System &GeneratedSystem){
    GeneratedSystem.Temperature =  pow((GeneratedSystem.Luminosity/(4*pi*Stephan*(pow(GeneratedSystem.Radius,2)))),0.25);
}

void SetPlanetMass(System &GeneratedSystem){
    GeneratedSystem.PlanetMass = DensityOfEarth*4*pi*(pow(GeneratedSystem.PlanetRadius,3))/3;
}

//compute the planets orbital period using Kepler's law https://en.wikipedia.org/wiki/Orbital_period
void SetPlanetPeriod(System &GeneratedSystem){
    GeneratedSystem.PlanetOrbitalPeriod = 2*pi*pow(((pow(GeneratedSystem.OrbitalRadius,3))/GeneratedSystem.GravitationalParameter),0.5);
}

void SetoSphereMasses(System &GeneratedSystem){
    GeneratedSystem.AtmosphereMass = GeneratedSystem.PlanetMass*PercentageAtmopshere;
    GeneratedSystem.OceanMass = GeneratedSystem.PlanetMass*PercentageOcean;
    GeneratedSystem.LithosphereMass = GeneratedSystem.PlanetMass*PercentageLithosphere;

}

//choose what gasses to have in your atmosphere. This function is horrible with the copy pasta :(
void SetAtmosphereConstituents(System &GeneratedSystem){
    if (GeneratedSystem.Earth == 1){ //not the earth
        double CurrentPercentage = fRand(0,0.9);
        GeneratedSystem.AtmosphereOxygen = GeneratedSystem.AtmosphereMass*CurrentPercentage;
        double NewRange = 1 - CurrentPercentage;
        CurrentPercentage = fRand(0,NewRange);
        GeneratedSystem.AtmosphereWater = GeneratedSystem.AtmosphereMass*CurrentPercentage;
        NewRange = NewRange - CurrentPercentage;
        CurrentPercentage = fRand(0,NewRange);
        GeneratedSystem.AtmosphereCarbonDioxide = GeneratedSystem.AtmosphereMass*CurrentPercentage;
        NewRange = NewRange - CurrentPercentage;
        GeneratedSystem.AtmosphereNitrogen = GeneratedSystem.AtmosphereMass*NewRange;
    }
    else { //is the earth
        GeneratedSystem.AtmosphereOxygen = GeneratedSystem.AtmosphereMass*0.2;
        GeneratedSystem.AtmosphereWater = GeneratedSystem.AtmosphereMass*0.04;
        GeneratedSystem.AtmosphereCarbonDioxide = GeneratedSystem.AtmosphereMass*0.04;
        GeneratedSystem.AtmosphereNitrogen = GeneratedSystem.AtmosphereMass*0.72;
    }


}

//functions for computing the temperature based on sunlight, CO2 and O2
//work out how reflective the planet is
float ComputeAlbedo(float Temperature){
    if (Temperature < 273){
        return 0.7;
    }
    if (Temperature > 373){
        return 0.6;
    }
    else{
        return 0.7 - (0.1*(Temperature - 273)/100);
    }
}

//compute the warming effect from water vapour in the atmosphere
float ComputeWaterVapour(float Temperature){
	if (Temperature < 273){
		return 0;
	}
	if (Temperature > 373){
		return 1;
	}
	else{
		return (Temperature - 273)/100;
	}
}

//compute the temperature change (dT/dt)
float ComputeTempChange(double IncomingSunlight, float CarbonDioxide,
                          float Oxygen, float WaterVapour, float Albedo, float Temperature){
	return ((1 - Albedo)*(1 - Oxygen*OxygenParam)*IncomingSunlight
		- (1 - WaterVapour*WaterVapourParam)*
		(1 - CarbonDioxide*CarbonDioxideParam)*Stephan*pow(Temperature,4));
}

//compute the temerature by running the ODE to an equilibrium
float ComputeTemperature(double IncomingSunlight, float CarbonDioxide,float Oxygen){
	float Temperature = 200;
	for (int i = 0; i < 1000; i++){
		float WaterVapour = ComputeWaterVapour(Temperature);
		float Albedo = ComputeAlbedo(Temperature);
		Temperature += ComputeTempChange(IncomingSunlight, CarbonDioxide,
                                   Oxygen, WaterVapour, Albedo, Temperature)*SmallDelta;
	}
	return Temperature;
}

//compute how habitable a planet would be at different radii
void ComputeHabitableZone(System &GeneratedSystem){
    double DiameterStep = (GeneratedSystem.MaxOrbitalDiameter - GeneratedSystem.MinOrbitalDiameter) / NumberOfTests;
    int Counter = 0;
    //start at a close distance
    double CurrentDiameter = GeneratedSystem.MinOrbitalDiameter;
    while (CurrentDiameter < GeneratedSystem.MaxOrbitalDiameter ){
        GeneratedSystem.HabitabilityScore[Counter] = 0;
        //work out incoming sunlight
        double IncomingSunlight = GeneratedSystem.Luminosity/(4*pi*(pow(CurrentDiameter,2)));
        //test different values of CO2 and O2 in the atmosphere
        for (int i = 0; i <= Detail; i++){
            float CarbonDioxide = i*((float)1 / (float)Detail);
                    for (int j = 0; j <= Detail; j++){
                    float Oxygen = j*((float)1 / (float)Detail);
                    float Temperature = ComputeTemperature(IncomingSunlight, CarbonDioxide, Oxygen);
                    if (Temperature < 373 && Temperature > 273){
                        GeneratedSystem.HabitabilityScore[Counter]++;
                    }
                    }
        }
        GeneratedSystem.OrbitalDistances[Counter] = CurrentDiameter;
        //increase the distance
        Counter++;
        CurrentDiameter += DiameterStep;
    }
    GeneratedSystem.HabitabilityScore[0] = 0; //fixing a weird bug I found, sorry :(

}

//put the planet in the optimal place in the system
void ComputeOrbitalRadius(System &GeneratedSystem){
    int MaxHabitability = 0;
    int EntryLocation = 0;
    for (int i = 0; i < NumberOfTests; i++){
            if (GeneratedSystem.HabitabilityScore[i] > MaxHabitability){
                MaxHabitability = GeneratedSystem.HabitabilityScore[i];
                EntryLocation = i;
            }
    }
    GeneratedSystem.OrbitalRadius = GeneratedSystem.OrbitalDistances[EntryLocation];
}

//simple formula for surface area of a sphere
double ComputeSurfaceAreaFromRadius(System &GeneratedSystem){
	return 4*pi*(pow(GeneratedSystem.PlanetRadius,2));
}

//how much gas is there in a column above 1sq meter of land?
double MassOfGasIn1sqm(System &GeneratedSystem, double MassOfGas){
	double SurfaceArea = ComputeSurfaceAreaFromRadius(GeneratedSystem);
	double MassIn1sqm = MassOfGas/SurfaceArea;
	return MassIn1sqm;
}

//how many atoms are there in a column above 1sq m of land?
double AtomsOfGasIn1sqm(System &GeneratedSystem, double MassOfGas, double MolecularMass){
	double MassIn1sqm = MassOfGasIn1sqm(GeneratedSystem, MassOfGas);
	double NumberOfMoles = MassIn1sqm/MolecularMass;
	double NumberOfAtoms = NumberOfMoles*Avagadro;
	return NumberOfAtoms;
}

//what percentage of the light should make it through?
double AttenuationParameter(System &GeneratedSystem, char gas){
	double FudgeFactor;
	double MolecularArea;
	double MolecularMass;
	double MassOfGas;
	if (gas == 'w'){
        FudgeFactor = FudgeFactorWater;
        MolecularArea = pow(DiameterWater, 2);
        MolecularMass = MolecularMassWater;
        MassOfGas = GeneratedSystem.AtmosphereWater;
	}
	if (gas == 'o'){
        FudgeFactor = FudgeFactorOxygen;
        MolecularArea = pow(DiameterOxygen, 2);
        MolecularMass = MolecularMassOxygen;
        MassOfGas = GeneratedSystem.AtmosphereOxygen;
	}
	if (gas == 'n'){
        FudgeFactor = FudgeFactorNitrogen;
        MolecularArea = pow(DiameterNitrogen, 2);
        MolecularMass = MolecularMassNitrogen;
        MassOfGas = GeneratedSystem.AtmosphereNitrogen;
	}
	if (gas == 'c'){
        FudgeFactor = FudgeFactorCarbonDioxide;
        MolecularArea = pow(DiameterCarbonDioxide, 2);
        MolecularMass = MolecularMassCarbonDioxide;
        MassOfGas = GeneratedSystem.AtmosphereCarbonDioxide;
	}
    double NumberOfAtoms = AtomsOfGasIn1sqm(GeneratedSystem, MassOfGas, MolecularMass);
	double Exponent = -FudgeFactor*NumberOfAtoms*MolecularArea;
	return pow(e, Exponent);
	}

//compute how the atmospheric gasses filter the light
void ComputeLightFilter(System &GeneratedSystem){
    //what percentage of light to block for different compounds?
	//this value is the base and on earth, for all of them, it should be 0.5
	//this base value is then, as below, taken to a power based on wavelength
	double Water = AttenuationParameter(GeneratedSystem, 'w');
    double LargestFilter = Water;
	double Nitrogen = AttenuationParameter(GeneratedSystem, 'n');
	if (Nitrogen > LargestFilter){
        LargestFilter = Nitrogen;
	}
	double Oxygen = AttenuationParameter(GeneratedSystem, 'o');
	if (Oxygen > LargestFilter){
        LargestFilter = Oxygen;
	}
	double CarbonDioxide = AttenuationParameter(GeneratedSystem, 'c');
	if (CarbonDioxide > LargestFilter){
        LargestFilter = CarbonDioxide;
	}
	//define the values of the filter
	GeneratedSystem.AtmosphericFilter[0] = (pow(Nitrogen,0.3))*(pow(Oxygen,2.2))*Water;
	GeneratedSystem.AtmosphericFilter[1] =  (pow(Nitrogen,0.3))*(pow(Oxygen,2.2))*Water;
	GeneratedSystem.AtmosphericFilter[2] = (pow(Oxygen,2.2))*(pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[3] = (pow(Oxygen,2.2))*(pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[4] = (pow(Oxygen,2.2));
	GeneratedSystem.AtmosphericFilter[5] = (pow(Oxygen,2.2));
	GeneratedSystem.AtmosphericFilter[6] = (pow(Oxygen,2.2));
	GeneratedSystem.AtmosphericFilter[7] = pow(Oxygen,1.7);
	GeneratedSystem.AtmosphericFilter[8] = pow(Oxygen,1.7);
	GeneratedSystem.AtmosphericFilter[9] = pow(Oxygen,1.7);
	GeneratedSystem.AtmosphericFilter[10] = pow(Oxygen,1.7);
	GeneratedSystem.AtmosphericFilter[11] = (pow(Oxygen,1.7))*(pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[12] = (pow(Oxygen,1.7))*(pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[13] = (pow(Water,2.2))*(pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[14] = (pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[15] = (pow(Water,2.2))*1*Oxygen;
	GeneratedSystem.AtmosphericFilter[16] = (pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[17] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[18] = (pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[19] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[20] = (pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[21] = (pow(Water,2.2));
	GeneratedSystem.AtmosphericFilter[22] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[23] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[24] = (pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[25] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[26] = 1*Water;
	GeneratedSystem.AtmosphericFilter[27] = pow(CarbonDioxide,0.75);
	GeneratedSystem.AtmosphericFilter[28] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[29] = pow(CarbonDioxide,2.3);
	GeneratedSystem.AtmosphericFilter[30] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[31] = (pow(Oxygen,1.7));
	GeneratedSystem.AtmosphericFilter[32] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[33] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[34] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[35] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[36] = 1*Water;
	GeneratedSystem.AtmosphericFilter[37] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[38] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[39] = 1*CarbonDioxide;
	GeneratedSystem.AtmosphericFilter[40] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[41] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[42] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[43] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[44] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[45] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[46] = LargestFilter;
	GeneratedSystem.AtmosphericFilter[47] = (pow(Water,0.1));
	GeneratedSystem.AtmosphericFilter[48] = (pow(Water,0.1));
	GeneratedSystem.AtmosphericFilter[49] = LargestFilter;
}

void MassOfGasToClimateParameter(System &GeneratedSystem, float &Oxygen, float &CarbonDioxide){
    double const EarthOxygen = 1.03038e+018;
    double const EarthCarbonDioxide = 2.06076e+017;
    if (GeneratedSystem.AtmosphereOxygen < (0.5*EarthOxygen)){
        Oxygen = 0;
    }
    else if (GeneratedSystem.AtmosphereOxygen > (1.5*EarthOxygen)){
        Oxygen = 1;
    }
    else{
        Oxygen = (GeneratedSystem.AtmosphereOxygen/EarthOxygen) - 0.5;
    }
    if (GeneratedSystem.AtmosphereCarbonDioxide < (0.985*EarthCarbonDioxide)){
        CarbonDioxide = 0;
    }
    else if (GeneratedSystem.AtmosphereCarbonDioxide > (1.985*EarthCarbonDioxide)){
        CarbonDioxide = 1;
    }
    else{
        CarbonDioxide = (GeneratedSystem.AtmosphereCarbonDioxide/EarthCarbonDioxide) - 0.985;
    }
}

//compute the final temperature of the planet
void SetPlanetTemperature(System &GeneratedSystem){
    double IncomingSunlight = GeneratedSystem.Luminosity/(4*pi*(pow(GeneratedSystem.OrbitalRadius,2)));
    float Oxygen;
    float CarbonDioxide;
    MassOfGasToClimateParameter(GeneratedSystem, Oxygen, CarbonDioxide);
    GeneratedSystem.PlanetTemperature = ComputeTemperature(IncomingSunlight, CarbonDioxide, Oxygen);

}

int ComputeSystem(System &GeneratedSystem){
    if (GeneratedSystem.Earth == 0){
        GeneratedSystem.Earth = (rand()%2) + 1;
    }

    if (GeneratedSystem.StarMass == 0){
        if (GeneratedSystem.Earth == 2){
            GeneratedSystem.StarMass = 1; // solar masses
        }
        else {
            GeneratedSystem.StarMass = fRand(0.5,3); // solar masses
        }
    }

    //from the mass generate all the info about the star and habitable zone
    SetLifeSpan(GeneratedSystem);
    SetLuminosity(GeneratedSystem);
    SetRadius(GeneratedSystem);
    SetTemperature(GeneratedSystem);
    GenerateStellarSpectrum(GeneratedSystem);
    GeneratedSystem.MinOrbitalDiameter = GeneratedSystem.StarMass*BaseMinOrbitalDiameter;
    GeneratedSystem.MaxOrbitalDiameter = GeneratedSystem.StarMass*BaseMaxOrbitalDiameter;
    ComputeHabitableZone(GeneratedSystem);

    if (GeneratedSystem.OrbitalRadius == 0){
        ComputeOrbitalRadius(GeneratedSystem);
    }

    GeneratedSystem.GravitationalParameter = GravitationalConstant*GeneratedSystem.StarMass*MassOfOurSun;

    //generate all the info about the planet
    if (GeneratedSystem.Earth == 2){
        GeneratedSystem.PlanetRadius = RadiusOfTheEarth;
    }

    if (GeneratedSystem.PlanetRadius == 0){
        GeneratedSystem.PlanetRadius = fRand(MinimumPlanetRadius, MaximumPlanetRadius);
    }
    SetPlanetMass(GeneratedSystem);
    SetPlanetPeriod(GeneratedSystem);
    SetoSphereMasses(GeneratedSystem);
    if (GeneratedSystem.AtmosphereWater == 0){
        SetAtmosphereConstituents(GeneratedSystem);
    }
    ComputeLightFilter(GeneratedSystem);
    multiply(GeneratedSystem.StellarSpectrum, GeneratedSystem.AtmosphericFilter, GeneratedSystem.TerrestrialSpectrum);
    SetPlanetTemperature(GeneratedSystem);

}

void PrintSystemVariables(System GeneratedSystem){
    std::cout << "Current Star System\n";
    std::cout << "Earth Mode = " << GeneratedSystem.Earth << " (1 = Not Earth, 2 = Earth)\n";
    std::cout << "\n";
    std::cout << "The Star.\n";
    std::cout << "Star Mass = " << GeneratedSystem.StarMass << " Solar Masses.\n";
    std::cout << "Life Span = " << GeneratedSystem.LifeSpan << " of our years.\n";
    std::cout << "Luminosity = " << GeneratedSystem.Luminosity << " watts.\n";
    std::cout << "Radius = " << GeneratedSystem.Radius << " meters.\n";
    std::cout << "Temperature = " << GeneratedSystem.Temperature << " Kelvin.\n";
    std::cout << "\n";
    std::cout << "The Planet.\n";
    std::cout << "Orbital Radius = " << GeneratedSystem.OrbitalRadius << " meters.\n";
    std::cout << "Planet Radius = " << GeneratedSystem.PlanetRadius << " meters.\n";
    std::cout << "Planet Mass = " << GeneratedSystem.PlanetMass << " kg.\n";
    std::cout << "Planet Orbital Period = " << GeneratedSystem.PlanetOrbitalPeriod << " seconds = "
            << GeneratedSystem.PlanetOrbitalPeriod/3.154e+7 << " earth years. \n";
    std::cout << "Water : " << GeneratedSystem.AtmosphereWater << ", Oxygen : " << GeneratedSystem.AtmosphereOxygen
            << ", Nitrogen : " << GeneratedSystem.AtmosphereNitrogen << ", CO2: " << GeneratedSystem.AtmosphereCarbonDioxide
            << " kg in Atmosphere. \n";
    std::cout << "Planet Temperature = " << GeneratedSystem.PlanetTemperature << " Kelvin. \n";
    std::cout << "\n";

    //compute effectiveness of Chloroplasts
    double absorbtion_line_1 = 4.5e-7;
    double absorbtion_line_2 = 6.5e-7;
    std::cout << "Energy absorbed by Chloroplasts at line 1: " <<
        GeneratedSystem.TerrestrialSpectrum[int(absorbtion_line_1/WavelengthStep) - 1] << " watts. \n";
    std::cout << "Energy absorbed by Chloroplasts at line 2: " <<
        GeneratedSystem.TerrestrialSpectrum[int(absorbtion_line_2/WavelengthStep) - 1] << " watts. \n \n";

    if (ExtraDetail){
        std::cout << "Stellar Spectrum.\n";
        PrintSpectrum(GeneratedSystem.StellarSpectrum);
        std::cout << "\n";
        std::cout << "Terrestrial Spectrum. \n";
        PrintSpectrum(GeneratedSystem.TerrestrialSpectrum);
        std::cout << "\n";
        std::cout << "Habitability Scores in form Radius(m): Habitability Score. \n";
            for (int i = 0; i < NumberOfTests; i++){
            std::cout << GeneratedSystem.OrbitalDistances[i] << " : " << GeneratedSystem.HabitabilityScore[i] << "\n";
        }
    }
}

int main(){

    std::cout << "Thrive Planetary Generator Prototype.\n";
    srand (time(NULL));

    System GeneratedSystem;
    ComputeSystem(GeneratedSystem);
    PrintSystemVariables(GeneratedSystem);



}
