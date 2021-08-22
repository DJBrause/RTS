import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        self.coord_x, self.coord_y = x, y
        self.initial_coord_x, self.initial_coord_y = self.coord_x, self.coord_y
        self.target = target
        self.speed = 10
        self.rotated = False
        super().__init__()
        self.og_image = pygame.image.load(r'graphics/laser.png').convert_alpha()
        self.explosion_1 = pygame.image.load(r'graphics/explosion1.png').convert_alpha()
        self.explosion_2 = pygame.image.load(r'graphics/explosion2.png').convert_alpha()
        self.explosion_3 = pygame.image.load(r'graphics/explosion3.png').convert_alpha()
        self.explosion_4 = pygame.image.load(r'graphics/explosion2.png').convert_alpha()
        self.explosion_5 = pygame.image.load(r'graphics/explosion1.png').convert_alpha()
        self.explosion = [self.explosion_1, self.explosion_2, self.explosion_3, self.explosion_3, self.explosion_4,
                          self.explosion_5]
        self.explosion_index = 0
        self.explosion_end = False
        self.distance = (
                    math.sqrt((self.coord_x - self.target[0]) ** 2 + (self.coord_y - self.target[1]) ** 2) / self.speed)
        self.distance = int(self.distance)
        self.image = pygame.transform.scale(self.og_image, (8, 8))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def explosion_animation(self):
        self.explosion_index += 0.2
        if self.explosion_index >= len(self.explosion):
            self.explosion_end = True
            self.explosion_index = 0
        self.image = self.explosion[int(self.explosion_index)]

    def transformed_image(self):
        self.image = pygame.transform.scale(self.og_image, (8, 8))
        return self.image

    def move(self):
        if self.distance > 0:
            radians = math.atan2(self.target[1] - self.coord_y , self.target[0] - self.coord_x)
            mov_x = math.cos(radians) * self.speed
            mov_y = math.sin(radians) * self.speed
            self.distance -= 1
            self.coord_x += mov_x
            self.coord_y += mov_y
        elif self.distance <= 0 and self.explosion_end is False:
            self.explosion_animation()
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def rotate(self):
        waypoint_x, waypoint_y = self.target[0], self.target[1]
        rel_x, rel_y = waypoint_x - (self.rect.x + 51), waypoint_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 270

        self.image = pygame.transform.rotate(self.image, int(angle))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def update(self):
        if self.rotated is False:
            self.rotate()
            self.rotated = True
        self.move()

