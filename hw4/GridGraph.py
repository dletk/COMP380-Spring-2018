""" File:  GridGraph.py
Author:  Susan Fox
Date: April 2016

Contains a GridGraph that represents an occupancy grid with variable
weights on each cell, and also represents that as a weighted graph."""

# Improvements that could be made...
# -- Raising exceptions on bad inputs instead of letting normal python exceptions occur
# -- Allow for a creation method other than reading data from a file

import Graphs


class GridGraph(Graphs.WeightedListGraph):
    """A grid graph is both an occupancy grid with weighted cells, and
    a weighted graph. Each cell in the grid is a vertex in the graph,
    neighbors are adjacent in horizontal or vertical directions (not
    diagonal), and the edge weights are computed by combining neighbors'
    cell weights. It has many new methods to access the grid directly."""
    
    def __init__(self, mapFile = None, size = None):
        """Takes in two optional inputs. If neither is given, an empty
        GridGraph is created. Right now, the only other option is to
        give a filename. In that case, it reads the data to build the
        grid from a file, and then builds the graph from that."""
        self.gridOkay = False
        self.mapWidth = 0
        self.mapHeight = 0
        self.minCost = None
        self.maxCost = None
        self.startPos = None
        self.goalPos = None
        self.grid = dict()
        self.blockedLocs = set()

        if mapFile != None:
            self._readMapFile(mapFile)
            self.graphFromGrid()
        elif size != None:
            self.mapWidth = size
            self.mapHeight = size
            self.generateBlankMap()


    def _readMapFile(self, mapFile):
        """Takes in a filename for a grid-map file, and it reads in the data from the file.
        It creates a grid representation using a dictionary, where the key is the (row, col) of each
         grid cell, and the value is the weight at the cell."""
        try:
            filObj = open(mapFile, 'r')
        except:
            raise FileExistsError("ERROR READING FILE, ABORTING")
        seeking = 'grid size'

        row = 0
        for line in filObj:
            if line == "" or line.isspace() or line[0] == '#':
                continue
            elif seeking == 'grid size':   # Haven't seen first line, so it must be grid size
                [wid, hgt] = [int(s) for s in line.split()]
                self.mapWidth = wid
                self.mapHeight = hgt
                seeking = 'minmax'
            elif seeking == 'minmax':
                [minc, maxc] = [int(s) for s in line.split()]
                [minc, maxc] = [int(s) for s in line.split()]
                self.minCost = minc
                self.maxCost = maxc
                seeking = 'start'
            elif seeking == 'start':  # Have seen first line, so next must be start pos
                sPos = [int(s) for s in line.split()]
                self.startPos = sPos
                seeking = 'goal'
            elif seeking == 'goal': # Have seen first two, next must be goal pos
                gPos = [int(s) for s in line.split()]
                self.goalPos = gPos
                seeking = 'blocked'
            elif seeking == 'blocked': # Have seen all but blocked cells...
                if line[0] == '[':
                    # starting line, just keep going
                    pass
                elif line[0] == ']':
                    # final line, go on to the next
                    seeking = 'gridcells'
                else:
                    [blockRow, blockCol] = [int(s) for s in line.split()]
                    self.blockedLocs.add( (blockRow, blockCol) )
            elif seeking == 'gridcells':
                cellWeights = [int(s) for s in line.split()]
                for col in range(wid):
                    self.grid[row, col] = cellWeights[col]
                row += 1
            else:
                print("Uh-oh, should never get here")
        filObj.close()
        # self._printMaze()


    def graphFromGrid(self):
        """Assumes that the grid has been constructed before this method is called. It constructs the graph that
        this object is, from the grid. Weights between edges are computed as 1/2 the cell weight of one vertex, plus 1/2
        the cell weight of the other vertex."""
        numVerts = self.mapWidth * self.mapHeight
        vertInfo = []
        for r in range(self.mapHeight):
            for c in range(self.mapWidth):
                vertInfo.append( (r, c) )
        Graphs.WeightedListGraph.__init__(self, numVerts, vertInfo)
        for node in range(self._numVerts):
            (r, c) = self.getData(node)
            cellWgt = self.grid[r, c]
            neighInfo = self._getGridNeighbors(r, c)
            #print("For node", node, " at", (r, c))
            #print("  Neighbors are:", neighInfo)
            for neigh in neighInfo:
                if neigh > node:
                    (nr, nc) = self.getData(neigh)
                    neighWgt = self.grid[nr, nc]
                    newWgt = (cellWgt / 2) + (neighWgt / 2)
                    self.addEdge(node, neigh, newWgt)
                    #print("Adding edge from", node, "to", neigh, "with weight", newWgt)
        self.gridOkay = True


    def _getGridNeighbors(self, row, col):
        """Get the 2-4 adjacent cells, rturning their vertex numbers."""
        neighbs = []
        if row > 0:
            aboveNeigh = (row - 1) * self.mapWidth + col
            neighbs.append(aboveNeigh)
        if row < (self.mapHeight - 1):
            belowNeigh = (row + 1) * self.mapWidth + col
            neighbs.append(belowNeigh)
        if col > 0:
            leftNeigh = row * self.mapWidth + (col - 1)
            neighbs.append(leftNeigh)
        if col < (self.mapWidth - 1):
            rightNeigh = row * self.mapWidth + (col + 1)
            neighbs.append(rightNeigh)
        return neighbs



    def printWithRoute(self, route):
        """Helper to print the grid representation, mostly
        for debugging."""
        for row in range(self.mapHeight):
            rowStr = ""
            for col in range(self.mapWidth):
                val = self.grid[row, col]
                node = row * self.mapWidth + col
                if node == route[0]:
                    valStr = "S".rjust(3)
                elif node == route[-1]:
                    valStr = 'G'.rjust(3)
                elif node in route:
                    valStr = 'X'.rjust(3)
                else:
                    valStr = str(val).rjust(3)
                rowStr += valStr + " "
            print(rowStr)


    def printGrid(self):
        """Helper to print the grid representation, mostly
        for debugging."""
        for row in range(self.mapHeight):
            rowStr = ""
            for col in range(self.mapWidth):
                val = self.grid[row, col]
                valStr = str(val).rjust(3)
                rowStr += valStr + " "
            print(rowStr)

    def copy(self):
        """Makes a new copy of the GridGraph object."""
        newGG = GridGraph()
        newGG.mapWidth = self.mapWidth
        newGG.mapHeight = self.mapHeight
        newGG.minCost = self.minCost
        newGG.maxCost = self.maxCost
        newGG.grid = self.grid.copy()
        newGG.graphFromGrid()
        return newGG


    def getWidth(self):
        """Returns the width (number of columns) of the occupancy grid."""
        return self.mapWidth

    def getHeight(self):
        """Returns the height (number of rows) of the occupancy grid."""
        return self.mapHeight

    def getStart(self):
        """Returns the starting position of the occupancy grid."""
        return self.startPos

    def getGoal(self):
        """Returns the goal position of the occupancy grid."""
        return self.goalPos

    def getMinCost(self):
        """Returns the minimum cost on the grid."""
        return self.minCost

    def getMaxCost(self):
        """Returns the maximum cost on the grid."""
        return self.maxCost

    def getCellValue(self, row, col):
        """Given a row and column in the grid, it returns the
        value at that location. Should throw an exception of its own if
        the row or column is out of bounds, but not implemented yet."""
        return self.grid[row, col]

    def setCellValue(self, row, col, val):
        """Given a row and column in the grid, and a value, it changes
        that cell to have that value. Should throw an exception of its
        own, but it doesn't yet."""
        self.grid[row, col] = val
        self.gridOkay = False

    def setStart(self, newPos):
        """Takes in a new position and sets the starting position to that. No error checking right now!"""
        self.startPos = newPos

    def setGoal(self, newPos):
        """Takes in a new position and sets the goal position to that. No error checking right now!"""
        self.goalPos = newPos

    def isOkay(self):
        """Returns True if the grid graph was constructed okay, and
        False if there was a problem."""
        return self.gridOkay


    def heuristicDist(self, node1, node2):
        """Estimates the distance between any two nodes using
        city-block metric."""
        (r1, c1) = self.getData(node1)
        (r2, c2) = self.getData(node2)
        return abs(r1 - r2)+ abs(c1 - c2)


    def generateBlankMap(self):
        print("NOT IMPLEMENTED YET")



if __name__ == '__main__':
    gg = GridGraph("grid6.txt")
    print('============================')
    print("Hgt wid:", gg.getHeight(), gg.getWidth())
    print("min max:", gg.getMinCost(), gg.getMaxCost())
    print("start pos:", gg.getStart())
    print("goal pos:", gg.getGoal())
    print()
    # gg.printGrid()
    print()
    print('============================')

