import os
from copy import copy
screen_width = 1116
screen_height = 444
GRID_INCREMENT = 12

class Graph:

    def __init__(self, blueprint, step):
        # get the names from file
        self.map = blueprint
        self.step = step
        # get x co-ord
        self.node_list = []

        self.initialize_nodes()
        self.initialize_connections()

    def initialize_nodes(self):
        x = y = matrix_position_counter =  0
        for row in self.map:
            for column in row:
                if column == "N":
                    node = Node(matrix_position_counter, x, y, None)
                    #add the new node to our list
                    self.node_list.append(node)
                    # print("adding node " + str(node.name) + " x: " + str(node.x) + " y: " + str(node.y))
                x += 12
                matrix_position_counter += 1
            y += 12
            x = 0

    def initialize_connections(self):
        lol_blueprint = convert_to_lol(self.map)
        # for each node we check 8 directions (Top, Top Right, Right, etc.) for neighboring nodes to connect to.
        # if the node exists in that position we create a connection to it
        for node in self.node_list:
            x = node.x / GRID_INCREMENT
            y = node.y / GRID_INCREMENT
            direction = 1
            while direction <= 8:
                counter = 1
                is_clear = True
                # Direction starts at top above the current node and moves in a clockwise direction
                if direction == 1:
                    dy = -1
                    dx = 0
                elif direction == 2:
                    dy = -1
                    dx = 1
                elif direction == 3:
                    dy = 0
                    dx = 1
                elif direction == 4:
                    dy = 1
                    dx = 1
                elif direction == 5:
                    dy = 1
                    dx = 0
                elif direction == 6:
                    dy = 1
                    dx = -1
                elif direction == 7:
                    dy = 0
                    dx = -1
                elif direction == 8:
                    dy = -1
                    dx = -1

                #these variables help us increment through the matrix
                inc_dy = dy
                inc_dx = dx
                # we check our matrix for any wall objects ('W') that exist between our node and the neighboring
                # node. If there are no walls in between, then the path is clear and we can add the node to our list of
                # connections.
                while counter <= self.step:
                    if lol_blueprint[y + dy][x + dx] != 'W':
                        if counter != self.step:
                            dy += inc_dy
                            dx += inc_dx
                        counter += 1
                    else:
                        is_clear = False
                        break
                if is_clear:
                    node_connection_number = (y + dy) * (screen_width / GRID_INCREMENT) + ( x + dx )
                    node.connections.append(node_connection_number)
                direction += 1


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

         if(connections == None):
             return

         for i in range(len(connections) - 1):
             self.connections += [connections[i]]
             print("connection: " + connections[i])



class AStar:
    def __init__(self, node_list):
        #nodes which we know the f cost for but have not yet searched
        self.open_list = []
        #nodes whose connections we have searched
        self.closed_list = []
        #we will stick our chain of nodes that form our final path in here
        self.final_path_list = []

        #the list of all the nodes we start with in our graph
        self.unvisited = node_list

        # for now, our start node is hard-coded to be the top right node in our list
        self.start_node = None
        self.start_node_index = 2

        self.end_node = None
        self.current_node = None


    def find_path(self, end_node):
        """ Implements the A* algorithm and creates a list of nodes from the starting node to the end node

            The find_path method works in the following steps:
            1. the first node in your open_list becomes your current node whose connections you are searching
            2. remove the current node from the open_list and place it into the closed_list
            3. for each connection to the current node, find the connected node in our unvisited list and determine it's F cost
            4. once a node's F cost is determined, sort it into the open_list from lowest F cost to Highest
            5. when all the current node's connections have been checked, repeat steps 1 - 4 until your end goal is reached
            """

        # reset our lists as empty
        self.open_list = []
        self.closed_list = []
        self.final_path_list = []

        # this will be false until we reach our goal
        path_found = False

        # pull the start node out of our list
        original_node_list = copy(self.unvisited)
        self.start_node = self.unvisited[self.start_node_index]


        # we set our start node as the current node and search it's connections
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
            # loop through all of connections in our node object (ex. "190", "194", "198")
             for connection in self.current_node.connections:
                 if path_found:
                     break
                # find that corresponding node in the list of our unvisited nodes
                 for unvisited_node in self.unvisited:
                     if unvisited_node.name == connection:
                        # once we find a match, we pass it in to our determine_cost method to find its f cost
                         determine_cost(self.current_node, unvisited_node, end_node)
                         # print("unvisited Node " + str(unvisited_node.name) + " f cost: " + str(unvisited_node.f))
                        # check to see if we have reached our goal node
                         if self.end_node.name == unvisited_node.name:
                             self.end_node = unvisited_node
                             self.end_node.previous_node = self.current_node
                             path_found = True
                             break
                        # now move the node from our unvisited list to our open list since we know its f cost
                         self.transfer_open_node(unvisited_node)




             if not path_found:
                # now we move on the the first node found in our open list, this is the most likely candidate
                # based on it's f cost.
                self.current_node = self.open_list.pop(0)
                self.closed_list.append(self.current_node)

        # Once we have found the path to the end node, will will place the linked nodes into a list to make it easier
        # to read our path. this setup is not necessary as we could just access the "previous_node" field directly, but
        # for this example we will organize it into a list
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
        # delete our old lists to avoid memory leaks
        # del self.unvisited
        # del self.closed_list
        # del self.open_list

        self.unvisited = original_node_list





    def transfer_open_node(self, unvisited_node):
        """removes a node from the unvisited list and adds it to the open list"""

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


def determine_cost(current_node, unvisited_node, end_node):
    """ uses the pythagorean theorem to determine the g and h cost of an unvisited node

        we determine the distance by measuring a straight line from our current node to our starting and ending node

        g = distance from the start node
        h = guess of how far we are from the end node
        f = total estimated cost
        """
    # determine the distance based on the difference in our x and y coordinates,
    # then add on the distance we already are from the start node
    unvisited_node.g = (((current_node.x - unvisited_node.x) ** 2 + (current_node.y - unvisited_node.y) ** 2) ** .5) + current_node.g

    h = ((end_node.x - unvisited_node.x) ** 2 + (end_node.y - unvisited_node.y) ** 2) ** .5

    unvisited_node.f = unvisited_node.g + h

def convert_to_lol(node_blueprint):
    lol_blueprints = []
    for y, line in enumerate(node_blueprint):
        line_list = []
        for x, letter in enumerate(line):
            line_list.append(letter)
        # print(line_list)
        lol_blueprints.append(line_list)
    return lol_blueprints




