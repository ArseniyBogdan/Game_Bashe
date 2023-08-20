import pygame
import json
from enum import Enum
from Toast import Toast

class CharacterSprite(pygame.sprite.Sprite):
    class Orientation(Enum):
        RIGHT = 1
        LEFT = 2

    def __init__(self, x, y, filename_group, section, orientation: Orientation,
                 step_width, move_event_id, slowness, active):
        pygame.sprite.Sprite.__init__(self)
        # во сколько раз медленней двигается спрайт
        # по сравнению со скоростью отрисовки кадров игры
        self.slowness = slowness

        self.tick = 0
        self.active = active
        self.move_event_id = move_event_id
        self.x = x
        self.y = y

        # в какую сторону смотрит спрайт при начале ходьбы
        self.orientation = orientation

        self.step_width = step_width
        self.frame = 0
        self.is_moving = False
        self.paths = self.load_sprites(filename_group, section)
        if self.paths is not None:
            self.image = pygame.image.load(self.paths[0]).convert_alpha()
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

    def handle_event(self, event):
        if event.type == self.move_event_id and self.active:
            self.is_moving = True
            self.active = False
        elif event.type == self.move_event_id and not self.active:
            self.active = True

    def update(self, *args):
        if self.is_moving and self.tick % self.slowness:
            # игнорируем кадры с 1 по 3, с 12 по 16 и с 25 по 26
            # т.к. на них персонаж не двигается, а разворачивается
            if self.orientation == CharacterSprite.Orientation.RIGHT and 2 < self.frame % 26 < 11:
                self.x += self.step_width
            elif self.orientation == CharacterSprite.Orientation.RIGHT and 15 < self.frame % 26 < 24:
                self.x -= self.step_width
            elif self.orientation == CharacterSprite.Orientation.LEFT and 2 < self.frame % 26 < 11:
                self.x -= self.step_width
            elif self.orientation == CharacterSprite.Orientation.LEFT and 15 < self.frame % 26 < 24:
                self.x += self.step_width

            self.frame += 1
            self.image = pygame.image.load(self.paths[self.frame % 26]).convert_alpha()
            self.rect = self.image.get_rect(center=(self.x, self.y))

            # при достижении по 1 кадра, останавливаем движение
            if self.frame % 26 == 0:
                self.is_moving = False
                self.tick = 0

        self.tick += 1

    def get_event_id(self):
        return self.move_event_id
