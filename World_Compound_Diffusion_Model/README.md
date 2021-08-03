# Diffusion model for Compounds

This folder implements a prototype to model the diffusion of the compounds in a patch map.

___
## How does this work?

To be detailed...

___
## How to run

Before running this code, you have to select a setup first.
These can be found under the `setups` folder.

Conversely, you can create your own setup by adding or editing a JSON file.
More details on the parameters in section below.

To run the code, simply type the following line in your terminal, after moving to the directory containing this readme file.

`python3 main.py setups/FILE_NAME`

Example:

`python3 main.py setups/horizontal.json`

___
## Json parameters

Here is a description of the influence of the parameters of the JSON setup files.
All units are arbitrary.

- `"compound"`: the name of the compound, purely cosmetic.
- `"patches_data"`: a list describing all the patches in their initial state.
  - `"depth"`: depth of the patch. Useless now, but will be used in case of biased distribution (e.g. glucose drowning)
  - `"molecule_speed"`: the average speed of the compound molecules in the patch. Used in the model as increasing the number of molecules leaving the patch (and entering neighbour patches)
  - `"initial_compound_amount"`: the initial compound amount.
  - `"initial_compound_production"`: the initial compound production.
  - `"name"`: the name of the patch. Purely cosmetic, used to distinguish them more easily.
- `"patch_links"`: the list of the existing links between patches. Links between similar patches will override the values! Also, note that validity proofs requires all patches to be transitively linked (not two worlds in isolation)
  - `"patch1"`: the index of the first patch. Indices range from 0 to the number of patches minus 1.
  - `"patch2"`: the index of the second patch.
  - `"value"`: the value of the link, defining how well compounds flow from one to another. Should range from 0 to 1.
  - `"1-2 bias"`: the value of the bias in favor of movement from patch 1 to patch 2. Negative values indicate an actual bias from 2 to 1. Should range from -1 (no 1 -> 2) to 1(no 2-> 1). 0 means a balanced exchange.
- `"future_productions"`: list of the productions per patch for the upcoming time steps.
- `"step_duration"`: duration of the time step between two changes (elapsed time from editor). Note that the model assumes long-term dynamics, so weird behaviors can occur if too low!
- `"solver"`: the kind of solver to use to find the repartition. "np-least_squares" is the only implemented currently.
