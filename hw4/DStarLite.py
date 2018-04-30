###############################################
# D* Lite
# Susan Fox
# Spring 2016

"""This file contains an implementation of D* Lite. Because of the different\
pieces of this algorithm, and their need to access a lot of shared data, and\
the way in which the algorithm must be restarted when new information comes in, it
made sense to make a class to contain the information. I have separated the outer loop, where
it computes shortest path and then waits for new information, into external functions. The purpose of
the class is to contain the information that is generated, including the priority queue,
and to respond with methods that implement the key features of the algorithm."""

import random
from FoxQueue import Queue, PriorityQueue
import time
import math


class DStarAlgorithm:

    def __init__(self, graph, startVert, goalVert):
        """Takes in a graph, start vertex and goal vertex, and sets up the D* Lite
        search, initializing all the data structures and the priority queue."""
        self.graph = graph
        self.startVert = startVert
        self.goalVert = goalVert
        self.maxVal = 1000

        self.rhs = {}
        self.pred = {}
        self.g = {}
        self.u = None

        self.initialize()

    def initialize(self):
        """The Initialize algorithm from the pseudocode."""
        self.u = PriorityQueue()
        vertices = self.graph.getVertices()
        for vert in vertices:
            self.rhs[vert] = self.maxVal
            self.g[vert] = self.maxVal
        self.rhs[self.startVert] = 0
        self.u.insert(priority=self.calculateKey(
            self.startVert), val=self.startVert)

    def computeShortestPath(self):
        """The ComputeShortestPath algorithm from the pseudocode."""
        while (not self.u.isEmpty()) and (self.compareKeys(self.u.firstElement()[0], self.calculateKey(self.goalVert))) or (self.rhs[self.goalVert] != self.g[self.goalVert]):
            # The first element has the form (priority, value)
            # print("=====> ", self.u.firstElement())
            vert = self.u.firstElement()[1]
            # print(vert)

            self.u.delete()

            if self.g[vert] > self.rhs[vert]:
                self.g[vert] = self.rhs[vert]
            else:
                self.g[vert] = self.maxVal
                self.updateVertex(vert)

            vertNeighbors = self.graph.getNeighbors(vert)
            # Get neighbor returns a list in the form of (vert, weight)
            for v in vertNeighbors:
                # Using v[0] to only take out the vert, not with the weight
                # print("====>", v)
                v = v[0]
                self.updateVertex(v)
        return self.reconstructPath()

    def updateVertex(self, vert):
        """The UpdateVertex algorithm from the pseudocode."""
        if vert != self.startVert:
            self.rhs[vert] = self.minNeighCost(vert)
        if self.u.contains(vert):
            self.u.removeValue(value=vert)
        if self.g[vert] != self.rhs[vert]:
            self.u.insert(self.calculateKey(vert), vert)
        # print(self.u)

    def minNeighCost(self, vert):
        """A helper to compute the new rhs value, by finding the minimum cost among
        all the neighbors of a vertex. The cost is computed as the g cost of the
        neighbor plus the edge cost between the neighbor and the vertex."""
        minNCost = self.maxVal
        minVert = -1
        for neighInfo in self.graph.getNeighbors(vert):
            neigh = neighInfo[0]
            edgeCost = neighInfo[1]
            newCost = self.g[neigh] + edgeCost
            if newCost < minNCost:
                minNCost = newCost
                minVert = neigh
        return minNCost

    def calculateKey(self, vert):
        """The CalculateKey algorithm from the pseudocode."""
        minG = min(self.g[vert], self.rhs[vert])
        heurCost = self.graph.heuristicDist(vert, self.goalVert)
        return [minG + heurCost, minG]

    def compareKeys(self, key1, key2):
        """Takes in two keys, each of which is a list containing f cost
        and g cost. It prefers the lower f cost, but for equal f costs
        it chooses the lower g cost."""
        [f1, g1] = key1
        [f2, g2] = key2
        return (f1 < f2) or ((f1 == f2) and (g1 < g2))

    def correctInformation(self, newInfo):
        """Takes in a dictionary whose keys are (r, c) tuples, and the value
        is the newly corrected cell weight. Updates the graph, and then updates
        the search information appropriately."""
        for (r, c) in newInfo:
            self.graph.setCellValue(r, c, newInfo[r, c])
        self.graph.graphFromGrid()
        for (r, c) in newInfo:
            nodeNum = r * self.graph.getWidth() + c
            #print("(", r, c, ")", nodeNum)
            self.updateVertex(nodeNum)
            neighs = self.graph.getNeighbors(nodeNum)
            for (nextNeigh, wgt) in neighs:
                self.updateVertex(nextNeigh)

    def reconstructPath(self):
        """ Given the start vertex and goal vertex, and the table of
        predecessors found during the search, this will reconstruct the path
        from start to goal"""

        path = [self.goalVert]
        currVert = self.goalVert
        while currVert != self.startVert:
            currVert = self._pickMinNeighbor(currVert)
            path.insert(0, currVert)
        return path

    def _pickMinNeighbor(self, vert):
        """A helper to path-reconstruction that finds the neighbor of a vertex
        that has the minimum g cost."""
        neighs = self.graph.getNeighbors(vert)
        minVal = self.maxVal
        minNeigh = None
        for [neigh, cost] in neighs:
            if self.g[neigh] < minVal:
                minVal = self.g[neigh]
                minNeigh = neigh
        return minNeigh


# ---------------------------------------------------------------
def DStarRoute(graph, startVert, goalVert):
    """ This algorithm searches a graph using D* Lite looking for a path from
    some start vertex to some goal vertex It uses a queue to store the
    indices of vertices that it still needs to examine. This version of D*
    Lite is equivalent to A*, because the information used in the search is
    all accurate."""

    dStarRunner = DStarAlgorithm(graph, startVert, goalVert)
    route = dStarRunner.computeShortestPath()
    return route


def DStarGlobal(graph, startVert, goalVert, percWrong=20):
    """This algorithm search a graph using D* Lite for
    a path from some start to some goal. It simulates incorrect
    information about the world by modifying percWrong percent
    of the cells in the graph to have a different value. Then,
    after the first route is generated, the correct data is
    provided to the DStarLite object, and it updates its route."""
    if graph.__class__.__name__ != "GridGraph":
        print("DStarGlobal only works on Grid Graphs, try again.")
        return
    correctInfo, incorrectGraph = corruptGraph(graph, percWrong)
    # print("CORRUPTED GRAPH:")
    # incorrectGraph.printGrid()
    dStarRunner = DStarAlgorithm(incorrectGraph, startVert, goalVert)
    t1 = time.time()
    route1 = dStarRunner.computeShortestPath()
    t2 = time.time()
    print("First route found is:")
    print(route1)
    print("Time elapsed:", t2 - t1)
    # graph.printWithRoute(route1)

    # print("--------")
    # print("CORRECT MAP:")
    # graph.printGrid()
    print("Correcting information...")
    dStarRunner.correctInformation(correctInfo)

    t1 = time.time()
    route2 = dStarRunner.computeShortestPath()
    t2 = time.time()
    if route1 == route2:
        print("SAME ROUTE")
    print("Fixed route found is:")
    print(route2)
    print("Time elapsed:", t2 - t1)
    # graph.printWithRoute(route2)
    return route2


def DStarLocal(graph, startVert, goalVert, percWrong=20):
    """This algorithm search a graph using D* Lite for
    a path from some start to some goal. It simulates incorrect
    information about the world by modifying percWrong percent
    of the cells in the graph to have a different value. Then,
    after the first route is generated, the function determines when
    the route comes close to an incorrect value, and it feeds a small number of corrections at a time to DStarLite.."""
    if graph.__class__.__name__ != "GridGraph":
        print("DStarGlobal only works on Grid Graphs, try again.")
        return
    correctInfo, incorrectGraph = corruptGraph(graph, percWrong)
    print("CORRUPTED GRAPH:")
    dStarRunner = DStarAlgorithm(incorrectGraph, startVert, goalVert)
    print("First pass...")
    t1 = time.time()
    route1 = dStarRunner.computeShortestPath()
    t2 = time.time()
    print("First route found is:")
    print(route1)
    print("Time elapsed:", t2 - t1)
    # incorrectGraph.printWithRoute(route1)
    mapWid = graph.getWidth()
    mapHgt = graph.getHeight()
    for cell in route1:
        (r, c) = graph.getData(cell)
        badNeighbors = findIncorrectNeighbors(correctInfo, r, c, mapWid, mapHgt)
        if len(badNeighbors) > 0:
            print("Incorrect neighbors:", badNeighbors)
            print("Correcting information...")
            dStarRunner.correctInformation(badNeighbors)
            t1 = time.time()
            nextRoute = dStarRunner.computeShortestPath()
            t2 = time.time()
            print("Fixed route found is:")
            print(nextRoute)
            print("Time elapsed:", t2 - t1)
            # graph.printWithRoute(nextRoute)
    return nextRoute


def findIncorrectNeighbors(correctInfo, row, col, wid, hgt):
    """Takes in the dictionary of correct information, along
    with a row and column of a cell in the occupancy grid, and the size
    of the occupancy grid. It checks if any of the nine cells centered
    on row and col are incorrect. If so, they, along with the correct
    information, are added to the dictionary. That dictionary is returned."""
    bads = {}
    for r in [row - 1, row, row + 1]:
        for c in [col - 1, col, col + 1]:
            if (r >= 0) and (r < wid) and (c >= 0) and (c < hgt):
                if (r, c) in correctInfo:
                    bads[r, c] = correctInfo[r, c]
                    del correctInfo[r, c]
    return bads


def corruptGraph(oldGraph, percWrong):
    """Takes in an old grid graph and the percentage that should
    be modified, and returns a dictionary containing the correct
    values, so they can be fixed later, and a new graph with
    modified values."""
    graph = oldGraph.copy()
    graphSize = graph.getSize()
    minC = oldGraph.getMinCost()
    maxC = oldGraph.getMaxCost()
    #print("minC =", minC, "maxC =", maxC)
    correctInfo = {}
    for i in range(percWrong * graphSize // 100):
        randNode = random.randrange(graphSize)
        (randRow, randCol) = graph.getData(randNode)
        randVal = random.randint(minC, maxC)
        correctInfo[randRow, randCol] = graph.getCellValue(randRow, randCol)
        graph.setCellValue(randRow, randCol, randVal)
    graph.graphFromGrid()
    return correctInfo, graph
