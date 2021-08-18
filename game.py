import pygame
import math
import random
from ship_class import Player

pygame.init()
screen = pygame.display.set_mode((1600, 1000))
list_of_ships = []
scroll = [0, 0]

class Station(pygame.sprite.Sprite):
    def __init__(self):
        self.x_coord = 300
        self.y_coord = 200
        super().__init__()
        self.image = pygame.image.load(r'graphics\spacestation\WB_baseu3_d0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(midbottom=(self.x_coord, self.y_coord))

    def move(self):
        pass

    def update(self):
        pass

# Two super junky functions. To be replaced with dynamic ship generation.
def ship_generator():
    for i in range(10):
        x = random.randint(0, 1600)
        y = random.randint(0, 1000)
        player = pygame.sprite.GroupSingle()
        player.add(Player(x, y))
        list_of_ships.append(player)

def add_ship_list_to_ships():
    for sprite in list_of_ships:
        for ship in sprite.sprites():
            ship.list_of_ships = list_of_ships

ship_generator()
add_ship_list_to_ships()

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
        screen_scrolling()
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
        add_scroll_to_ship_pos()
        draw_ships()
        station.draw(screen)

        pygame.display.update()
        clock.tick(60)  # <-- ogranicza program do 60 fps


def draw_ships():
    for ship in list_of_ships:
        ship.draw(screen)
        ship.update()


def add_scroll_to_ship_pos():
    for rectangle in station.sprites():
        rectangle.rect.x -= scroll[0]
        rectangle.rect.y -= scroll[1]
    for sprite in list_of_ships:
        for rectangle_ship in sprite.sprites():
            rectangle_ship.coord_x -= scroll[0]
            rectangle_ship.coord_y -= scroll[1]
            rectangle_ship.wp_modifier_x -= scroll[0]
            rectangle_ship.wp_modifier_y -= scroll[1]
            if rectangle_ship.active_waypoint is not None:
                rectangle_ship.active_waypoint = ((rectangle_ship.active_waypoint[0] - scroll[0]), (rectangle_ship.active_waypoint[1] - scroll[1]))

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
                # adding wp modifier to take into account scrolling
                print(item.wp_modifier_x)
                wp = (wp[0] - item.wp_modifier_x, wp[1] - item.wp_modifier_y)
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


def screen_scrolling():
    global scroll
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] < 20:
        scroll[0] -= 1
        print("scrolling left")
    elif mouse_pos[0] > 1579:
        scroll[0] += 1
        print("scrolling right")
    elif mouse_pos[1] < 20:
        scroll[1] -= 1
        print("scrolling down")
    elif mouse_pos[1] > 979:
        scroll[1] += 1
        print("scrolling up")
    else:
        scroll = [0, 0]


if __name__ == "__main__":

    main()
