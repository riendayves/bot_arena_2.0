import pygame


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
                return True;

        return False

