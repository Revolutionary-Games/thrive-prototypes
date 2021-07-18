using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace MulticellAutoEvo
{
    [TestClass]
    public class SimulationTests
    {
        [TestMethod]
        public void SanityTest()
        {
            var species1 = new CritterSpecies();
            var species2 = new CritterSpecies();

            var critter1 = new Critter(species1);
            var critter2 = new Critter(species2);

            var simulation = new Simulation(new Critter[] { critter1, critter2 });
            var results = simulation.RunSimulation();

            CollectionAssert.Contains(results, critter1);
            CollectionAssert.Contains(results, critter2);
        }
    }
}
