import os

'''
steps for pathfinding algorithm
1. parse text file of node data and store nodes in graph list
2. User enters End node (any letter from A to J)
3. check each connection of start node(or current node), adding each connected node to the "open" list
4. add the distance of each node from start node (G) with the Heuristic(H, distance from the end node) to get: G + H = F
5. add the current node to the "closed" list because it has been processed
5. find the lowest F value(or "best" node) of all the connections from step 4 and then repeat step 4 for F
6. if none of the F values are lower than the previous nodes check the connections of next lowest node
7. repeat 4 - 6 until current node is goal node

'''
class Graph:

    def __init__(self):
        # get the names from file

        #get x co-ord
        self.list = []
        self.name = ""
        self.connections = ""
        self.x = 0
        self.y = 0

        self.initializeNodes()

    def initializeNodes(self):
        nodeFile = open("nodelist.txt", 'r');

        while (nodeFile.readline()):
            self.name = nodeFile.readline()
            print(self.name)
            self.x = nodeFile.readline()
            print(self.x)
            self.y = nodeFile.readline()
            print(self.y)
            self.connections = nodeFile.readline()
            self.list.append(Node(self.name, self.x, self.y, self.connections))

class Node:
     def __init__(self, name, x, y, connections):
         self.name = name
         self.x = x
         self.y = y
         self.connections = []

         # values for A* algorithm
         self.g = 0
         self.h = 0
         self.f = 0

         for i in range(len(connections) - 1):
             self.connections += [connections[i]]
             print("connection: " + connections[i])


class Connection:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight



class NodeRecord:
    def __init__(self, start_node):
        self.node = start_node
        self.connection = None
        self.cost_so_far = 0;
        self.estimated_total_cost = Heuristic.estimate(start_node)

class AStar:
    def __init__(self, list):
        self.open_list = []
        self.closed_list = []

        self.unvisited = list

        self.start_node = None
        self.end_node = None
        self.current_node = None

    def find_path(self, start_node, end_node):

        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        node_num = 0
        counter = 0


        for connection in self.current_node.connections:
            for node in self.unvisited:
                if connection[counter].name == connection:
                    node_num = counter
                    break
                counter += 1

            build_connection(self.current_node, self.unvisited.index(node_num))


class Heuristic:
    def __init__(self):
        self.estimate = 0

    def estimate(self,node):
        pass



def build_connection(node1, node2):
    name = node1.name + node2.name
    print("Connection NAME: " + name)
    cost = 0

    # subtract the smaller x and y values from the other to determine the distance
    if (node1.x < node2.x):
        cost = node2.x - node1.x
    else:
        cost = node1.x - node2.x

    if (node1.y < node2.y):
        cost += node2.y - node1.y
    else:
        cost += node1.y - node2.y

    print("Cost: " + str(cost))

    return Connection(name, cost)



#
# def setup(start, goal):
#     calcHeuristic(start, goal)
#
#
# def calcHeuristic(start, end):
#     diffX = goal.x - start.x
#     diffY = goal.y - start.y
#     return di


