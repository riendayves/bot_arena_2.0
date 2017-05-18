import pygame

# for position checking
MARGIN = 48

class AIHANDLER:
    def __init__(self, red_player, blue_player):
        self.red_player = red_player
        self.blue_player = blue_player
        # the neural_net variable will test a primitive neural network, for now it is null
        self.neural_net = None
        self.score = 0

        #bits to determine what the player is doing
        self.CHASING = 2
        self.SHOOTING = 4
        self.FLEEING = 8

        self.current_action = 2


        #bits to determine where player is located in regards to opponent
        self.red_is_left = 2
        self.red_is_right = 4
        self.red_is_up = 8
        self.red_is_down = 16

        self.current_position = 2

    def run_battle(self):
        if self.current_action == self.CHASING:
            self.determine_movement()
        elif self.current_action == self.SHOOTING:
            self.shoot_bullets()
        elif self.current_action == self.FLEEING:
            self.run_away


    def determine_movement(self):
        # place the player's coordinates into variables for checking
        red_coordinate = ((self.red_player.rect.centerx), (self.red_player.rect.centery))

        blue_coordinate = ((self.blue_player.rect.centerx), (self.blue_player.rect.centery))


        if red_coordinate[0] + MARGIN >= blue_coordinate[0] and red_coordinate[0]  - MARGIN <= blue_coordinate[0]:
           # red player is above blue player
            if red_coordinate[1] < blue_coordinate[1] - MARGIN:
                self.current_position = self.red_is_up

            # red player is below blue player
            elif red_coordinate[1] > blue_coordinate[1] + MARGIN:
                self.current_position = self.red_is_down
        else:
            if red_coordinate[0] > blue_coordinate[0]:
                self.current_position = self.red_is_right
            elif red_coordinate[0] < blue_coordinate [0]:
                self.current_position = self.red_is_left

        # should we chase the player? if we are too far away then we will chase
        if red_coordinate[0] <= blue_coordinate[0] - 100 and self.red_player.is_healthy:
            self.red_player.chase_opponent(self.blue_player)
            self.current_action = self.CHASING

        elif red_coordinate[0] >= blue_coordinate[0] + 100 and self.red_player.is_healthy:
            self.red_player.chase_opponent(self.blue_player)
            self.current_action = self.CHASING
        #else we are in range to begin shooting
        else:
            self.current_action = self.SHOOTING

        # print(self.current_action)



    def shoot_bullets(self):
        bullet_List = pygame.sprite.Group()

        if self.current_position == self.red_is_left:
            bullet_List.add(self.red_player.shoot_right())
        elif self.current_position ==  self.red_is_right:
            bullet_List.add(self.red_player.shoot_left())
        elif self.current_position == self.red_is_up:
            bullet_List.add(self.red_player.shoot_down())
        elif self.current_position == self.red_is_down:
            bullet_List.add(self.red_player.shoot_up())

        #check if player has moved
        self.determine_movement()

        return bullet_List

    def run_away(self):
        return False





