import pygame

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, font, text='', text_filter=None, action=None):
        self.text_filter = text_filter
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.base_text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, (255, 255, 255))
        self.active = False
        self.action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # если нажали на окошко
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            # меняем цвет окошка на активный/неактивный
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                # при нажатии на Enter проверяем на соответствие
                # фильтру текста и на правильность выполнения действия
                if event.key == pygame.K_RETURN:
                    self.check_and_save()
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # подготавливаем текст к отображению
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def update(self):
        # Делаем окно шире, если не хватает места тексту
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Перерисовываем текст
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Перерисовываем окно
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def check_and_save(self):
        if not self.text_filter(self.text):
            # если не соответствует фильтру, то возвращаем исходный текст
            self.text = self.base_text
        else:
            if self.action is not None and not self.action(self.text):
                self.text = self.base_text
            else:
                # если соответствует фильтру и действие выполнилось
                # корректно то обновляем базовый текст
                self.base_text = self.text

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text