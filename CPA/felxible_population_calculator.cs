using System;
using System.Collections.Generic;
				
public class species
{
	public List<string> organelles = new List<string>();
	public int numberOfOrganelles;
	public int population;
	public float speedScore;
	public float energy;
	
	public species(Random random, List<string> resources, Dictionary<string, string> resourceGathered, Dictionary<string, float> gatheringEffectiveness)
	{
		//how many of each organelle do you have?
		numberOfOrganelles = random.Next(2,7);
		//add organelles at random
		for (var i = 0; i < numberOfOrganelles; i++){
			List<string> keyList = new List<string>(resourceGathered.Keys);
			int index = random.Next(keyList.Count);
			organelles.Add(keyList[index]);	
			Console.WriteLine(keyList[index]);
		}

		
		//how much energy have you gathered this turn?
		energy = 0;  
		
		//how fast are you? more flagella makes you faster, more organelles make you slower
		//numberOfOrganelles = (1 + flagella + chloroplasts + chemoplasts + pilus);
		//speedScore = (float)(1 + flagella)/numberOfOrganelles;
	}
}

public class Program
{
	public static void Main()
	{
		//what resources are available in the world?
		List<string> primaryResources = new List<string>(){"sunglight", "hydrogen", "iron"}; 
		
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
			{"chloroplast", 2.0f},
			{"rusticyanin", 1.0f},
			{"chemoplast", 1.0f}
		};
		
		Console.WriteLine("Population Calculator using lists");
		Console.WriteLine(" ");
		
		Random random = new Random();
		new species(random, primaryResources, resourceGathered, gatheringEffectiveness);
	}
}