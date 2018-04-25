"""##########################################################
A MapGraph, which includes the location as the data part of the graph
and provides utilities for determining straightline distance between
any two vertices in the graph, both those connected by an edge (the distance
in that case is the weight of the edge, and those not directly connected.

Susan Fox
Spring 2014
"""

from Graphs import WeightedListGraph
import math

class MapGraph(WeightedListGraph):
    """The purpose of this subclass is to require the user to provide
    the required data for each node, which must be a coordinate pair,
    either from some arbitrary global coordinate system, or based on GPS
    values"""

    def __init__(self, n, nodeData):
        """Takes the number of nodes in the graph, plus a list of
        node data.  The list MUST be the same length as the number of nodes,
        and each value must be a pair of numbers giving the location in the world
        of the related node.  If it is not, then an exception is raised."""
        if len(nodeData) != n or (not self._goodNodeData(nodeData)):
            raise(BadNodeDataException())
        else:   
            WeightedListGraph.__init__(self, n, nodeData)
            self.markerMap = {}


    def _goodNodeData(self, nodeData):
        """Takes in the list of node data and makes sure that it is appropriate. 
        Every value in the nodeData list must be either a tuple or a list, and it must
        have extactly two elements.  The two elements must be numbers.  They represent the
        (x, y) coordinate (in real-valued space) of the associated vertex."""
        for val in nodeData:
            if not (type(val) == tuple or type(val) == list):
                return False
            elif len(val) != 2:
                return False
            else:
                v1 = val[0]
                v2 = val[1]
                if not (type(v1) in [int, float] and type(v2) in [int, float]):
                    return False
        # Only if every node value is right should we return True
        return True


    def addEdge(self, node1, node2, weight = "default"):
        """takes two nodes and an optional weight and addes an edge
        to the graph.  If no weight is specified, then it uses the nodes' data
        to compute the straightline distance between the two nodes, and sets
        the weight to be that"""
        if weight == "default":
            weight = self._straightDist(node1, node2)
        WeightedListGraph.addEdge(self, node1, node2, weight)


    def addMarkerInfo(self, node, markerData):
        """Adds to a dictionary of information about markers. Each marker occurs
        at a node of the graph, so the node is the key, and the data is whatever makese sense."""
        self.markerMap[node] = markerData


    def getMarkerInfo(self, node):
        """Given a node, returns the marker data, if any, or None if none."""
        return self.markerMap.get(node, None)


    def heuristicDist(self, node1, node2):
        """Estimates the distance from any node to any other."""
        return self._straightDist(node1, node2)
    
    
    def _straightDist(self, node1, node2):
        """For estimating the straightline distance between two points for short term"""
        loc1 = self.getData(node1)
        loc2 = self.getData(node2)

        return math.hypot(loc1[0] - loc2[0], loc1[1] - loc2[1])
    


class BadNodeDataException(Exception):
    """A special exception for catching when node data is incomplete
    or badly formed"""
    

    def __str__(self):
        s = "Node data incomplete or badly formed"
        return s


# ------------------------------------------
# Function for creating a MapGraph from a file of data
# TODO: Think about whether this should be part of MapGraph itself?

def readMapFile(mapFile):
    """Takes in a filename for a occupancy-grid map graph, and it reads
    in the data from the file. It then generates the map appropriately."""
    try:
        filObj = open(mapFile, 'r')
    except:
        print("ERROR READING FILE, ABORTING")
        return
    readingIntro = True
    readingNodes = False
    readingMarkers = False
    readingEdges = False
    allData = []
    numNodes = -1
    row = -1
    graph = None
    for line in filObj:
        line = line.strip()
        lowerLine = line.lower()

        if line == "" or line[0] == '#':
            # ignore blank lines or lines that start with #
            continue
        elif readingIntro and lowerLine.startswith("number"):
            # If at the start and line starts with number, then last value is # of nodes
            words = line.split()
            numNodes = int(words[-1])
            readingIntro = False
        elif (not readingIntro) and lowerLine.startswith('nodes:'):
            # If have seen # of nodes and now see Nodes:, start reading node data
            readingNodes = True
            row = 0
        elif readingNodes and row < numNodes:
            # If reading nodes, and haven't finished (must be data for every node)
            try:
                [nodeNumStr, locStr, descr] = line.split("   ")
            except:
                print("ERROR IN FILE AT LINE: ", line, "ABORTING")
                return
            nodeNum = int(nodeNumStr)
            if nodeNum != row:
                print("ROW DOESN'T MATCH, SKIPPING")
            else:
                dataList = locStr.split()
                nodeData = [part.strip("(),") for part in dataList]
                allData.append((float(nodeData[0]), float(nodeData[1])))
            row += 1
            if row == numNodes:
                # If reading nodes, and should be done, then go on
                readingNodes = False
                graph = MapGraph(numNodes, allData)
        elif (not readingNodes) and lowerLine.startswith('markers:'):
            # If there are markers, then start reading them
            readingMarkers = True
        elif (not readingNodes) and lowerLine.startswith('edges:'):
            # If you see "Edges:", then start reading edges
            readingMarkers = False
            readingEdges = True
        elif readingMarkers:
            # If reading a marker, data is node and heading facing marker
            markerData = line.split()
            node = int(markerData[0])
            heading = float(markerData[1])
            graph.addMarkerInfo(node, heading)
        elif readingEdges:
            # If reading edges, then data is pair of nodes, add edge
            [fromNode, toNode] = [int(x) for x in line.split()]
            graph.addEdge(fromNode, toNode)
        else:
            print("Shouldn't get here", line)
    return graph

