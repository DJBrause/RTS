import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1600, 1000))
list_of_ships = []


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.moving_to_wp = False
        self.active_waypoint = None
        self.coord_x = x
        self.coord_y = y
        self.active = False
        self.ship_collision = False
        self.colliding_element = None
        super().__init__()
        self.og_image = pygame.image.load(r'graphics\statek_clear.png').convert_alpha()
        self.image = pygame.transform.scale(self.og_image, (51, 51))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))
        self.waypoints = []

    def test(self):
        print(f"len list = {len(self.waypoints)}")

    def transformed_image(self):
        self.image = pygame.transform.scale(self.og_image, (51, 51))
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
            x_move = (self.active_waypoint[0] - self.coord_x)
            y_move = (self.active_waypoint[1] - self.coord_y)
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
        for ship in list_of_ships:
            for item in ship.sprites():
                if item != self.rect and item.rect.colliderect(self.rect):
                    self.ship_collision = True
                    self.colliding_element = item

    def go_to_next_wp(self):
        if len(self.waypoints) > 1:
            self.waypoints.remove(self.active_waypoint)
            print(len(self.waypoints))
            self.active_waypoint = self.waypoints[0]
            self.rotate()

    def change_wp_upon_collision(self):

        new_wp_x = self.coord_x + random.randrange(-150, 150, 50)
        new_wp_y = self.coord_y + random.randrange(-150, 150, 50)

        self.active_waypoint = (new_wp_x, new_wp_y)
        self.waypoints.append(self.active_waypoint)
        self.rotate()
        self.ship_collision = False

    def update(self):
        self.go_to_waypoint()


class Station(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'graphics\spacestation\WB_baseu3_d0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(midbottom=(300, 200))

    def move(self):
        pass

    def update(self):
        pass


def ship_generator():
    for i in range(10):
        x = random.randint(0, 1600)
        y = random.randint(0, 1000)
        player = pygame.sprite.GroupSingle()
        player.add(Player(x, y))
        list_of_ships.append(player)


ship_generator()

station = pygame.sprite.GroupSingle(sprite=Station())
station.add(Station())

background = pygame.image.load(r'graphics/SpaceShooterRedux/Backgrounds/black.png').convert_alpha()
background = pygame.transform.scale(background, (1600, 1000))


def main():
    pygame.display.set_caption("RTS maybe")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text_surface = test_font.render("test text", False, (0, 0, 0))  # (text, anti aliasing, color)
    selection_box_start = None
    selection = None

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    forward_wp_to_active_ship_list(event.pos)

                else:
                    waypoint = event.pos
                    forward_wp_to_active_ship(waypoint)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = event.pos
                collision_check(click_pos)
                selection_box_start = click_pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if selection is not None:
                    collision_check(selection)
                    selection = None

        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
            selection_box_end = pygame.mouse.get_pos()
            width = -(selection_box_start[0] - selection_box_end[0])
            height = -(selection_box_start[1] - selection_box_end[1])
            selection = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(selection_box_start[0], selection_box_start[1]
                                                                          , width, height), 2)

        draw_ships()
        station.draw(screen)

        pygame.display.update()
        clock.tick(60)  # <-- ogranicza program do 60 fps


def draw_ships():
    for ship in list_of_ships:
        ship.draw(screen)
        ship.update()


def forward_wp_to_active_ship(wp):
    for ship in list_of_ships:
        for item in ship.sprites():
            if item.active is True:
                item.new_waypoint(wp)
                item.waypoints.append(wp)


def forward_wp_to_active_ship_list(wp):
    for ship in list_of_ships:
        for item in ship.sprites():
            if item.active is True:
                item.waypoints.append(wp)
                print(len(item.waypoints))
                if len(item.waypoints) == 1:
                    item.new_waypoint_keep_list(wp)

def collision_check(rect):
    if type(rect) == tuple:
        for ship in list_of_ships:
            for item in ship.sprites():
                if item.rect.collidepoint(rect):
                    item.activate_ship()
                else:
                    item.deactivate_ship()
    elif type(rect) == pygame.Rect:
        for ship in list_of_ships:
            for item in ship.sprites():
                if item.rect.colliderect(rect):
                    item.activate_ship()
                else:
                    item.deactivate_ship()


if __name__ == "__main__":

    main()
