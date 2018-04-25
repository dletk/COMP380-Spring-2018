"""
File: MCLStarter.py

This file contains the class definition of a Monte Carlo Localizer. Your task is to fill in the
incomplete methods that implement the MCL algorithm. This works on a straight map, where the robot
moves parallel to a wall and gets information about whether there is a wall, or no wall, or something
confusing.

Units throughout are in centimeters.
"""

import random


class MonteCarloLocalizer:
    """Implementation of the Monte Carlo Localization algorithm for a simple, one-dimensional movement."""

    def __init__(self, numParticles, minValue, maxValue, worldMap):
        """This takes in the number of particles to maintain, the minimum and maximum positional values
        that are allowed, and a map of the world. The map's format is a list of tuples. Each tuple has a low
        and high values that marks the ends of a region, and then whether or not that region has a wall
        or no wall."""
        self.doorsMap = worldMap
        self.numParticles = numParticles
        self.minValue = minValue
        self.maxValue = maxValue
        self.countCycles = 0      # This should be updated in mclCycle to count how many cycles have run
        self.displayBins = 40

        # set up initial samples, and then display the text version of the map and histogram
        self.samples = []
        self.weights = []
        self.initSamples()
        self.printMCLStatus()


    def initSamples(self):
        """Creates self.numParticles samples, each of which are generated randomly
        with a uniform distribution across the range from minVal to maxVal."""
        pass
        # Define this (note random.uniform is helpful here!)


    def mclCycle(self, moveData, senseData):
        """Main MCL cycle. This performs one "cycle" given movement data and sensor data,
        it updates the samples with the motion, and then resamples based on consistency with the sensor data.
        The movedata is a single number, the distance traveled. The senseData is a string, one of: "wall",
        "no wall", or "unknown"."""
        self.countCycles += 1
        # Insert code for these steps here:
        # 1. Set up a new sample list and a new weights list
        # 2. Loop over every particle, and for each particle:
        # 3.    Call motionUpdate on the particle and moveData
        # 4.    Compute the new weight for this particle by calling perceptionUpdate on the new (updated) location
        # 5.    Add these to the new samples and new weights lists
        # 6. Normalize the weights (note I've provided a method for this)
        # 7. Use the weights to resample from the new sample list (see the method I've provided)
        # 8. Store the new samples into self.samples, and the new weights to a local variable, newSampleWeights

        self.printMCLStatus()
        CoM =  self.findCenterOfMass(newSampleWeights)
        return CoM


    def motionUpdate(self, newY, deltaY):
        """Given particle's y value, and move information, which is the reported change in y,
        this updates the old position accordingly, adding a random amount of noise based on a gaussian
        distribution. The updated value is returned
        """
        pass
        # You define this one

    def perceptionUpdate(self, newParticle, sensorData):
        """This takes in a new particle/location, and the sensor data, which is one of "wall",
        "no wall", or "unknown", and it uses the map measurements to determine what we expect."""
        expectedVal = self.getMapValue(newParticle)
        if expectedVal == sensorData:
            return 100
        elif sensorData == "unknown":
            return 10
        else:
            return 0.5
        print("Should never get here!", newParticle, sensorData)
        return 0

    def getMapValue(self, yLoc):
        """Given a y location, return the value from the map at that location.
        Helper to perceptionUpdate and also to reportResults."""
        for (lo, hi, mapVal) in self.doorsMap:
            if lo <= yLoc < hi:
                return mapVal
        return "unknown"

    def resample(self, samplePool, weights):
        """Takes in pool of new samples and corresponding weights, and it resamples from them.
        It makes a corresponding weight associated with each chose new particle, for later use."""
        newSamples = random.choices(samplePool, weights, k=self.numParticles)
        newW = []
        for s in newSamples:
            indx = samplePool.index(s)
            newW.append(weights[indx])
        return newSamples, newW

    def normalize(self, weights):
        """Takes a bunch of newly-computed weights and normalizes them so they add up to 1.0"""
        tot = sum(weights)
        newW = [-1] * self.numParticles
        for i in range(len(weights)):
            newW[i] = weights[i] / tot
        return newW

    def findCenterOfMass(self, newSampleWeights):
        """Computes the center of mass of the particles, as the weighted average of locations and current weights"""
        # First must normalize the weights
        normedWeights = self.normalize(newSampleWeights)
        weightedAvg = 0
        for i in range(self.numParticles):
            weightedAvg += self.samples[i] * normedWeights[i]
        return weightedAvg

    def printMCLStatus(self):
        """Prints a text version """
        print()
        print("====================")
        print("Cycle", self.countCycles)
        self._printHist()

    def _printHist(self):
        """Prints a rough histogram with 20 bins"""
        bins = [0] * self.displayBins
        binSize = self.maxValue / self.displayBins
        displaySamps = self.samples[:]
        displaySamps.sort()
        currLimit = binSize
        binIndex = 0
        partIndex = 0
        while partIndex < self.numParticles:
            part = displaySamps[partIndex]
            if binIndex >= self.displayBins:
                # if value beyond max value, add to last bin and go on to next particle
                bins[19] += 1
                partIndex += 1
            elif part < currLimit:
                # count particle in current bin, go on to next particle
                bins[binIndex] += 1
                partIndex += 1
            else:
                # go on to next bin, don't go on to next particle
                binIndex += 1
                currLimit += binSize
        self.printMapPattern(binSize)
        histStr = "{0:3d} "
        printStr = ""
        for b in bins:
            printStr += histStr.format(b)
        print(printStr)

    def printMapPattern(self, binSize):
        """From the map, determines which bins are walls and which are not, and prints a line with gaps,
        sized to match the histogram string that is printed next"""
        ticks = self.displayBins * 4
        tickSize = self.maxValue / ticks
        val = tickSize
        mapStr = ""
        while val < self.maxValue:
            mapVal = self.getMapValue(val)
            if mapVal == "wall":
                mapStr += "="
            else:
                mapStr += " "
            val += tickSize
        print(mapStr)

    def printPoint(self, yVal, label):
        """Given a y location and a single-character label for it, it prints it where
        it should be, consistent with the map pattern that is printed"""
        ticks = self.displayBins * 4
        tickSize = self.maxValue / ticks
        mapList = [' '] * ticks
        currVal = tickSize
        for pos in range(ticks):
            currVal = tickSize * (pos + 1)
            if yVal < currVal:
                mapList[pos] = label
                break
        mapStr = "".join(mapList)
        print(mapStr)



def MCLDemo():
    """This runs a simple simulation where the robot starts at 1cm and moves about 2 cm each time until it gets
    to the far end"""
    doorsWorld = [(0.0, 32.0, "wall"), (32.0, 48.0, "no wall"),
                  (48.0, 93.0, "wall"), (93.0, 109.0, "no wall"), (109.0, 121.0, "wall"),
                  (121.0, 137.0, "no wall"), (137.0, 182.0, "wall"), (182.0, 185.0, "no wall")]
    opposites = {"wall": "no wall", "no wall": "wall"}

    monte = MonteCarloLocalizer(1000, 0, 185, doorsWorld)

    # quick simulation to test the code
    actualLoc = 1.0
    expectedLoc = 1.0
    twoNumsStr = "{0:7.3f}  {1:7.3f}"
    print("------------ Initial location, expected and actual:", twoNumsStr.format(expectedLoc, actualLoc))
    while expectedLoc < 180:
        distMoved = random.gauss(2.0, 0.25)
        print("------------ Movement, expected and actual:", twoNumsStr.format(2.0, distMoved))

        expectedLoc += 2.0
        actualLoc = actualLoc + distMoved
        print("------------ New location, expected and actual:", twoNumsStr.format(expectedLoc, actualLoc))

        actualSensor = monte.getMapValue(actualLoc)
        oppSensor = opposites[actualSensor]
        sensorData = random.choices([actualSensor, oppSensor, "unknown"], [96, 1, 4])
        reportedData = sensorData[0]
        print("------------ Sensor value, actual and reported:", actualSensor, reportedData)

        result = monte.mclCycle(2.0, reportedData)
        monte.printPoint(expectedLoc, 'E')
        monte.printPoint(actualLoc, 'A')
        if result is not None:
            monte.printPoint(result, 'C')
            print("MCL Result:", result)

if __name__ == "__main__":
    MCLDemo()


