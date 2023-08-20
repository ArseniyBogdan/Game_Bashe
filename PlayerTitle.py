import pygame
from enum import Enum


class PlayerTitle:
    ACTIVE_COLOR = (255, 255, 255)
    INACTIVE_COLOR = (184, 184, 184)

    class Alignment(Enum):
        TOP_LEFT = 1
        TOP_RIGHT = 2

    def __init__(self, surface: pygame.Surface, name, font,
                 positive_status, negative_status, active,
                 event_id, align: Alignment, end_of_game_ev_id):
        self.end_of_game_ev_id = end_of_game_ev_id
        self.surface = surface
        self.name = name
        self.font = font
        self.positive_status = positive_status
        self.negative_status = negative_status
        self.active = active
        self.event_id = event_id
        self.align = align
        if self.active:
            self.color = PlayerTitle.ACTIVE_COLOR
            self.status = self.positive_status
        else:
            self.color = PlayerTitle.INACTIVE_COLOR
            self.status = self.negative_status

    def draw(self):
        name_surface = self.font.render("Игрок " + self.name, True, self.color)
        status_surface = self.font.render("Статус " + self.status, True, self.color)

        window = self.surface.get_rect()
        name_w = name_surface.get_width()
        name_h = name_surface.get_height()
        status_w = status_surface.get_width()

        name_x, name_y = 0, 0
        status_x, status_y = 0, 0

        # считаем положение строчки статуса и имени игрока относительно
        # левого верхнего угла View с учётом выравнивания
        if self.align == PlayerTitle.Alignment.TOP_LEFT:
            name_x = 10
            name_y = 10
            status_x = name_x
            status_y = name_y + name_h
        elif self.align == PlayerTitle.Alignment.TOP_RIGHT:
            name_x = window.width - 10 - name_w
            name_y = 10
            status_x = window.width - 10 - status_w
            status_y = name_y + name_h

        self.surface.blit(name_surface, (name_x, name_y))
        self.surface.blit(status_surface, (status_x, status_y))

    def handle_event(self, event):
        if event.type == self.event_id:
            self.active = not self.active
            if self.active:
                self.color = PlayerTitle.ACTIVE_COLOR
                self.status = self.positive_status
            else:
                self.color = PlayerTitle.INACTIVE_COLOR
                self.status = self.negative_status

    def is_active(self):
        return self.active


