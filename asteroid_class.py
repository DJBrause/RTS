import pygame


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.coord_x, self.coord_y = x, y
        self.hitpoints = 100
        super().__init__()
        self.image = pygame.image.load(r'E:\Projekty Python\PyGame_2021\graphics\SpaceShooterRedux\PNG\Meteors\meteorGrey_med1.png').convert_alpha()
        #self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def move(self):
        pass

    def update(self):
        pass