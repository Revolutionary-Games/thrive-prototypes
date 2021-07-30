class Patch(object):
    def __init__(   self, depth, molecule_speed,
                    compound_amount,
                    compound_production,
                    name = "undefined",
                    compound_name = "Compound"):
        self.depth = depth
        self.molecule_speed = molecule_speed
        self.compound_amount = compound_amount
        self.compound_production = compound_production

        self.name = name
        self.compound_name = compound_name

    def __str__(self):
        return "Patch {}:\n".format(self.name)+\
                "\tDepth: {}m,\n".format(self.depth)+\
                "\tLocal speed: {}m/s,\n".format(self.molecule_speed)+\
                "\t{0} amount: {1} mol,\n".format(self.compound_name, self.compound_amount)+\
                "\t{0} production: {1} mol/s,\n".format(self.compound_name, self.compound_production)
