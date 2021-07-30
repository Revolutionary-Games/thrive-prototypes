import numpy as np

class WorldDiffusionSystem(object):
    def __init__(self, patch_map, linear_solver):
        self.patch_map = patch_map
        self.compound_total_amount = np.sum(patch_map.compute_repartition_vector())
        self.solver = linear_solver

    def __str__(self):
        return  "#"*5+" WORLD DIFFUSION SYSTEM "+"#"*5+"\n"+\
                "Solver: {}\n".format(self.solver)+\
                str(self.patch_map)

    def compute_new_repartition(self, compound_total_amount, production_vector):
        C = self.patch_map.compute_speed_matrix()
        C_inversed = self.patch_map.compute_inverted_speed_matrix()

        M = np.matmul(self.patch_map.links_matrix, C)
        P = production_vector

        X_0 = self.solver.solve(np.matmul(M,M), -np.matmul(M,P))
        Y_0 = np.matmul(C_inversed, np.ones((P.shape[0],)))

        lambda_value = (compound_total_amount - np.sum(X_0))/np.sum(Y_0)
        new_repartition = X_0 + lambda_value * Y_0

        return new_repartition

    def update_production(self, new_production_vector):
        self.patch_map.update_production(new_production_vector)

    def make_step(self, time_elapsed):
        production_vector = self.patch_map.compute_production_vector()

        compound_total_production = np.sum(production_vector)
        initial_compound_amount = np.sum(self.patch_map.compute_repartition_vector())
        compound_total_amount = initial_compound_amount + time_elapsed * compound_total_production

        new_repartition = self.compute_new_repartition(compound_total_amount, production_vector)

        for i, patch in enumerate(self.patch_map.patches):
            patch.compound_amount = new_repartition[i]
