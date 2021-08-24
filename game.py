import pygame
import random
from ship_class import Player
from asteroid_class import Asteroid
from projectile_class import Projectile

pygame.init()
window_width = 1200
window_height = 900
screen = pygame.display.set_mode((window_width, window_height))
list_of_ships = []
list_of_asteroids = []
list_of_projectiles = []
active_ships = []
scroll = [0, 0]
scrolled_distance_x = 0
scrolled_distance_y = 0
### For event loop ###
object_detected = False
######################




class Station(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x_coord, self.y_coord = x, y
        super().__init__()
        self.image = pygame.image.load(r'graphics\spacestation\WB_baseu3_d0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(self.x_coord, self.y_coord))

    def move(self):
        pass

    def update(self):
        pass


# To be replaced with dynamic ship generation.
def ship_generator():
    for i in range(10):
        x = random.randint(0, window_width)
        y = random.randint(0, window_height)
        player = pygame.sprite.GroupSingle()
        player.add(Player(x, y))
        list_of_ships.append(player)


def add_ship_list_to_ships():
    for sprite in list_of_ships:
        for ship in sprite.sprites():
            ship.list_of_ships = list_of_ships


def asteroid_generator():
    for i in range(50):
        x = random.randint(-window_width, window_width)
        y = random.randint(-window_height, window_height)
        asteroid = pygame.sprite.GroupSingle()
        asteroid.add(Asteroid(x, y))
        list_of_asteroids.append(asteroid)


def projectile_generator(x,y,target):
    shot = pygame.sprite.GroupSingle(Projectile(x, y, target))
    list_of_projectiles.append(shot)


ship_generator()
add_ship_list_to_ships()
asteroid_generator()

"""TEST"""

station = pygame.sprite.GroupSingle()
station.add(Station(window_width/3, window_height/2))

station2 = pygame.sprite.GroupSingle()
station2.add(Station(window_width/2, (window_height/2)*-1))

"""TEST"""

background = pygame.image.load(r'graphics/SpaceShooterRedux/Backgrounds/black.png').convert_alpha()
background = pygame.transform.scale(background, (1600, 1000))


def main():
    global object_detected
    pygame.display.set_caption("RTS maybe")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text_surface = test_font.render("test text", False, (0, 0, 0))  # (text, anti aliasing, color)
    selection_box_start = None
    selection = None


    while True:
        screen.blit(background, (0, 0))
        screen_scrolling()
        # Resets object_detected to false value for every frame.
        object_detected = False


        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    forward_wp_to_active_ship_list(event.pos)

                else:
                    # Checks if there is any targetable object in click location. If yes, ship moves to engage,
                    # if not, it continues with regular move.
                    check_for_targetable_object(event.pos)
                    if object_detected is True:
                        engage_target()
                    elif object_detected is False:
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
        draw_objects()
        remove_destroyed_objects()
        engage_target()
        #################
        station.draw(screen)
        station2.draw(screen)
        #################
        pygame.display.update()
        clock.tick(60)  # <-- ogranicza program do 60 fps


# Takes all objects and draws then on the screen in each frame.

def draw_objects():
    for ship in list_of_ships:
        ship.draw(screen)
        ship.update()
    for asteroid in list_of_asteroids:
        asteroid.draw(screen)
        asteroid.update()
    for projectile in list_of_projectiles:
        projectile.draw(screen)
        projectile.update()


# Prevents removed/destroyed objects from being drawn.
def remove_destroyed_objects():
    for projectile in list_of_projectiles:
        for projectile_sprite in projectile.sprites():
            if projectile_sprite.explosion_end is True:
                list_of_projectiles.remove(projectile)


# Updates objects position with scroll value.

def add_scroll_to_ship_pos():
    int_scroll_x = int(scroll[0])
    int_scroll_y = int(scroll[1])

    for rectangle in station.sprites():
        rectangle.rect.x -= int_scroll_x
        rectangle.rect.y -= int_scroll_y

    for rectangle in station2.sprites():
        rectangle.rect.x -= int_scroll_x
        rectangle.rect.y -= int_scroll_y

    ###################################

    for sprite in list_of_ships:

        for rectangle_ship in sprite.sprites():
            rectangle_ship.coord_x -= int_scroll_x
            rectangle_ship.coord_y -= int_scroll_y
            # Ship waypoints update
            new_waypoints = []
            for waypoint in rectangle_ship.waypoints:
                coord_x = waypoint[0]
                coord_y = waypoint[1]
                coord_x -= int_scroll_x
                coord_y -= int_scroll_y
                new_waypoint = (coord_x, coord_y)
                new_waypoints.append(new_waypoint)
            rectangle_ship.waypoints = new_waypoints
            if rectangle_ship.active_waypoint is not None:
                rectangle_ship.active_waypoint = ((rectangle_ship.active_waypoint[0] - int_scroll_x),
                                                  (rectangle_ship.active_waypoint[1] - int_scroll_y))

    for sprite in list_of_asteroids:
        for asteroid_rectangle in sprite.sprites():
            asteroid_rectangle.rect.x -= int_scroll_x
            asteroid_rectangle.rect.y -= int_scroll_y

    for projectile in list_of_projectiles:  # Updates both projectile position and target variable.
        for projectile_sprite in projectile.sprites():
            projectile_sprite.coord_x -= int_scroll_x
            projectile_sprite.coord_y -= int_scroll_y
            new_target_x = projectile_sprite.target[0]
            new_target_y = projectile_sprite.target[1]
            new_target_x -= int_scroll_x
            new_target_y -= int_scroll_y
            projectile_sprite.target = (new_target_x, new_target_y)


'''''''''MOVEMENT FUNCTIONS'''''''''''


# Move towards a single waypoint.
def forward_wp_to_active_ship(wp):
    for ship in list_of_ships:
        for item in ship.sprites():
            if item.active is True:
                item.new_waypoint(wp)
                item.waypoints.append(wp)
                # Prevents ship from shooting once move order was made.
                item.target = None


# Adds additional waypoints to waypoints list.
def forward_wp_to_active_ship_list(wp):
    for ship in list_of_ships:
        for item in ship.sprites():
            if item.active is True:
                # Adds new waypoint to the list. If there is a single entry in the waypoints list,
                # it become the active waypoint.
                item.waypoints.append(wp)
                if len(item.waypoints) == 1:
                    item.new_waypoint_keep_list(wp)


def move_to_target(click_pos):
    active_ships.clear()
    populate_active_ship_list()
    for asteroid_sprite in list_of_asteroids:
        for asteroid_obj in asteroid_sprite.sprites():
            if asteroid_obj.rect.collidepoint(click_pos):
                for ship in active_ships:
                    ship.attacking_target = True
                    ship.target = (asteroid_obj.rect.x, asteroid_obj.rect.y)


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


def populate_active_ship_list():
    for ship in list_of_ships:
        for ship_sprite in ship.sprites():
            if ship_sprite.active is True:
                active_ships.append(ship_sprite)


'''''''''SUPPORTING FUNCTIONS'''''''''''


def check_for_targetable_object(click_pos):
    global object_detected
    active_ships.clear()
    populate_active_ship_list()

    for asteroid in list_of_asteroids:
        for asteroid_sprite in asteroid.sprites():
            if asteroid_sprite.rect.collidepoint(click_pos):
                # Passes the rect of the target object to ship.
                pass_target_to_active_ships(asteroid_sprite.rect)
                object_detected = True


def pass_target_to_active_ships(target):
    for ship in active_ships:
        ship.target = target
        ship.orbit_mode = True
        ship.orbit_target()


def engage_target():
    for ship_item in list_of_ships:
        for ship in ship_item.sprites():
            if ship.target is not None:
                ship.check_distance(ship.target)
                if ship.dist <= ship.max_range:
                    if ship.shot_interval == 0:
                        x_cor = int(ship.coord_x)
                        y_cor = int(ship.coord_y)
                        projectile_generator(x_cor, y_cor, ship.target)
                    ship.shot_interval += .1
                    if ship.shot_interval >= 5:
                        ship.shot_interval = 0
                    ship.waypoints = []


def screen_scrolling():
    global scroll, scrolled_distance_x, scrolled_distance_y

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] < 20:
        scroll[0] -= 1
        scrolled_distance_x -= 1
    elif mouse_pos[0] > (window_width - 20):
        scroll[0] += 1
        scrolled_distance_x += 1
    elif mouse_pos[1] < 20:
        scroll[1] -= 1
        scrolled_distance_y -= 1
    elif mouse_pos[1] > (window_height - 20):
        scroll[1] += 1
        scrolled_distance_y += 1
    else:
        scroll = [0, 0]


if __name__ == "__main__":

    main()
