import pygame
from pathfinder import Graph, AStar

# for position checking
MARGIN = 48


class AIHANDLER:
    def __init__(self, red_player, blue_player, health_pack):
        self.red_player = red_player
        self.blue_player = blue_player
        self.health_pack = health_pack

        #initialize our nodes for pathfinding
        self.graph = Graph()
        #create A-star object
        self.a_star = AStar(self.graph.list)

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

    def run_battle(self):

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
        elif self.current_action == self.FLEEING:
            self.run_away()
            # print(self.current_action)

    def determine_movement(self):
        # length of the graph
        length = len(self.graph.list) - 1
        self.a_star.find_path(self.a_star.unvisited[0], self.a_star.unvisited[length])
        pass
            # place the player's coordinates into variables for checking
            # red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))
            #
            # blue_coordinate = ((self.blue_player.rect.centerx), (self.blue_player.rect.centery))
            #
            #
            #
            # # should we chase the player? if we are too far away then we will chase
            # if red_coordinate[0] <= blue_coordinate[0] - 100 and self.red_player.is_healthy:
            #     self.red_player.chase_opponent(self.blue_player)
            #     self.current_action = self.CHASING
            #
            # elif red_coordinate[0] >= blue_coordinate[0] + 100 and self.red_player.is_healthy:
            #     self.red_player.chase_opponent(self.blue_player)
            #     self.current_action = self.CHASING
            # # else we are in range to begin shooting
            # else:
            #     self.current_action = self.SHOOTING
            #
            #     # print(self.current_action)

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

        # cehck if the player has moved away
        self.determine_movement()

        return bullet_List

    def run_away(self):

        health_pack_coordinate = (self.health_pack.rect.centerx, self.health_pack.rect.centery)

        # place the player's coordinates into variables for checking
        red_coordinate = (self.red_player.rect.centerx, self.red_player.rect.centery)
        #
        # blue_coordinate = ((self.blue_player.rect.centerx), (self.blue_player.rect.centery))
        #
        # if blue_coordinate[0] < 500:
        #     self.red_player.move(2, 0)
        # if blue_coordinate[1] < 200:
        #     self.red_player.move(0, 2)
        # if blue_coordinate[0] > 500:
        #     self.red_player.move(-2, 0)
        # if blue_coordinate[1] > 200:
        #     self.red_player.move(0, -2)

        if red_coordinate[0] != health_pack_coordinate[0]:
            self.red_player.chase_opponent(self.health_pack)


        elif red_coordinate[1] != health_pack_coordinate[1]:
            self.red_player.chase_opponent(self.health_pack)
        if self.red_player.rect.colliderect(self.health_pack):
            self.current_action = self.RESTING
            print("picked up health pack")


        return False
