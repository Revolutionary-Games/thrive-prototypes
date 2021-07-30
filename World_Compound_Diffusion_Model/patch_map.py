import numpy as np

class PatchMap(object):
    def __init__(self, patches, patch_links):
        self.num_patches = len(patches)
        self.patches = patches
        self.links_matrix = np.zeros((self.num_patches, self.num_patches))
        self.fill_link_matrix(patch_links)

    def __str__(self):
        return "Patch map:\n"+\
                "-Links: \n{}\n".format(self.links_matrix) +\
                "-Speeds: \n{}\n".format(self.compute_speed_matrix()) +\
                "-Repartition: \n{}\n".format(self.compute_repartition_vector()) +\
                "-Production: \n{}\n".format(self.compute_production_vector())

    def fill_link_matrix(self, patch_links):
        print(patch_links)
        for (patch_index1, patch_index2, link_value) in patch_links:
            self.links_matrix[patch_index1, patch_index2] = link_value
            self.links_matrix[patch_index2, patch_index1] = link_value

        for i in range(self.num_patches):
            self.links_matrix[i,i] = -np.sum(self.links_matrix[i,:])

    def update_production(self, new_production_vector):
        for i, patch in enumerate(self.patches):
            patch.compound_production = new_production_vector[i]

    ####### MATRICES #######

    def compute_speed_matrix(self):
        speed_matrix = np.eye(self.num_patches)
        for i, patch in enumerate(self.patches):
            speed_matrix[i,i] = patch.molecule_speed
        return speed_matrix

    # helper to fasten computations
    def compute_inverted_speed_matrix(self):
        inverted_speed_matrix = np.eye(self.num_patches)
        for i, patch in enumerate(self.patches):
            inverted_speed_matrix[i,i] = 1/patch.molecule_speed
        return inverted_speed_matrix

    def compute_repartition_vector(self):
        repartition_vector = np.zeros((self.num_patches,))
        for i, patch in enumerate(self.patches):
            repartition_vector[i] = patch.compound_amount
        return repartition_vector

    def compute_production_vector(self):
        production_vector = np.zeros((self.num_patches,))
        for i, patch in enumerate(self.patches):
            production_vector[i] = patch.compound_production
        return production_vector
