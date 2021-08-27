import pygame
import math
import random


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, side):
        self.hitpoints = 100
        self.moving_to_wp = False
        self.active_waypoint = None
        self.coord_x = x
        self.coord_y = y
        self.active = False
        self.ship_collision = False
        self.list_of_ships = []
        self.waypoints = []
        self.max_range = 100
        self.side = side
        self.dist = None
        self.target_object = None
        self.target = None
        self.attacking_target = False
        self.target_reached = False
        self.orbit_sector = 0
        self.orbit_mode = False
        self.shot_interval = 0
        self.timer = 0
        super().__init__()
        self.og_image_blue = pygame.image.load(r'graphics\fighter.png').convert_alpha()
        self.og_image_red = pygame.image.load(r'graphics\red_fighter.png').convert_alpha()
        self.image = self.image_choice()
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def test(self):
        print(f"len list = {len(self.waypoints)}")

    def image_choice(self):
        if self.side == 'red':
            self.image = self.og_image_red
        elif self.side == 'blue':
            self.image = self.og_image_blue
        return self.image

    def transformed_image_blue(self):
        self.image = pygame.transform.scale(self.og_image_blue, (16, 16))
        return self.image

    def transformed_image_red(self):
        self.image = pygame.transform.scale(self.og_image_red, (16, 16))
        return self.image

    '''Sets the ship into active state where it can react to orders.'''
    def activate_ship(self):
        self.active = True
        if self.moving_to_wp is False:
            self.active_waypoint = (self.coord_x, self.coord_y)

    def deactivate_ship(self):
        self.active = False

    # for use with RMB click, ignores waypoint list and goes right to the clicked coords.
    def new_waypoint(self, wp):
        self.orbit_mode = False
        self.orbit_sector = 0
        self.waypoints = []
        self.active_waypoint = wp
        self.rotate()

    # same as above, but keeps list
    def new_waypoint_keep_list(self, wp):
        self.active_waypoint = wp
        self.rotate()

    # rotates self towards next waypoint
    def rotate(self):
        if self.active_waypoint is not None:
            waypoint_x, waypoint_y = self.active_waypoint[0], self.active_waypoint[1]
            rel_x, rel_y = waypoint_x - (self.rect.x + 51), waypoint_y - self.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 270

            self.image = pygame.transform.rotate(self.image_choice(), int(angle))
            self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    # checks distance between self and destination/waypoint
    def check_distance(self, destination):
        if destination is not None:
            self.dist = math.sqrt((self.coord_x - destination[0]) ** 2 +
                                  (self.coord_y - destination[1]) ** 2)
            self.dist = int(self.dist)

    def go_to_waypoint(self):
        if self.active_waypoint is not None and self.target_reached is False:
            self.check_distance(self.active_waypoint)
            limit = 1200
            reduction = 100
            wp_vicinity = 30

            '''dopracować'''
            x_move = (self.active_waypoint[0] - self.coord_x) + random.randrange(-30, 30, 5)
            y_move = (self.active_waypoint[1] - self.coord_y) + random.randrange(-30, 30, 5)
            distance = abs(int(x_move + y_move))
            if distance > limit:
                reduction += (abs(distance)-limit)
            ''''''

            # if not near the destination, continue moving
            if self.dist > wp_vicinity:
                self.moving_to_wp = True
                self.coord_x += x_move / reduction
                self.coord_y += y_move / reduction

            # if near destination
            elif self.dist <= wp_vicinity:
                if self.orbit_mode is False:
                    # if this is last waypoint, check for bumps
                    if len(self.waypoints) == 1:
                        self.final_leg()
                    else:
                        self.go_to_next_wp()
                else:
                    self.orbit_target()



        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    # orbit_target generates random waypoints around target. orbit_target_2 creates 8 waypoints around the target.

    def orbit_target(self):
        # Swapping rect for tuple
        # a = self.target.x + self.target.w / 2
        # b = self.target.y + self.target.h / 2
        if self.target_object is not None:
            a = self.target[0] + self.target_object.rect.w / 2
            b = self.target[1] + self.target_object.rect.h / 2
            x = a + random.randint(-100, 100)
            y = b + random.randint(-100, 100)

            self.active_waypoint = (x, y)
            self.rotate()
        else:
            self.active_waypoint = (self.coord_x, self.coord_y)
            self.orbit_mode = False

    def orbit_target_2(self):
        r = 120
        a = self.target.x + self.target.w/2
        b = self.target.y + self.target.h/2
        x = int
        y = int
        if self.orbit_sector == 0:
            x = a
            y = b - r
        elif self.orbit_sector == 1:
            x = a - (r/2)
            y = b - (r/2)
        elif self.orbit_sector == 2:
            x = a - r
            y = b
        elif self.orbit_sector == 3:
            x = a - (r/2)
            y = b + (r/2)
        elif self.orbit_sector == 4:
            x = a
            y = b + r
        elif self.orbit_sector == 5:
            x = a + (r/2)
            y = b + (r/2)
        elif self.orbit_sector == 6:
            x = a + r
            y = b
        elif self.orbit_sector == 7:
            x = a + (r/2)
            y = b - (r/2)

        self.active_waypoint = (x, y)
        self.rotate()
        if self.orbit_sector != 7:
            self.orbit_sector += 1
        else:
            self.orbit_sector = 0
        self.bump()
        if self.ship_collision is True:
            self.change_wp_upon_collision()

    def final_leg(self):
        self.waypoints = []
        self.bump()
        if self.ship_collision is False:
            self.moving_to_wp = False
            self.active_waypoint = None
        elif self.ship_collision is True:
            self.change_wp_upon_collision()    # generates random waypoint to avoid collision state with another object

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

    def update_target(self):
        if self.target_object is not None and self.target_object.hitpoints > 0:
            x = self.target_object.rect.x
            y = self.target_object.rect.y
            self.target = (x, y)
        elif self.target_object is not None and self.target_object.hitpoints <= 0:
            self.target = None
            self.target_object = None

    def update(self):
        self.update_target()
        self.go_to_waypoint()
