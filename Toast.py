import pygame


class Toast:
    TOAST_COLOR = (184, 184, 184)
    LENGTH_LONG = 10000
    LENGTH_SHORT = 3000

    def __init__(self, surface: pygame.Surface, font,
                 finish_event_id, start_event_id, text=None, time_in_millis=LENGTH_SHORT):
        self.surface = surface
        self.time_in_millis = time_in_millis
        self.text = text
        self.font = font
        self.start_event_id = start_event_id
        self.finish_event_id = finish_event_id
        self.color = pygame.color.Color(Toast.TOAST_COLOR)
        self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
        self.active = False

    def draw(self):
        if self.active:
            # высчитываем координаты Toast (снизу посередине)
            window = self.surface.get_rect()
            toast_w = self.txt_surface.get_width()
            toast_h = self.txt_surface.get_height()
            text_x = (window.width - toast_w) / 2
            text_y = (window.height - window.height / 8) - toast_h

            rect_x = text_x - 5
            rect_y = text_y - 5

            rect = pygame.rect.Rect(rect_x, rect_y, toast_w + 10, toast_h + 10)

            pygame.draw.rect(self.surface, self.color, rect)
            self.surface.blit(self.txt_surface, (text_x, text_y))

    def handle_event(self, event):
        if event.type == self.start_event_id:
            self.active = True
            pygame.time.set_timer(self.finish_event_id, self.time_in_millis, True)
        if event.type == self.finish_event_id:
            self.active = False

    def set_text(self, text):
        self.text = text
        self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
