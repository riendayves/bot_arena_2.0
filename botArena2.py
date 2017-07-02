import os
import pygame
import player
from player import Player
from player import Wall
from ai_handler import AIHANDLER

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

# Initialize pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# clock to keep track of movement
clock = pygame.time.Clock()

# Set up the display
pygame.display.set_caption("RED VS. BLUE!")
screen = pygame.display.set_mode((screen_width, screen_height))


# holds the sprites that make up the wall and creates the nodes for our graph
node_graph = []
node_graph = Wall.build_map()
wall_list = player.wall_list
print(len(node_graph))
print(len(wall_list))
# This object holds all of our AI code
ai = AIHANDLER(red_player, blue_player, health_pack, node_graph)

# this list is for any object that stops bullets
solid_object = pygame.sprite.Group(player_list,wall_list)
Player.set_objects(solid_object)



# shoot 2 rounds per second
pygame.time.set_timer(SHOOTING, 500)


game_running = True

# subprogram = input("Which subprogram would you like to run? Enter P for pathfinding or S for state behavior")


while game_running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            game_running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            bullet_list.add(blue_player.shoot_left())
        if e.type == SHOOTING and ai.current_action == ai.SHOOTING:
            bullet_list.add(ai.shoot_bullets())



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

    # Red Player Movement
    move = pygame.key.get_pressed()
    if move[pygame.K_a]:
        red_player.move(-2, 0)
    if move[pygame.K_d]:
        red_player.move(2, 0)
    if move[pygame.K_w]:
        red_player.move(0, -2)
    if move[pygame.K_s]:
        red_player.move(0, 2)
    if move[pygame.K_SPACE]:
        bullet_list.add(red_player.shoot_right())


    # move bullets
    for bullet in bullet_list:
        collided = bullet.update(solid_object)
        if collided:
            bullet_list.remove(bullet)



    screen.fill((0, 0, 0))
    player_list.draw(screen)
    wall_list.draw(screen)
    bullet_list.draw(screen)
    pygame.display.flip()
