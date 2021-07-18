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

        public Critter[] RunSimulation()
        {
            return critters;
        }
    }
}
