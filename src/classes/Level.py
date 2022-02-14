import pygame
from src.config.settings import TILE_SIZE, WORLD_MAP
from src.classes.Tile import Tile
from src.classes.Player import Player


class Level:

    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.generate_map()

    def generate_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
