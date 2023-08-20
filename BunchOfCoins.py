import math

import pygame
import json


class BunchOfCoins(pygame.sprite.Sprite):

    def __init__(self, x, y, filename_group, section, coins, max_delta_coins):
        pygame.sprite.Sprite.__init__(self)
        self.max_delta_coins = max_delta_coins
        self.coins = coins
        self.max_coins = coins
        self.x = x
        self.y = y
        self.frame = 0
        self.paths = self.load_sprites(filename_group, section)
        if self.paths is not None:
            self.image = pygame.image.load(self.paths[6]).convert_alpha()
            self.rect = self.image.get_rect(center=(self.x, self.y))
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

    def update(self):
        # делим кучу монет на 7 долей, количество оставшихся
        # долей - кадр, который будет отрисовываться
        delta_change = math.ceil(self.max_coins / 7)
        self.image = pygame.image.load(self.paths[int(self.coins / delta_change)]).convert_alpha()

    def get_coins(self):
        return self.coins

    def set_coins(self, coins):
        self.coins = coins
        self.update()