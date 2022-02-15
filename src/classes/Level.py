import pygame
from random import choice
from src.functions.helper import import_csv_layout, import_folder
from src.config.settings import TILE_SIZE
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
        layouts = {
            'boundary': import_csv_layout('src/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('src/map/map_Grass.csv'),
            'object': import_csv_layout('src/map/map_LargeObjects.csv')
        }
        graphics = {
            'grass': import_folder('src/graphics/Grass'),
            'objects': import_folder('src/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacle_sprites],
                                 'grass', choice(graphics['grass']))

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacle_sprites],
                                 'object', surf)

        self.player = Player((2000, 1430), [self.visible_sprites],
                             self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.h_width = self.display_surface.get_size()[0] // 2
        self.h_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        self.floor_surf = pygame.image.load(
            'src/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # get offset
        self.offset.x = player.rect.centerx - self.h_width
        self.offset.y = player.rect.centery - self.h_height

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # first draw minor y valued sprites
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
