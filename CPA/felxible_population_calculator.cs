using System;
using System.Collections.Generic;
				
public class species
{
	public List<string> organelles = new List<string>();
	public int numberOfOrganelles;
	public int population;
	public float speedScore;
	public float energy;
	public float currentResourceScore;
	
	public species(Random random, Dictionary<string, string> resourceGathered)
	{
		Console.WriteLine("Making new species with organelles:");
		//how many of each organelle do you have?
		numberOfOrganelles = random.Next(2,7);
		//add organelles at random
		for (var i = 0; i < numberOfOrganelles; i++){
			List<string> keyList = new List<string>(resourceGathered.Keys);
			int index = random.Next(keyList.Count);
			organelles.Add(keyList[index]);	
			Console.WriteLine(keyList[index]);
		}
		Console.WriteLine(" ");

		
		//how much energy have you gathered this turn?
		energy = 0;  
		
		//how fast are you? more flagella makes you faster, more organelles make you slower
		//numberOfOrganelles = (1 + flagella + chloroplasts + chemoplasts + pilus);
		//speedScore = (float)(1 + flagella)/numberOfOrganelles;
	}
}

public class patch
{
	public List<species> listOfSpecies = new List<species>();
	public Dictionary<string, float> myAvailablePrimaryResources = new Dictionary<string, float>();
	
	public patch(Dictionary<string, float> availablePrimaryResources, Dictionary<string, string> resourceGathered, Dictionary<string, float> gatheringEffectiveness)
	{
		Random random = new Random();
		for (var i = 0; i < 5; i++)
		{
			listOfSpecies.Add(new species(random, resourceGathered));
			myAvailablePrimaryResources = availablePrimaryResources;
		}
	}
	
	public void computePopulations(Dictionary<string, string> resourceGathered, Dictionary<string, float> gatheringEffectiveness)
	{
		
		//zero out the energy for all species
		foreach (species spec in listOfSpecies)
		{
			//start with 0 energy
			spec.energy = 0;
			
		}
		//for each resource that can be gathered
		foreach (KeyValuePair<string, float> resource in myAvailablePrimaryResources)
		{
		
			//work out the total number of organelles in the patch, weighted by their effectiveness
			float totalResourceGathering = 0;
			foreach (species spec in listOfSpecies)
			{
				spec.currentResourceScore = 0;
				//in each species work out which organelles they have which can help and weight them by their effectiveness
				foreach (string organelle in spec.organelles)
				{
					if (resourceGathered[organelle] == resource.Key)
					{
						Console.WriteLine("adding weight, " + resource.Key + " " + gatheringEffectiveness[organelle].ToString());
						spec.currentResourceScore += gatheringEffectiveness[organelle];
						totalResourceGathering += gatheringEffectiveness[organelle];
					}
				}
			}
			
			Console.WriteLine("Resource " + resource + " total score = " + totalResourceGathering);
		
			//for each species give them energy proportional to their gathering effectiveness
			if (totalResourceGathering > 0)
			{
				foreach (species spec in listOfSpecies)
				{
					spec.energy += resource.Value*spec.currentResourceScore;	
				}
			}
			
		}
		
		//this is where the predation relations need to be added
		
		//work out the population for each species based on how much energy they have collected
		foreach (species spec in listOfSpecies)
		{
			spec.population = (int)(spec.energy/(Math.Pow(spec.numberOfOrganelles,1.3)));	
		}
		
	}
	
}

public class Program
{
	public static void Main()
	{
		
		//for each organelle which resource do they gather?
		Dictionary<string, string> resourceGathered = new Dictionary<string, string>(){
			{"thylakoid", "sunlight"},
			{"chloroplast", "sunlight"},
			{"rusticyanin", "iron"},
			{"chemoplast", "hyrdrogen"},
			{"flagella","none"},
			{"pilus", "none"},
		};
		
		//how effective is that organelle at gathering resources
		Dictionary<string, float> gatheringEffectiveness = new Dictionary<string, float>(){
			{"thylakoid", 1.0f},
			{"chloroplast", 1.5f},
			{"rusticyanin", 1.0f},
			{"chemoplast", 1.0f}
		};
		
		//for this patch what resources are available?
		Dictionary<string, float> availablePrimaryResources = new Dictionary<string, float>()
		{
			{"sunlight", 10000.0f},
			{"iron", 10000.0f},
			{"hydrogen", 10000.0f},		
		};
		
		Console.WriteLine("Population Calculator using lists");
		Console.WriteLine(" ");
		
		patch mainPatch = new patch(availablePrimaryResources, resourceGathered, gatheringEffectiveness);
		mainPatch.computePopulations(resourceGathered, gatheringEffectiveness);
		
		Console.WriteLine(" ");
		Console.WriteLine("Population, Energy Gathered, Organelles");
		foreach (species spec in mainPatch.listOfSpecies)
		{
			string organellesString = "     ";
			foreach (string organelle in spec.organelles)
			{
				organellesString += organelle;
				organellesString += ", ";
			}
			Console.WriteLine(spec.population.ToString().PadLeft(10) 
							  + ", " + spec.energy.ToString().PadLeft(10)
							  + ", " + organellesString.PadLeft(10));
		}
		
	}
}