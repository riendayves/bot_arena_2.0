import os
import pygame
import player
import thread
from player import Player
from player import Wall
from ai_handler import AIHANDLER


'''
*********************************************************
*                        BOT ARENA 2.0                  *
*                                                       *
*********************************************************

Intro:
This program demonstrates basic topics in A.I. including pathfinding and state machines.
In order to run the program you must first install python2.7 and the pygame module.
Follow the instructions at this link. https://github.com/sai-byui/resources/blob/master/pygame-files/Python-links.md
Once you have installed the necessary packages you can run the program

Files:
botArena2.py - the main driver file of game, takes care of drawing sprites and event handling. Runs the main game loop
player.py - contains Player, Wall, and Bullet classes
ai_handler.py - holds all of the code for switching between state behaviors for the red rectangle
pathfinder.py - contains Graph, Node, and AStar classes for pathfinding.

Subprograms:
pathfinding - The user enters a x and y coordinate for the A* algorithm to find a path to. Once the path is found the
red rectangle moves through the maze to that location. The console will print out F costs of each node that is checked
in the path, allowing the user to follow the nodes from start to finish

Written by the BYU-I society for Artificial Intelligence, 2017
'''

# this determines which aspect of our AI handler we will run
SUBPROGRAM = None

def get_node_coordinates():
    invalid = True
    while invalid:
        try:
            node_x_coordinate = int(raw_input("Enter a x coordinate for the Red rectangle to find (number between 24 - 1075)"))
            node_y_coordinate = int(raw_input("Enter a y coordinate (number between 24 - 420)"))
        except ValueError:
            print("invalid input, please enter numbers only within the range given")
            continue
        if 24 <= node_x_coordinate <= 1075 and 24 <= node_y_coordinate <= 420:
            invalid = False
        else:
            print("Number out of bounds, please enter numbers within the range given")

    ai.find_node(node_x_coordinate, node_y_coordinate)


# set measurements for the screen size
screen_height = 444
screen_width = 1116

# event values for handling during gameplay
SHOOTING = pygame.USEREVENT + 1

player_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

# create players and add them to the game
red_player = Player(1)
blue_player = Player(2)
health_pack = Player(3)
player_list.add(red_player, blue_player, health_pack)

# set up pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# clock to track events
clock = pygame.time.Clock()

# Set up the display
pygame.display.set_caption("RED VS. BLUE!")
screen = pygame.display.set_mode((screen_width, screen_height))


# holds the sprites that make up the wall and creates the nodes for our graph
node_graph = []
node_graph = Wall.build_map()
wall_list = player.wall_list

# This object holds all of our AI code
ai = AIHANDLER(red_player, blue_player, health_pack, node_graph)

# this list is for any object that stops bullets
solid_object = pygame.sprite.Group(player_list,wall_list)
Player.set_objects(solid_object)



# shoot 2 rounds per second
pygame.time.set_timer(SHOOTING, 500)


game_running = True
getting_coordinates = False

SUBPROGRAM = raw_input("Which subprogram would you like to run? Enter P for pathfinding or S for state behavior")
if SUBPROGRAM.upper() == "P":
    SUBPROGRAM = "pathfinding"
    ai.subprogram = SUBPROGRAM
    get_node_coordinates()
elif SUBPROGRAM.upper() == "S":
    SUBPROGRAM = "states"
    ai.subprogram = SUBPROGRAM
else:
    print("Invalid input, running pathfinding subprogram")
    get_node_coordinates()


while game_running:

    clock.tick(60)

    #this determines if our red bot is still moving towards the end node
    finding_path = ai.finding_path
    getting_coordinates = ai.getting_coordinates

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            game_running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            bullet_list.add(blue_player.shoot_left())
        if e.type == SHOOTING and ai.current_action == ai.SHOOTING:
            bullet_list.add(ai.shoot_bullets())


    if not finding_path and not getting_coordinates and SUBPROGRAM == "pathfinding":
        ai.getting_coordinates = True
        thread.start_new_thread(get_node_coordinates, ())


    # handle ai actions
    ai.run_battle()




    # Blue Player Movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        blue_player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        blue_player.move(2, 0)
    if key[pygame.K_UP]:
        blue_player.move(0, -2)
    if key[pygame.K_DOWN]:
        blue_player.move(0, 2)

    # Blue player shooting buttons
    move = pygame.key.get_pressed()
    if move[pygame.K_a]:
        bullet_list.add(blue_player.shoot_left())
    if move[pygame.K_d]:
        bullet_list.add(blue_player.shoot_right())
    if move[pygame.K_w]:
        bullet_list.add(blue_player.shoot_up())
    if move[pygame.K_s]:
        bullet_list.add(blue_player.shoot_down())
    if move[pygame.K_SPACE]:
        bullet_list.add(red_player.shoot_right())


    # move bullets
    for bullet in bullet_list:
        collided = bullet.update(solid_object)
        if collided:
            bullet_list.remove(bullet)
    if len(bullet_list) > 200:
        print("TOO Many bullets")



    screen.fill((0, 0, 0))
    player_list.draw(screen)
    wall_list.draw(screen)
    bullet_list.draw(screen)
    pygame.display.flip()



