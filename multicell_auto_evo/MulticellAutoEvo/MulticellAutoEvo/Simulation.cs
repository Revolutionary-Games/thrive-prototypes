using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MulticellAutoEvo
{
    class Simulation
    {
        Critter[] critters;


        public Simulation(Critter[] critters)
        {
            this.critters = critters;
        }

        public Critter[] RunSimulation(int turns)
        {

            for(var turn = 0; turn < turns; turn++)
            {
                foreach(Critter critter in critters)
                {
                    critter.location = critter.location.TowardsPoint(critter.movementTarget, critter.species.Speed);
                }
            }
            return critters;
        }
    }
}
