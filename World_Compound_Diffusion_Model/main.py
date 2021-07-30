import matplotlib.pyplot as plt
import numpy as np
import json

from patch import Patch
from patch_map import PatchMap
from world_diffusion_system import WorldDiffusionSystem
from solver import Solver
import plotting

def define_patches(data):
    patches = [
        Patch(  patch_data["depth"], patch_data["molecule_speed"],
                patch_data["initial_compound_amount"],
                patch_data["initial_compound_production"],
                compound_name = data["compound"],
                name = patch_data["name"])
        for patch_data in data["patches_data"]
    ]

    for patch in patches:
        print(patch)

    return patches

def define_patches_and_patch_map(data):
    patches = define_patches(data)

    patch_links = [
        (link_data["patch1"],link_data["patch2"], link_data["value"])
        for link_data in data["patch_links"]
    ]

    patch_map = PatchMap(patches, patch_links)

    print(patch_map)

    return patches, patch_map

def run_simulation(data):
    patches, patch_map = define_patches_and_patch_map(data)
    solver = Solver(data["solver"])
    world_diffusion_system = WorldDiffusionSystem(patch_map, solver)

    initial_productions = [patch.compound_production for patch in patches]
    productions_over_time = [initial_productions] + data["future_productions"]
    num_steps = len(productions_over_time)

    repartition_snapshots = [world_diffusion_system.patch_map.compute_repartition_vector()]

    for i in range(num_steps):
        print("# STEP {}".format(i))
        world_diffusion_system.update_production(productions_over_time[i])
        world_diffusion_system.make_step(data["step_duration"])
        repartition_snapshots.append(world_diffusion_system.patch_map.compute_repartition_vector())
        print(world_diffusion_system)

    return patches, patch_map, world_diffusion_system, np.asarray(repartition_snapshots)


if __name__=="__main__":
    SETUP_FILE_PATH = "setups/horizontal.json"
    with open(SETUP_FILE_PATH) as f:
        data = json.load(f)

    patches, patch_map, world_diffusion_system, repartition_snapshots = run_simulation(data)
    plotting.plot_compound_in_patches(patches, repartition_snapshots)
    plotting.plot_repartitions(patches, repartition_snapshots)
