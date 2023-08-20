import pygame
import json


class SpDoge(pygame.sprite.Sprite):
    def __init__(self, x, y, filename_group, section):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        # получаем пути к изображениям из json-файла
        self.paths = self.load_sprites(filename_group, section)
        if self.paths is not None:
            self.image = pygame.image.load(self.paths[0]).convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.image = None
            self.rect = None

    def load_sprites(self, filename_group, section):
        with open(filename_group) as f:
            templates = json.load(f)

        for section_t, paths in templates.items():
            if section_t == section:
                return paths

        return None

    def update(self, *args):
        self.frame += 1
        self.image = pygame.image.load(self.paths[self.frame % 24]).convert_alpha()
