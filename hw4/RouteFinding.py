######################################
# RoutePlanning.py
#
"""Contains code that finds the shortest route between two points in a 
graph that is a topological representation of the robot's world.  May need
to be combined with a more detailed map for localization purposes"""


import LoadGraphs
import GridGraph
import GraphSearch
import DStarLite
import time



def routeFinder():
    """First step: choose a map.  
    Second step: choose an algorithm.
    Third step: loop forever getting start and goal and finding routes."""
    
    print("Which map do you wish to find routes for: Olin-Rice, Macalester Campus, or a grid graph from a file?")
    mapChoice = getUserChoice("Enter o for Olin-Rice, m for Macalester, g for grid", ['o', 'm', 'g', 'olin', 'mac', 'grid'])
    if mapChoice in ['o', 'olin']:
        currMap = LoadGraphs.olin
    elif mapChoice in ['m', 'mac']:
        currMap = LoadGraphs.macCampus
    elif mapChoice in ['g', 'grid']:
        fileName = input("Enter file name for grid map: ")
        currMap = GridGraph.GridGraph(fileName)
        if not currMap.isOkay():
            print("Grid not build correctly!")

    print("Which algorithm should we use: DFS, BFS, UCS, Dijkstra's, A*, or D*Lite?")
    print("Enter: d for DFS")
    print("       b for BFS")
    print("       u for UCS")
    print("       j for Dijkstra's")
    print("       a for A*")
    print("       l for D*Lite")
    algChoice = getUserChoice("[d, b, u, a, j, l]", 
                              {'d', 'dfs', 'b', 'bfs',
                               'u', 'ucs',
                               'j', 'dij', 'dijkstras', 
                               'a', 'a*', 'astar',
                               'l', 'lite', 'd*', 'dstar'})
    if algChoice in {'l', 'lite', 'd*', 'dstar'}:
        variant = chooseDStarVariant()
        algChoice = 'd* ' + variant
    findRoutes(currMap, algChoice)


def chooseDStarVariant():
    """Chooses between no incorrect knowledge, globally corrected knowledge,
    or iteratively "as stumbled upon" corrected knowledge."""
    print("Which knowledge option do you choose for D* Lite?")
    print("        a: No incorrect knowledge")
    print("        b: Incorrect knowledge, globally corrected")
    print("        c: Incorrect knowledge, corrected as found")
    optChoice = getUserChoice("[a, b, c]",
                              ['a', 'b', 'c'])
    return optChoice




def findRoutes(currMap, whichAlg):
    """Repeatedly asks for start and goal and finds the shortest route, using the input search algorithm"""
    numNodes = currMap.getSize()
    while True: 
        
        promptTxt = "Enter the starting location as an integer between 0 and " + str(numNodes-1) + " (or -1 to quit): "
        validInputs = [str(x) for x in range(-1, numNodes)]
        startTxt = getUserChoice(promptTxt, validInputs)
        startNode = int(startTxt)
        if startNode == -1:
            break
        
        promptTxt = "Enter the goal location as an integer between 0 and " + str(numNodes-1) + " (or -1 to quit): "
        goalTxt = getUserChoice(promptTxt, validInputs)
        goalNode = int(goalTxt)
        if goalNode == -1:
            break

        searchAlg = getSearchAlg(whichAlg)

        # Run algorithm to find the route
        if whichAlg == 'd* b' or whichAlg == 'd* c':
            searchAlg(currMap, startNode, goalNode)
        else:

            timeAndRun(searchAlg, currMap, startNode, goalNode)



def getSearchAlg(algChoice):
    """Takes in a string which describes which algorithm, and returns the correct algorithm to call."""
    if algChoice in {'d', 'dfs'}:
        return  GraphSearch.DFSRoute
    elif algChoice in {'b', 'bfs'}:
        return GraphSearch.BFSRoute
    elif algChoice in {'u', 'ucs'}:
        return GraphSearch.UCSRoute
    elif algChoice in {'j', 'dij', 'dijkstras'}:
        return GraphSearch.dijkstras
    elif algChoice in {'a', 'a*', 'astar'}:
        return GraphSearch.AStarRoute
    elif 'd*' in algChoice:
        if 'a' in algChoice:
            return DStarLite.DStarRoute
        elif 'b' in algChoice:
            return DStarLite.DStarGlobal
        else:
            return DStarLite.DStarLocal


def timeAndRun(searchAlg, graph, start, goal):
    """Takes ina  search algorithm and runs it, while timing how long it takes. Reports the time
    and the final route (if any), and prints the route."""
    t1 = time.time()
    route = searchAlg(graph, start, goal)
    t2 = time.time()
    print("Route found is:")
    print(route)
    print("Time elapsed:", t2 - t1)
    if graph.__class__.__name__ == "GridGraph":
        graph.printWithRoute(route)


def getUserChoice(prompt, validOpts):
    """Given a prompt and a list of the valid inputs the user could enter, this keeps asking until the
    user types something valid. It returns the valid input, as a string"""
    while True:
        print(prompt)
        val = input("Enter your choice: ")
        val = val.lower()
        if val in validOpts:
            return val
        print("Invalid input, try again.")
        
    


routeFinder()