import pygame

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x_coord, self.y_coord = x, y
        self.hitpoints = 100
        super().__init__()
        self.image = pygame.image.load(r'E:\Projekty Python\PyGame_2021\graphics\SpaceShooterRedux\PNG\Meteors\meteorGrey_med1.png').convert_alpha()
        #self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(self.x_coord, self.y_coord))

    def move(self):
        pass

    def update(self):
        pass