using System;
using System.Collections.Generic;

public class species
{
	public int chloroplasts;
	public int chemoplasts;
	public int flagella;
	public int pilus;
	public int numberOfOrganelles;
	public int population;
	public float speedScore;
	public float energy;
	
	public species(Random random)
	{
		//how many of each organelle do you have?
		chloroplasts = random.Next(0,5);
		chemoplasts = random.Next(0,5);
		flagella = random.Next(0,5);
		
		pilus = random.Next(0,5);
		
		//how much energy have you gathered this turn?
		energy = 0;  
		
		//how fast are you? more flagella makes you faster, more organelles make you slower
		numberOfOrganelles = (1 + flagella + chloroplasts + chemoplasts + pilus);
		speedScore = (float)(1 + flagella)/numberOfOrganelles;
	}
}

public class patch
{
	public List<species> listOfSpecies = new List<species>();
	public float sunlight; //how much sunlight energy enters the patch?
	public float hydrogen; //how much hydrogen sulfide is in the patch?
	public int totalChloroplasts = 0; //what is the total number of chloroplasts in all species in the patch?
	public int totalChemoplasts = 0;
	public int totalPilus = 0;
	
	public patch()
	{
		Random random = new Random();
		for (var i = 0; i < 5; i++)
		{
			listOfSpecies.Add(new species(random));
		}
		
		//compute total numbers of organelles in the patch
		foreach (species spec in listOfSpecies)
		{
			totalChloroplasts += spec.chloroplasts;
			totalChemoplasts += spec.chemoplasts;
			totalPilus += spec.pilus;
		}
		
		//make sure not to divide by zero
		if (totalChloroplasts == 0) {totalChloroplasts = 1;}
		if (totalChemoplasts == 0) {totalChemoplasts = 1;}
		if (totalPilus == 0) {totalPilus = 1;}
		
		//set up environmental variables
		sunlight = random.Next(0,100000);
		hydrogen = random.Next(0,100000);
	}
	
	public void computePopulations()
	{
		float predationEnergyPool = 0;
		
		foreach (species spec in listOfSpecies)
		{
			//start with 0 energy
			spec.energy = 0;
			
			//gather sunlight
			float myShareOfSunlight = (float)spec.chloroplasts/totalChloroplasts;
			spec.energy += sunlight*myShareOfSunlight;
			
			//gather hydrogen sulfide
			float myShareOfHydrogen = (float)spec.chemoplasts/totalChemoplasts;
			spec.energy += hydrogen*myShareOfHydrogen;
			
			//donate energy to the predation energy pool
			predationEnergyPool += 0.5f*spec.energy;
			spec.energy *= 0.5f;
		}
		
		//share out the predation pool based on combat strength and compute population
		foreach (species spec in listOfSpecies)
		{
			float myCombatStrength = (float)spec.pilus/totalPilus;
			spec.energy += predationEnergyPool*myCombatStrength;
			
			spec.population = (int)(spec.energy/(Math.Pow(spec.numberOfOrganelles,1.3)));
		}
		
	}
}

public class Program
{
	
	public static void Main()
	{
		Console.WriteLine("Basic Population Calculator");
		Console.WriteLine(" ");
		patch mainPatch = new patch();
		mainPatch.computePopulations();
		Console.WriteLine("Patch Data: Sunlight, Hydrogen Sulfide, Total Chloroplasts, Total Chemoplasts");
		
		Console.WriteLine(mainPatch.sunlight.ToString().PadLeft(15) 
						+ ", " + mainPatch.hydrogen.ToString().PadLeft(15)
						+ ", " + mainPatch.totalChloroplasts.ToString().PadLeft(15)
						+ ", " + mainPatch.totalChemoplasts.ToString().PadLeft(15));
		
		Console.WriteLine(" ");
		Console.WriteLine("Species Data");
		Console.WriteLine("Population, Chloroplasts, Chemoplasts, Flagella, Pilus, Total Organelles, SpeedScore, Energy");
		
		foreach (species spec in mainPatch.listOfSpecies)
		{
			Console.WriteLine(spec.population.ToString().PadLeft(10) 
							  + ", " + spec.chloroplasts.ToString().PadLeft(10)
							  + ", " + spec.chemoplasts.ToString().PadLeft(10) 
							  + ", " + spec.flagella.ToString().PadLeft(10)
							  + ", " + spec.pilus.ToString().PadLeft(5)
							  + ", " + (spec.numberOfOrganelles-1).ToString().PadLeft(12)
							  + ", " + spec.speedScore.ToString().PadLeft(14)
							  + ", " + spec.energy.ToString().PadLeft(10));
		}
	}
}