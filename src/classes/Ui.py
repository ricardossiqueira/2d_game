import pygame
from src.config.settings import *


class Ui:

    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.hp_bar_rect = pygame.Rect(10, 10, HP_BAR_WIDTH, BAR_HEIGHT)
        self.mp_bar_rect = pygame.Rect(10, 35, MP_BAR_WIDTH, BAR_HEIGHT)
        self.sta_bar_rect = pygame.Rect(10, 60, STA_BAR_WIDTH, BAR_HEIGHT)

        # load weapon graphics
        self.weapon_graphics = [
            pygame.image.load(weapon['graphic']).convert_alpha()
            for weapon in WEAPON_DATA.values()
        ]

    def draw_bar(self, current, max, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # conv
        ratio = current / max
        current_rect = bg_rect.copy()
        current_rect.width = ratio * bg_rect.width

        # draw bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(f'exp: {int(exp)}', False, TEXT_COLOR)
        text_rect = text_surf.get_rect(
            bottomright=(self.display_surface.get_size()[0] - 10,
                         self.display_surface.get_size()[1] - 10))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(5, 5))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(5, 5), 3)

        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, current_weapon_index, weapon_index):
        # bg
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        bg_color = UI_ACTIVE_COLOR if weapon_index == current_weapon_index else UI_BG_COLOR
        pygame.draw.rect(self.display_surface, bg_color, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        # overlay
        item_size = ITEM_BOX_SIZE * 0.8
        content_surf = self.weapon_graphics[weapon_index]
        scaled_width = content_surf.get_width(
        ) * item_size / content_surf.get_height()
        content_surf = pygame.transform.scale(content_surf,
                                              (scaled_width, item_size))
        content_rect = content_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(content_surf, content_rect)

    def display(self, player):
        self.draw_bar(player.hp, player.base_stats['hp'], self.hp_bar_rect,
                      HP_COLOR)
        self.draw_bar(player.sta, player.base_stats['sta'], self.sta_bar_rect,
                      STA_COLOR)
        self.draw_bar(player.mp, player.base_stats['mp'], self.mp_bar_rect,
                      MP_COLOR)
        self.show_exp(player.exp)
        for weapon_index in range(len(WEAPON_DATA)):
            left = (ITEM_BOX_SIZE + 10) * weapon_index + 10
            top = self.display_surface.get_height() - ITEM_BOX_SIZE - 10
            self.selection_box(left, top, player.weapon_index, weapon_index)