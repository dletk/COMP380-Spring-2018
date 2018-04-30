###############################################
# Breadth-First and Depth-First Search on a graph
# Susan Fox
# Spring 2014
# Spring 2016: This Homework version also contains working
#              implementations of UCS and A*


from FoxQueue import Queue, PriorityQueue
from FoxStack import Stack


# ---------------------------------------------------------------
def BFSRoute(graph, startVert, goalVert):
    """ This algorithm searches a graph using breadth-first search
    looking for a path from some start vertex to some goal vertex
    It uses a queue to store the indices of vertices that it still
    needs to examine."""

    if startVert == goalVert:
        return []
    q = Queue()
    q.insert(startVert)
    visited = {startVert}
    pred = {startVert: None}
    while not q.isEmpty():
        nextVert = q.firstElement()
        q.delete()
        neighbors = graph.getNeighbors(nextVert)
        for n in neighbors:
            if type(n) != int:
                # weighted graph, strip and ignore weights
                n = n[0]
            if n not in visited:
                visited.add(n)
                pred[n] = nextVert
                if n != goalVert:
                    q.insert(n)
                else:
                    return reconstructPath(startVert, goalVert, pred)
    return "NO PATH"






# ---------------------------------------------------------------
def DFSRoute(graph, startVert, goalVert):
    """This algorithm searches a graph using depth-first search
    looking for a path from some start vertex to some goal vertex
    It uses a stack to store the indices of vertices that it still
    needs to examine."""

    if startVert == goalVert:
        return []
    s = Stack()
    s.push(startVert)
    visited = {startVert}
    pred = {startVert: None}
    while not s.isEmpty():
        nextVert = s.top()
        s.pop()
        neighbors = graph.getNeighbors(nextVert)
        for n in neighbors:
            if type(n) != int:
                # weighted graph, strip and ignore weights
                n = n[0]
            if n not in visited:
                visited.add(n)
                pred[n] = nextVert
                if n != goalVert:
                    s.push(n)
                else:
                    return reconstructPath(startVert, goalVert, pred)
    return "NO PATH"

# ---------------------------------------------------------------
def UCSRoute(graph, startVert, goalVert):
    """This algorithm search a graph using Uniform Cost Search algorithm"""
    num_q_nodes_removed = 0
    max_queue_size = -1
    if startVert == goalVert:
        return []
    q = PriorityQueue()
    q.insert(0, (startVert, None))
    visited = set()
    pred = {}
    while not q.isEmpty():
        weight, (nextVert, predNextvert) = q.firstElement()
        if q.getSize() > max_queue_size:
            max_queue_size = q.getSize()
        q.delete()
        num_q_nodes_removed += 1
        if nextVert in visited:
            pass
        else:
            visited.add(nextVert)
            pred[nextVert] = predNextvert
            if nextVert == goalVert:
                print("====> UCS number of visited: ", len(visited))
                print("====> UCS number of nodes removed from queue: ", num_q_nodes_removed)
                print("====> UCS max queue size: ", max_queue_size)
                return reconstructPath(startVert, goalVert, pred)
            neighbors = graph.getNeighbors(nextVert)
            for n in neighbors:
                if type(n) != int:
                    # NOTICE: From getNeighbors, the order is (vert, weight)
                    weight_n = n[1]
                    n = n[0]
                if n not in visited:
                    q.insert(weight + weight_n, (n, nextVert))
    return "NO PATH"

def AStarRoute(graph, startVert, goalVert):
    """This algorithm search a graph using A star Search algorithm"""
    num_q_nodes_removed = 0
    max_queue_size = -1
    if startVert == goalVert:
        return []
    q = PriorityQueue()
    q.insert(0, (startVert, None))
    visited = set()
    pred = {}
    while not q.isEmpty():
        weight, (nextVert, predNextvert) = q.firstElement()
        # The weight in PriorityQueue also contains the heuristicDist, not the actual weight
        # Calculate the actual weight
        weight = weight - graph.heuristicDist(nextVert, goalVert)
        if q.getSize() > max_queue_size:
            max_queue_size = q.getSize()
        q.delete()
        num_q_nodes_removed += 1
        if nextVert in visited:
            pass
        else:
            visited.add(nextVert)
            pred[nextVert] = predNextvert
            if nextVert == goalVert:
                print("===> Astar number of visited: ", len(visited))
                print("===> Number of nodes removed from queue: ", num_q_nodes_removed)
                print("===> Astart max queue size: ", max_queue_size)
                return reconstructPath(startVert, goalVert, pred)
            neighbors = graph.getNeighbors(nextVert)
            for n in neighbors:
                if type(n) != int:
                    # NOTICE: From getNeighbors, the order is (vert, weight)
                    weight_n = n[1]
                    n = n[0]
                if n not in visited:
                    q.insert(weight + weight_n + graph.heuristicDist(n, goalVert), (n, nextVert))
    return "NO PATH"

# ---------------------------------------------------------------
def dijkstras(graph, startVert, goalVert):
    """ This algorithm searches a graph using Dijkstras algorithm to find
    the shortest path from every point to a goal point (actually
    searches from goal to every point, but it's the same thing.
    It uses a priority queue to store the indices of vertices that it still
    needs to examine.
    It returns the best path frmo startVert to goalVert, but otherwise
    startVert does not play into the search."""
    num_q_nodes_removed = 0
    max_queue_size = -1
    if startVert == goalVert:
        return []
    q = PriorityQueue()
    visited = set()
    pred = {}
    cost = {}
    for vert in graph.getVertices():
        cost[vert] = 1000.0
        pred[vert] = None
        q.insert(cost[vert], vert)
    visited.add(goalVert)
    cost[goalVert] = 0
    q.update(cost[goalVert], goalVert)
    while not q.isEmpty():
        (nextCTG, nextVert) = q.firstElement()
        if q.getSize() > max_queue_size:
            max_queue_size = q.getSize()
        q.delete()
        num_q_nodes_removed += 1
        visited.add(nextVert)
        # print("--------------")
        # print("Popping", nextVert, nextCTG)
        neighbors = graph.getNeighbors(nextVert)
        for n in neighbors:
            neighNode = n[0]
            edgeCost = n[1]
            if neighNode not in visited and\
               cost[neighNode] > nextCTG + edgeCost:
                # print("Node", neighNode, "From", nextVert)
                # print("New cost =", nextCTG + edgeCost)
                cost[neighNode] = nextCTG + edgeCost
                pred[neighNode] = nextVert
                q.update( cost[neighNode], neighNode )
    # This part is finding the best path from all nodes to the goal. Not necessary
    # for vert in graph.getVertices():
    #     bestPath = reconstructPath(goalVert, vert, pred)
    #     bestPath.reverse()
    #     print("Best path from ", vert, "to", goalVert, "is", bestPath)
    print("====> Dijkstra number of nodes visited: ", len(visited))
    print("====> Dijkstra number of nodes removed: ", num_q_nodes_removed)
    print("====> Dijkstra max size of queue: ", max_queue_size)
    finalPath = reconstructPath(goalVert, startVert, pred)
    finalPath.reverse()
    return finalPath



# ---------------------------------------------------------------
# This function is used by all the algorithms in this file to build
# the path after the fact

def reconstructPath(startVert, goalVert, preds):
    """ Given the start vertex and goal vertex, and the table of
    predecessors found during the search, this will reconstruct the path
    from start to goal"""

    path = [goalVert]
    p = preds[goalVert]
    while p != None:
        path.insert(0, p)
        p = preds[p]
    return path
