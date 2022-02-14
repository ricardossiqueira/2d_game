from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        return [list(row) for row in layout]


def import_folder(path):
    for _, _, img_files in walk(path):
        return [
            pygame.image.load(f'{path}/{img_path}').convert_alpha()
            for img_path in img_files
        ]
