import numpy as np

class Solver(object):
    def __init__(self, solver_type):
        if solver_type == "np-least_squares":
            self.solve = lambda A, B: np.linalg.lstsq(A,B, rcond = -1)[0]
            self.solver_type = solver_type
        else:
            return ValueError("This solver does not exist: {}!".format(solver_type))

    def __str__(self):
        return self.solver_type
