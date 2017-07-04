import pygame
from pathfinder import Graph, AStar
from copy import copy
import player


# for position checking
MARGIN = 48

GRID_INCREMENT = player.GRID_INCREMENT
NODE_STEP = player.node_step


class AIHANDLER:
    def __init__(self, red_player, blue_player, health_pack, node_graph):
        self.red_player = red_player
        self.blue_player = blue_player
        self.health_pack = health_pack


        # the neural_net variable will test a primitive neural network, for now it is null
        self.neural_net = None
        self.score = 0

        # bits to determine what the player is doing
        self.CHASING = 2
        self.SHOOTING = 4
        self.FLEEING = 8
        self.RESTING = 16

        self.current_action = 2

        # bits to determine where player is located in regards to opponent
        self.red_is_left = 2
        self.red_is_right = 4
        self.red_is_up = 8
        self.red_is_down = 16

        self.current_position = 2

        self.node_graph = node_graph
        self.a_star = AStar()

        self.finding_path = False
        self.getting_coordinates = True

        self.subprogram = None


    def run_battle(self):

       if self.subprogram == "states":
            if self.current_action == self.RESTING:
                return
            # first we check if the agent is healthy, if not we run away
            if not self.red_player.is_player_healthy():
                self.current_action = self.FLEEING

            if self.current_action == self.CHASING:
                 self.determine_movement()
            # check the agent's current state and act accordingly
            elif self.current_action == self.SHOOTING:
                self.shoot_bullets()
                self.determine_movement()
            elif self.current_action == self.FLEEING:
                self.run_away()

                # print(self.current_action)
       elif self.subprogram == "pathfinding":
           self.determine_movement()

    def determine_movement(self):
        if self.subprogram == "pathfinding":
            # if our path list is currently empty do nothing
            if not self.a_star.final_path_list:
                self.finding_path = False
                return

            # find the next node in our path for the red_player to travel to
            next_node_coordinate = ((self.a_star.final_path_list[0].x), (self.a_star.final_path_list[0].y))
            # place the player's coordinates into variables for checking
            red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))


            # until we reach the node keep moving towards it
            if 2 <= abs(red_coordinate[0] - next_node_coordinate[0]) or 2 <= abs(red_coordinate[1] - next_node_coordinate[1]):
                self.red_player.move_to_next_node(next_node_coordinate)
            else:
                # then remove the current node so we can move toward the next node
                print("popping Node #: " + str(self.a_star.final_path_list[0].name))
                self.a_star.final_path_list.pop(0)


        if self.subprogram == "states":
            turning_around = False
            blue_coordinate = ((self.blue_player.rect.centerx), (self.blue_player.rect.centery))
            red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))

            # should we chase the player? if we are too far away then we will chase
            if (100 <= abs(blue_coordinate[0] - red_coordinate[0]) or 100 <= abs(blue_coordinate[0] - red_coordinate[0]))\
                and not self.finding_path:
                self.find_node(blue_coordinate[0], blue_coordinate[1])
                self.blue_player.previous_x = blue_coordinate[0]
                self.blue_player.previous_y = blue_coordinate[1]
                self.current_action = self.CHASING
            elif 300 <= abs(self.blue_player.previous_x - blue_coordinate[0]) or\
                100 <= abs(self.blue_player.previous_y - blue_coordinate[1]):
                self.change_course(blue_coordinate)
            elif 5 > abs(blue_coordinate[0] - red_coordinate[0]) or 5 > abs(blue_coordinate[1] - red_coordinate[1]):
                self.move_freely(blue_coordinate)
            else:
                self.current_action = self.SHOOTING




    def move_through_path(self):
        # if our path list is currently empty do nothing
        if not self.a_star.final_path_list:
            self.finding_path = False
            return

        # find the next node in our path for the red_player to travel to
        next_node_coordinate = ((self.a_star.final_path_list[0].x), (self.a_star.final_path_list[0].y))
        # place the player's coordinates into variables for checking
        red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))

        # until we reach the node keep moving towards it
        if 1 <= abs(red_coordinate[0] - next_node_coordinate[0]) or 1 <= abs(red_coordinate[1] - next_node_coordinate[1]):
            self.red_player.move_to_next_node(next_node_coordinate)
        else:
            # then remove the current node so we can move toward the next node
            if self.subprogram == "pathfinding":
                print("popping Node #: " + str(self.a_star.final_path_list[0].name))
            self.a_star.final_path_list.pop(0)

    def change_course(self, blue_coordinate):
        if self.a_star.final_path_list:
            self.a_star.start_node_index = self.find_node_index(self.a_star.final_path_list[0])
        del self.a_star.final_path_list
        self.find_node(blue_coordinate[0], blue_coordinate[1])
        self.blue_player.previous_x = blue_coordinate[0]
        self.blue_player.previous_y = blue_coordinate[1]

    def shoot_bullets(self):
        bullet_List = pygame.sprite.Group()

        red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))

        blue_coordinate = ((self.blue_player.rect.centerx), (self.blue_player.rect.centery))

        if red_coordinate[0] + MARGIN >= blue_coordinate[0] and red_coordinate[0] - MARGIN <= blue_coordinate[0]:
            # red player is above blue player
            if red_coordinate[1] < blue_coordinate[1] - MARGIN:
                self.current_position = self.red_is_up

            # red player is below blue player
            elif red_coordinate[1] > blue_coordinate[1] + MARGIN:
                self.current_position = self.red_is_down
        else:
            if red_coordinate[0] > blue_coordinate[0]:
                self.current_position = self.red_is_right
            elif red_coordinate[0] < blue_coordinate[0]:
                self.current_position = self.red_is_left

        if self.current_position == self.red_is_left:
            bullet_List.add(self.red_player.shoot_right())
        elif self.current_position == self.red_is_right:
            bullet_List.add(self.red_player.shoot_left())
        elif self.current_position == self.red_is_up:
            bullet_List.add(self.red_player.shoot_down())
        elif self.current_position == self.red_is_down:
            bullet_List.add(self.red_player.shoot_up())

        if self.finding_path:
            self.move_through_path()




        return bullet_List

    def run_away(self):

        health_pack_coordinate = (self.health_pack.rect.centerx, self.health_pack.rect.centery)
        red_coordinate = (self.red_player.rect.centerx, self.red_player.rect.centery)

        if not self.finding_path:
            self.find_node(health_pack_coordinate[0], health_pack_coordinate[1])

        if GRID_INCREMENT * NODE_STEP >= abs(red_coordinate[0] - health_pack_coordinate[0]) and \
           GRID_INCREMENT * NODE_STEP >= abs(red_coordinate[1] - health_pack_coordinate[1]):
            self.move_freely(health_pack_coordinate)
        elif self.finding_path:
            self.move_through_path()

        if self.red_player.rect.colliderect(self.health_pack):
            self.red_player.hit_points += 100
            self.red_player.set_healthy()
            print("picked up health pack")
            self.current_action = self.CHASING

    def move_freely(self, target):
        self.red_player.chase_object(target)





        return False


    def find_node(self, x_coordinate, y_coordinate):
        # we make a deep copy of our graph because we will be removing nodes when we run the A*
        # and we don't want it to change our original graph
        self.a_star.unvisited = copy(self.node_graph)
        search_index = 0
        if x_coordinate > 550 and y_coordinate > 220:
            search_index = len(self.node_graph) / 2
        # for each node in our graph, we check the coordinates to see if it's "close enough" to our user coordinates
        for node in self.node_graph[search_index:]:
            if GRID_INCREMENT * NODE_STEP >= abs(node.x - x_coordinate) and GRID_INCREMENT * NODE_STEP >= abs(node.y - y_coordinate):
                print("matched coordinates with node# " + str(node.name))
                # use the matched node as the end node which we find the path to
                self.a_star.find_path(node)
                # our next start node will be our current end_node for the next time we find a path
                self.a_star.start_node_index = self.node_graph.index(node)
                self.finding_path = True
                self.getting_coordinates = False
                break

    def find_node_index(self, start_node):
        node_name = start_node.name
        for node in self.node_graph:
            if node.name == node_name:
                return self.node_graph.index(node)

    def getAction(self):
        new_action = input("ENTER COMMAND: ")

        if new_action.upper() == "CHASE":
            self.current_action = self.CHASING





