import pygame
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.moving_to_wp = False
        self.active_waypoint = None
        self.coord_x = x
        self.coord_y = y
        self.active = False
        self.ship_collision = False
        self.list_of_ships = []
        self.waypoints = []
        super().__init__()
        self.og_image = pygame.image.load(r'graphics\fighter.png').convert_alpha()
        self.image = pygame.transform.scale(self.og_image, (16, 16))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def test(self):
        print(f"len list = {len(self.waypoints)}")

    def transformed_image(self):
        self.image = pygame.transform.scale(self.og_image, (16, 16))
        return self.image

    '''Sets the ship into active state where it can react to orders.'''
    def activate_ship(self):
        self.active = True
        if self.moving_to_wp is False:
            self.active_waypoint = (self.coord_x, self.coord_y)

    def deactivate_ship(self):
        self.active = False

    def new_waypoint(self, wp):
        self.waypoints = []
        self.active_waypoint = wp
        self.rotate()

    def new_waypoint_keep_list(self, wp):
        self.active_waypoint = wp
        self.rotate()

    def rotate(self):
        if self.active_waypoint is not None:
            waypoint_x, waypoint_y = self.active_waypoint[0], self.active_waypoint[1]
            rel_x, rel_y = waypoint_x - (self.rect.x + 51), waypoint_y - self.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 270

            self.image = pygame.transform.rotate(self.transformed_image(), int(angle))
            self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def go_to_waypoint(self):
        if self.active_waypoint is not None:
            self.dist = math.sqrt((self.coord_x - self.active_waypoint[0]) ** 2 + (self.coord_y - self.active_waypoint[1]) ** 2)
            limit = 1200
            reduction = 100
            wp_vicinity = 30

            '''dopracować'''
            x_move = (self.active_waypoint[0] - self.coord_x) #+ random.randrange(-35, 35, 5)
            y_move = (self.active_waypoint[1] - self.coord_y) #+ random.randrange(-35, 35, 5)
            distance = abs(x_move + y_move)
            if distance > limit:
                reduction += (abs(distance)-limit)
            ''''''

            if self.dist > wp_vicinity:
                self.moving_to_wp = True
                self.coord_x += x_move / reduction
                self.coord_y += y_move / reduction

            elif self.dist <= wp_vicinity:
                if len(self.waypoints) == 1:
                    self.final_leg()
                else:
                    self.go_to_next_wp()

        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def final_leg(self):
        self.waypoints = []
        print(len(self.waypoints))
        self.bump()
        if self.ship_collision is False:
            self.moving_to_wp = False
            self.active_waypoint = None
        elif self.ship_collision is True:
            self.change_wp_upon_collision()

    def bump(self):
        for ship in self.list_of_ships:
            for item in ship.sprites():
                if item != self.rect and item.rect.colliderect(self.rect):
                    self.ship_collision = True
                    self.colliding_element = item

    def go_to_next_wp(self):
        if len(self.waypoints) > 1:
            self.waypoints.remove(self.waypoints[0])
            self.active_waypoint = self.waypoints[0]
            self.rotate()

    def change_wp_upon_collision(self):

        new_wp_x = self.coord_x + random.randrange(-75, 75, 25)
        new_wp_y = self.coord_y + random.randrange(-75, 75, 25)

        self.active_waypoint = (new_wp_x, new_wp_y)
        self.waypoints.append(self.active_waypoint)
        self.rotate()
        self.ship_collision = False

    def update(self):
        self.go_to_waypoint()
