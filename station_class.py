import pygame


class Station(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.coord_x, self.coord_y = x, y
        super().__init__()
        self.image = pygame.image.load(r'graphics\spacestation\WB_baseu3_d0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def move(self):
        self.rect = self.image.get_rect(center=(self.coord_x, self.coord_y))

    def update(self):
        self.move()
