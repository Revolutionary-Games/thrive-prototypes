import math

# The minimum positive price a compound can have.
MIN_POSITIVE_COMPOUND_PRICE = 0.00001

# The "willingness" of the compound prices to change.
# (between 0.0 and 1.0)
COMPOUND_PRICE_MOMENTUM = 0.2

# How much the "important" compounds get their price inflated.
IMPORTANT_COMPOUND_BIAS = 1000.0

# How important the storage space is considered.
STORAGE_SPACE_MULTIPLIER = 2.0

# Used to soften the demand according to the process capacity.
PROCESS_CAPACITY_DEMAND_MULTIPLIER = 15.0

# The initial variables of the system.
INITIAL_COMPOUND_PRICE = 10.0
INITIAL_COMPOUND_DEMAND = 1.0

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def demandSofteningFunction(processCapacity):
    return 2 * sigmoid(processCapacity * PROCESS_CAPACITY_DEMAND_MULTIPLIER) - 1.0

def calculatePrice(oldPrice, supply, demand):
    return math.sqrt(demand / (supply + 1)) * COMPOUND_PRICE_MOMENTUM + oldPrice * (1.0 - COMPOUND_PRICE_MOMENTUM)

def spaceSofteningFunction(availableSpace, requiredSpace):
    return 2.0 * (1.0 - sigmoid(requiredSpace / (availableSpace + 1.0) * STORAGE_SPACE_MULTIPLIER))

class CompoundData:
    def __init__(self, name, initial_amount):
        self.name = name
        self.amount = initial_amount
        self.uninflatedPrice = INITIAL_COMPOUND_PRICE
        self.price = INITIAL_COMPOUND_PRICE
        self.demand = INITIAL_COMPOUND_DEMAND
        self.priceReductionPerUnit = 0.0
        self.breakEvenPoint = 0.0

class Processor:
    def __init__(self, storage_space, compound_registry, process_registry, processes):
        self.total_space = storage_space
        self.occupied_space = 0
        self.compound_data = {}
        self.processes = processes.copy()

        for compound_name, compound in compound_registry.items():
            self.compound_data[compound_name] = CompoundData(compound_name, compound.initial_amount)
            self.occupied_space += compound.initial_amount

    def step(self, delta_time, process_registry, compound_registry):
        self.calculateStorageSpace()
        self.updateCompoundData(compound_registry)
        self.processCompounds(delta_time, compound_registry, process_registry)

    def printCompounds(self):
        for compound_name, compound_info in self.compound_data.items():
            print("Name: " + compound_name + " Amount: " + str(compound_info.amount) + " Price: " + str(compound_info.price) + " Demand: " + str(compound_info.demand))

    def calculateStorageSpace(self):
        self.occupied_space = 0
        for compound_name, compound_info in self.compound_data.items():
            self.occupied_space += compound_info.amount

    def updateCompoundData(self, compound_registry):
        for compound_name, compound_info in self.compound_data.items():
            # Edge case to get the prices above 0 if some demand exists.
            if compound_info.demand > 0 and compound_info.uninflatedPrice <= 0:
                compound_info.uninflatedPrice = MIN_POSITIVE_COMPOUND_PRICE

            # Adjusting the prices according to supply and demand.
            oldPrice = compound_info.uninflatedPrice
            compound_info.uninflatedPrice = calculatePrice(oldPrice, compound_info.amount, compound_info.demand)

            if compound_info.demand > 0 and compound_info.uninflatedPrice <= MIN_POSITIVE_COMPOUND_PRICE:
                compound_info.uninflatedPrice = MIN_POSITIVE_COMPOUND_PRICE

            # Setting the prices to 0 if they're below MIN_POSITIVE_COMPOUND_PRICE.
            if compound_info.uninflatedPrice < MIN_POSITIVE_COMPOUND_PRICE:
                compound_info.uninflatedPrice = 0
                compound_info.priceReductionPerUnit = 0

            # Calculating how much the price would fall if we had one more unit,
            # To make predictions with the demand.
            else:
                reducedPrice = calculatePrice(oldPrice, compound_info.amount + 1, compound_info.demand)
                compound_info.priceReductionPerUnit = compound_info.uninflatedPrice - reducedPrice

            # Inflating the price if the compound is useful outside of this system.
            compound_info.price = compound_info.uninflatedPrice
            if compound_registry[compound_name].is_useful:
                compound_info.price += (IMPORTANT_COMPOUND_BIAS + self.total_space - self.occupied_space) / (compound_info.amount + 1)
                reducedPrice = (IMPORTANT_COMPOUND_BIAS + self.total_space - self.occupied_space) / (compound_info.amount + 2)
                compound_info.priceReductionPerUnit += compound_info.price - reducedPrice

            # Calculating the break-even point
            if compound_info.price <= 0.0 or compound_info.priceReductionPerUnit <= 0.0:
                compound_info.breakEvenPoint = 0
            else:
                compound_info.breakEvenPoint = compound_info.price / compound_info.priceReductionPerUnit

            # Setting the demand to 0 in order to recalculate it later.
            compound_info.demand = 0

    def processCompounds(self, delta_time, compound_registry, process_registry):
        for process_name, max_rate in self.processes.items():
            process = process_registry[process_name]
            processLimitCapacity = max_rate * delta_time # big enough number.

            for input_name, input_needed in process.inputs.items():
                # Limiting the process by the amount of this required compound.
                processLimitCapacity = min(processLimitCapacity, self.compound_data[input_name].amount / input_needed)

            # Calculating the desired rate, with some liberal use of linearization.

            # Calculating the optimal process rate without considering the storage space.
            desiredRate = self.getOptimalProcessRate(process_name, False, process_registry, compound_registry)

            # Calculating the optimal process rate considering the storage space.
            desiredRateWithSpace = self.getOptimalProcessRate(process_name, True, process_registry, compound_registry)

            desiredRateWithSpace = min(desiredRateWithSpace, desiredRate)
            if desiredRate > 0.0:
                rate = min(max_rate * delta_time / 1000, processLimitCapacity, desiredRateWithSpace)

                # Running the process at the specified rate, transforming the inputs...
                for input_name, input_needed in process.inputs.items():
                    self.compound_data[input_name].amount -= rate * input_needed

                    # Phase 3: increasing the input compound demand.
                    self.compound_data[input_name].demand += desiredRate * input_needed * demandSofteningFunction(max_rate * input_needed)

                # ...into the outputs.
                for output_name, output_generated in process.outputs.items():
                    self.compound_data[output_name].amount += rate * output_generated

    def getOptimalProcessRate(self, process_name, considers_space, process_registry, compound_registry):
        # Calculating the price increment and the base price of the inputs
        # (the total price is rate * priceIncrement + basePrice).
        baseInputPrice = 0
        inputPriceIncrement = 0
        process = process_registry[process_name]

        for input_name, input_needed in process.inputs.items():
            input_data = self.compound_data[input_name]
            inputVolume = compound_registry[input_name].volume

            if(considers_space):
                spacePriceDecrement = spaceSofteningFunction(self.total_space - self.occupied_space, input_needed * inputVolume)
                inputPriceIncrement += input_needed * input_data.priceReductionPerUnit * spacePriceDecrement
                baseInputPrice += input_needed * input_data.price * spacePriceDecrement

            else:
                inputPriceIncrement += input_needed * input_data.priceReductionPerUnit
                baseInputPrice += input_needed * input_data.price

        # Finding the rate at which the costs equal the benefits.
        # The benefit curve is piecewise lineal and continuous, and the breaking points are
        # the break-even points of the output compounds.
        # So first we have to order said break-even points.
        outputBreakEvenPoints = self.getBreakEvenPointMap(process_name, process_registry)

        # Finding the piece of the function that contains the minimum
        # TODO: make it use binary search or something...
        baseOutputPrice = 0.0
        outputPriceDecrement = 0.0

        # Getting the initial revenue values
        for output_name, output_generated in process.outputs.items():
            output_data = self.compound_data[output_name]
            outputVolume = compound_registry[output_name].volume

            if considers_space:
                spacePriceDecrement = spaceSofteningFunction(self.total_space - self.occupied_space, output_generated * outputVolume)
                baseOutputPrice += output_data.price * output_generated * spacePriceDecrement
                outputPriceDecrement += output_data.priceReductionPerUnit * output_generated * spacePriceDecrement

            else:
                baseOutputPrice += output_data.price * output_generated
                outputPriceDecrement += output_data.priceReductionPerUnit * output_generated

        for breakEvenPoint in sorted(outputBreakEvenPoints.keys()):
            # Calculating the cost.
            cost = baseInputPrice + breakEvenPoint * inputPriceIncrement

            # Calculating the revenue.
            baseOutputPrice_l = 0.0
            outputPriceDecrement_l = 0.0
            for output_name, output_generated in process.outputs.items():
                output_data = self.compound_data[output_name]
                outputVolume = compound_registry[output_name].volume

                # The prices are never below 0.
                if(output_data.breakEvenPoint > breakEvenPoint):
                    if(considers_space) :
                        spacePriceDecrement = spaceSofteningFunction(self.total_space - self.occupied_space, output_generated * outputVolume)
                        baseOutputPrice_l += output_data.price * output_generated * spacePriceDecrement
                        outputPriceDecrement_l += output_data.priceReductionPerUnit * output_generated * spacePriceDecrement

                    else:
                        baseOutputPrice_l += output_data.price * output_generated 
                        outputPriceDecrement_l += output_data.priceReductionPerUnit * output_generated

            revenue = baseOutputPrice_l - breakEvenPoint * outputPriceDecrement_l

            if revenue < cost:
                # We found the piece :)
                break

            baseOutputPrice = baseOutputPrice_l
            outputPriceDecrement = outputPriceDecrement_l

        # Avoiding zero-division errors.
        if outputPriceDecrement + inputPriceIncrement > 0:
            desiredRate = (baseOutputPrice - baseInputPrice) / (outputPriceDecrement + inputPriceIncrement)
        else:
            desiredRate = 0.0
        if desiredRate <= 0.0: return 0.0
        return desiredRate

    def getBreakEvenPointMap(self, process_name, process_registry):
        result = {}

        for output_name, output_generated in process_registry[process_name].outputs.items():
            breakEvenPoint = self.compound_data[output_name].breakEvenPoint / output_generated
            result[breakEvenPoint] = output_name

        return result
