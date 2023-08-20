import pygame
from accessify import private


class Button:
    def __init__(self, display: pygame.Surface, width, height,
                 inactive_color=(219, 255, 253), active_color=(163, 255, 250)):
        self.display = display
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self, x, y, message, click_action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        left_clicked = pygame.mouse.get_pressed()[0]

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(self.display, self.active_color, (x, y, self.width, self.height))
            if left_clicked and click_action is not None:
                click_action()
        else:
            pygame.draw.rect(self.display, self.inactive_color, (x, y, self.width, self.height))

        self.print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)

    @private
    def print_text(self, message, x, y, font_color=(0, 0, 0), font_type='fonts/poppins-bold.ttf', font_size=30):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.display.blit(text, (x, y))