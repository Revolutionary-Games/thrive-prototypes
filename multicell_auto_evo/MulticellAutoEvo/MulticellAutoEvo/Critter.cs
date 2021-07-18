using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MulticellAutoEvo
{
    // A multicellular thing
    class Critter
    {

        public CritterSpecies species;

        public Point location;
        public Point movementTarget;

        public Critter(CritterSpecies species)
        {
            this.species = species;
        }

    }
}
