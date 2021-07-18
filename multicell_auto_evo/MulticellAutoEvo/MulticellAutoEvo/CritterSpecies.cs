using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MulticellAutoEvo
{
    class CritterSpecies
    {

        // Variable names intentionally stupid because this isn't the code being demonstrated
        int Buffness;
        int Toughness;
        int Speed;

        public CritterSpecies()
        {
            Buffness = 10;
            Toughness = 10;
            Speed = 10;
        }

        public CritterSpecies(CritterSpecies ancestor)
        {
            this.Buffness = ancestor.Buffness;
            this.Toughness = ancestor.Toughness;
            this.Speed = ancestor.Speed;
        }
    }
}
