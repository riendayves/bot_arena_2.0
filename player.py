import pygame
from random import randint

wall_list = pygame.sprite.Group()



class Player(pygame.sprite.Sprite):

    solid_object = pygame.sprite.Group()

    @staticmethod
    def set_objects(objects):
        solid_object = objects

    def __init__(self, player_id):
        super(Player, self).__init__()
        self.image = pygame.Surface([16, 16])
        self.rect = pygame.Rect(0, 0, 16, 16)


        # set the color and position of each player
        if player_id == 1:
            self.image.fill((255, 0, 0))
            self.rect.x = 100
            self.rect.y = 256
            self.player_id = 1
        elif player_id == 2:
            self.image.fill((0, 0, 255))
            self.rect.x = 900
            self.rect.y = 256
            self.player_id = 2
        elif player_id == 3:
            self.image.fill((255, 255, 255))
            self.rect.x = randint(20, 300)
            self.rect.y = randint(20, 300)

        #game variables
        self.score = 0
        self.hit_points = 100
        self.ammo = 100

        # variables for A.I. behavior
        self.healthy = 1.0
        self.is_healthy = True
        self.winning = False

    def set_healthy(self):
        self.healthy = self.hit_points / float(100)

    def is_player_healthy(self):
        return self.healthy > 0.5


    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy


        # If you collide with an object, move out based on velocity
        for wall in wall_list:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                elif dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                elif dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                elif dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom





    def chase_opponent(self, opponent):
        # left and right movement
        if opponent.rect.x < self.rect.x:
            self.move(-2,0)
        elif opponent.rect.x > self.rect.x:
            self.move(2, 0)

        #up and down
        if opponent.rect.y < self.rect.y:
            self.move(0, -2)
        elif opponent.rect.y > self.rect.y:
            self.move(0, 2)

    def run_away(self, coordinate):
        self.move(-(coordinate[0] % 6), -(coordinate[1] % 4))
        print(-coordinate[0] % 4)

    def shoot_up(self):
        bullet = Bullet(1)
        bullet.rect.x = self.rect.centerx
        bullet.rect.y = self.rect.y - 8
        return bullet


    def shoot_down(self):
        bullet = Bullet(2)
        bullet.rect.x = self.rect.centerx
        bullet.rect.y = self.rect.y + 16
        return bullet

    def shoot_left(self):
        bullet = Bullet(3)
        bullet.rect.x = self.rect.x - 16
        bullet.rect.y = self.rect.centery
        return bullet

    def shoot_right(self):
        bullet = Bullet(4)
        bullet.rect.x = self.rect.x + 16
        bullet.rect.y = self.rect.centery
        return bullet



    def getColor(self):
        if self.player_id == 1:
            return (255, 0, 0)
        elif self.player_id == 2:
            return (0, 0, 255)




class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, length, width):
        super(Wall, self).__init__()
        self.image = pygame.Surface([length, width])
        self.rect = pygame.Rect(x, y, length, width)
        self.image.fill((255, 255, 255))

        self.rect.x = x
        self.rect.y = y

    @staticmethod
    def build_walls():
        # Holds the arena layout using an array of strings.
        # W = 12 X 12 brick
        # S = spacing, moves map down by 24 pixels
        # B = 84 X 12 wall
        # and so on...

        level = [
            "LR                                                                                          L",
            " S                                                                                           ",
            "                                                                                             ",
            "                                                                                             ",
            "                               WWWWWWWWWWWWWWWWWWWWWWWWWW                                    ",
            "                               W                        W                                    ",
            "                                                                                             ",
            "                                                                                             ",
            "                                            B                                                ",
            "                                                                                             ",
            "  S                                                                                          ",
            "                               W                        W                                    ",
            "                               WWWWWWWWWWWWWWWWWWWWWWWWWW                                    ",
            " V                                                                                          ",
            " R ",
        ]

        # Parse the level string above.
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    wall = Wall(x, y, 12, 12)
                if col == "R":
                    wall = Wall(x, y, 1104, 12)
                if col == "L":
                    wall = Wall(x, y, 12, 444)
                if col == "S":
                    y += 72
                    continue
                if col == "V":
                    y += 120
                if col == "B":
                    wall = Wall(x, y, 12, 84)
                wall_list.add(wall)

                x += 12
            y += 12
            x = 0

        return wall_list


green = (0,255,0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction):
        # Call the parent class (Sprite) constructor
        super(Bullet,self).__init__()

        self.image = pygame.Surface([2, 6])
        self.image.fill(green)
        # for shooting directions: 1 = up, 2 = down, 3 = left, 4 = right
        self.direction = direction

        self.rect = pygame.Rect(0, 0, 2, 6)

    def move_up(self):
        self.rect.y -= 5

    def move_down(self):
        self.rect.y += 5

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5


    def update(self, wall_list):

        movement = {1 : self.move_up, 2 : self.move_down, 3 : self.move_left, 4 : self.move_right}

        movement[self.direction]()

        return self.check_collision(wall_list)

    def check_collision(self, wall_list):

        for wall in wall_list:
            if self.rect.colliderect(wall):
                # print("Bullet colliding")
                if isinstance(wall, Player):
                    wall.hit_points -= 10
                    wall.set_healthy()
                    print(wall.hit_points)
                    print(wall.healthy)
                    print(wall.is_player_healthy())
                return True

        return False