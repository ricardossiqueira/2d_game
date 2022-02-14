import pygame
from src.config.settings import TILE_SIZE, WORLD_MAP
from src.classes.Tile import Tile
from src.classes.Player import Player
from src.debug.debugging_tool import debug


class Level:

    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # groups
        self.visible_sprites = YSortCameraGroup()
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
                    self.player = Player((x, y), [self.visible_sprites],
                                         self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.h_width = self.display_surface.get_size()[0] // 2
        self.h_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

    def custom_draw(self, player):

        # get offset
        self.offset.x = player.rect.centerx - self.h_width
        self.offset.y = player.rect.centery - self.h_height

        # first draw minor y valued sprites
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
