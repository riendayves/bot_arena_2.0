import os


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
            self.name = nodeFile.readline().rstrip('\n')
            print(self.name)
            self.x = int(nodeFile.readline().rstrip())
            print(self.x)
            self.y = int(nodeFile.readline().rstrip())
            print(self.y)
            self.connections = nodeFile.readline()
            self.list.append(Node(self.name, self.x, self.y, self.connections))

class Node:
     def __init__(self, name, x, y, connections):
         self.name = name
         self.x = x
         self.y = y
         self.connections = []

         #this variable keeps track of which node preceded it in our path
         previous_node = None

         # value for A* algorithm
         self.f = 0
         self.g = 0

         for i in range(len(connections) - 1):
             self.connections += [connections[i]]
             print("connection: " + connections[i])


class Connection:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight





class AStar:
    def __init__(self, list):
        #nodes which we know the f cost for but have not yet searched
        self.open_list = []
        #nodes whose connections we have searched
        self.closed_list = []
        #we will stick our chain of nodes that form our final path in here
        self.final_path_list = []

        #the list of all the nodes we start with in our graph
        self.unvisited = list

        # for now, our start node is hard-coded to be node "A"
        self.start_node = self.unvisited[0]
        self.end_node = None
        self.current_node = None

    ''' The find_path method works in the following steps:
    1. the first node in your open_list becomes your current node whose connections you are searching
    2. remove the current node from the open_list and place it into the closed_list
    3. for each connection to the current node, find the connected node in our unvisited list and determine it's F cost
    4. once a node's F cost is determined, sort it into the open_list from lowest F cost to Highest
    5. when all the current node's connections have been checked, repeat steps 1 - 4 until your end goal is reached
    '''
    def find_path(self, end_node):
        # this will be false until we reach our goal
        path_found = False

        # we start of having our start node be the current node and search it's connections
        self.closed_list.append(self.start_node)
        self.current_node = self.start_node

        # set our class's end node to match what was passed in from aihandler
        self.end_node = end_node

        # if we happen to already be at our end node, put our start node as the only one in the list and return
        if self.start_node.name == self.end_node.name:
            self.final_path_list.append(self.start_node)
            return

        #remove the starting node from our list
        self.unvisited.remove(self.start_node)

        while not path_found:
            # loop through all of connections in our node object (ex. "B", "C", "D")
             for connection in self.current_node.connections:
                # find that corresponding node in the list of our unvisited nodes
                 for unvisited_node in self.unvisited:
                     if unvisited_node.name == connection:
                        # once we find a match, we pass it in to our determine_cost method to find its f cost
                         determine_cost(self.current_node, unvisited_node, end_node)
                         print("unvisited Node " + unvisited_node.name + " f cost: " + str(unvisited_node.f))
                        # now move the node from our unvisited list to our open list since we know its f cost
                         self.transfer_open_node(unvisited_node)
                         # check to see if we have reached our goal node
                         if self.end_node.name == unvisited_node.name:
                             self.end_node = unvisited_node
                             path_found = True
                         break

             if not path_found:
                # now we move on the the first node found in our open list, this is the most likely candidate
                # based on it's f cost.
                self.current_node = self.open_list.pop(0)
                self.closed_list.append(self.current_node)

        # Once we have found the path to the end node, will will place the linked nodes into a list to make it easier
        # to read our path. this setup is not necessary as we could just access the "previous_node" field directly, but
        # for this example we will organize it into a list

        # our next start node will be our current end_node for the next time we find a path
        next_start_node = self.end_node
        while self.end_node.name != self.start_node.name:

            # insert the current node of our chain into the front of the list
            self.final_path_list.insert(0,self.end_node)

            # if our current node does not have a previous node to point to, exit the loop
            if not self.end_node.previous_node:
                break

            # move to the previous connected node
            self.end_node = self.end_node.previous_node

        # finally insert our start_node
        self.final_path_list.insert(0, self.start_node)

        # set our new start node for the next time we find a path
        self.start_node = next_start_node




    def transfer_open_node(self, unvisited_node):

        # first remove the node from the unvisited list
        self.unvisited.remove(unvisited_node)

        # link our node to the previous node we are coming from so we can keep track of our path
        unvisited_node.previous_node = self.current_node

        # now check if our open_list is empty, in which case we place it in the front
        if not self.open_list:
            self.open_list.append(unvisited_node)
            return

        #now we iterate through our list and place our unvisited node in based on it's f cost
        i = 0
        inserted = False
        for current_node in self.open_list:
            if unvisited_node.f < current_node.f:
                self.open_list.insert(i,unvisited_node)
                inserted = True
                break
            else:
                i += 1

        # if our node's f cost is the largest, insert it at the back
        if not inserted:
            self.open_list.append(unvisited_node)

# we will use the pythagorean theorem to determine the g and h cost of our node
# g = distance from the start node
# h = guess of how far we are from the end node
# f = total estimated cost
def determine_cost(current_node, unvisited_node, end_node):
    # determine the distance based on the difference in our x and y coordinates, then add on the distance we already are from the start node
    unvisited_node.g = (((current_node.x - unvisited_node.x) ** 2 + (current_node.y - unvisited_node.y) ** 2) ** .5) + current_node.g

    h = ((end_node.x - unvisited_node.x) ** 2 + (end_node.y - unvisited_node.y) ** 2) ** .5

    unvisited_node.f = unvisited_node.g + h




