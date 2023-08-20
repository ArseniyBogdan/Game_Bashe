import pygame
from accessify import private

from spinning_doge import SpDoge
from Bool import Bool
from InputBox import InputBox
from Toast import Toast
from Button import Button
from PlayerTitle import PlayerTitle
from CharacterSprite import CharacterSprite
from BunchOfCoins import BunchOfCoins

pygame.init()

# Константы для событий
START_TOAST_EVENT_ID = 17
FINISH_TOAST_EVENT_ID = 18
SWAP_PLAYERS = 1
END_OF_GAME = 1000


class Game:
    def __init__(self, num_of_coins=15, max_delta_coins=3,
                 display_width=800, display_height=600, FPS=24):
        self.num_of_coins = num_of_coins
        self.max_delta_coins = max_delta_coins
        self.display_width = display_width
        self.display_height = display_height
        self.display = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.game_is_running = False
        pygame.display.set_caption("Bashe game")
        self.open_menu()

    @private
    def open_menu(self):
        running = True
        doge1 = SpDoge(x=100, y=100, filename_group='sprites.json', section='spinning_doge')
        doge2 = SpDoge(x=700, y=100, filename_group='sprites.json', section='spinning_doge')
        doge3 = SpDoge(x=100, y=500, filename_group='sprites.json', section='spinning_doge')
        doge4 = SpDoge(x=700, y=500, filename_group='sprites.json', section='spinning_doge')

        button_start_game = Button(display=self.display, width=250, height=70)
        button_settings = Button(display=self.display, width=190, height=70)
        button_rules = Button(display=self.display, width=130, height=70)
        button_quit = Button(display=self.display, width=115, height=70)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

            self.display.fill((0, 0, 0))
            self.display.blit(doge1.image, doge1.rect)
            self.display.blit(doge2.image, doge2.rect)
            self.display.blit(doge3.image, doge3.rect)
            self.display.blit(doge4.image, doge4.rect)
            doge1.update()
            doge2.update()
            doge3.update()
            doge4.update()

            self.print_text(message='Game Bashe', x=270, y=140, font_color=(255, 255, 255), font_size=40)

            # связываем кнопки с действиями, которые они выполняют
            button_start_game.draw(x=275, y=200, message="Start Game", font_size=40, click_action=self.start_game)
            button_settings.draw(x=305, y=280, message="Settings", font_size=40, click_action=self.open_settings)
            button_rules.draw(x=335, y=360, message="Rules", font_size=40, click_action=self.open_rules)
            button_quit.draw(x=342, y=440, message="Quit", font_size=40, click_action=self.close)

            pygame.display.update()
            self.clock.tick(self.FPS)

    @private
    def blit_text(self, text, pos, font, color=(255, 255, 255)):
        word_height = 0
        words = [word.split(' ') for word in text.splitlines()]  # каждая строка в 2D массиве - list из слов
        space = font.size(' ')[0]  # ширина пробела.
        max_width, max_height = self.display.get_size()
        # уменьшаем размеры multiline текста, по сравнению с окном игры
        max_width -= 150
        max_height -= 100

        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # обновляем x по левому краю
                    y += word_height  # начинаем с новой строки
                self.display.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    @private
    def print_text(self, message, x, y, font_color=(0, 0, 0), font_type='fonts/poppins-bold.ttf', font_size=30):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.display.blit(text, (x, y))

    def open_settings(self):
        running = Bool()
        doge = SpDoge(x=700, y=100, filename_group='sprites.json', section='spinning_doge')
        font = pygame.font.Font(pygame.font.get_default_font(), 30)

        input_box1 = InputBox(150, 280, 140, 32, font, text=str(self.num_of_coins),
                              text_filter=lambda text: text.isdigit(),
                              action=lambda text: self.num_of_coins_control(text))
        input_box2 = InputBox(150, 430, 140, 32, font, text=str(self.max_delta_coins),
                              text_filter=lambda text: text.isdigit(),
                              action=lambda text: self.max_delta_control(text))
        input_boxes = [input_box1, input_box2]

        toast = Toast(surface=self.display, text="Сохранено", font=font, start_event_id=START_TOAST_EVENT_ID,
                      finish_event_id=FINISH_TOAST_EVENT_ID, time_in_millis=Toast.LENGTH_SHORT)

        button_back = Button(display=self.display, width=75, height=70)
        while running.get_value():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                for box in input_boxes:
                    box.handle_event(event)
                toast.handle_event(event)

            self.display.fill((0, 0, 0))
            for box in input_boxes:
                box.update()

            for box in input_boxes:
                box.draw(self.display)

            toast.draw()

            self.display.blit(doge.image, doge.rect)
            doge.update()

            button_back.draw(x=20, y=20, message='  <', font_size=40, click_action=lambda: running.set_value(False))

            self.print_text(message='Settings', x=335, y=140, font_color=(255, 255, 255), font_size=40)
            self.blit_text(text='Количество элементов (3 < M < 10000) в стартовой куче:',
                           pos=(150, 200),
                           font=font)
            self.blit_text(text='Можно изымать (1 <= N < M) элементов из кучи:',
                           pos=(150, 350),
                           font=font)
            pygame.display.update()
            self.clock.tick(self.FPS)

    def open_rules(self):
        running = Bool()
        doge = SpDoge(x=700, y=100, filename_group='sprites.json', section='spinning_doge')

        rules = "Баше — математическая игра, в которой два игрока из кучки, " \
                "содержащей первоначально N предметов, по очереди берут не менее одного " \
                "и не более М предметов. Проигравшим считается тот, кому нечего брать."

        button_back = Button(display=self.display, width=75, height=70)
        font = pygame.font.Font(pygame.font.get_default_font(), 30)

        while running.get_value():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

            self.display.fill((0, 0, 0))
            self.display.blit(doge.image, doge.rect)
            doge.update()
            button_back.draw(x=20, y=20, message='  <', font_size=40, click_action=lambda: running.set_value(False))

            self.print_text(message='Rules', x=335, y=140, font_color=(255, 255, 255), font_size=40)
            self.blit_text(text=rules, pos=(150, 220), font=font)
            pygame.display.update()
            self.clock.tick(self.FPS)

    def start_game(self):
        self.game_is_running = True
        coins = self.num_of_coins
        max_delta_coins = self.max_delta_coins
        running = Bool()

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        player_title_1 = PlayerTitle(surface=self.display, name="1", active=True,
                                     font=font, event_id=SWAP_PLAYERS, negative_status="inactive",
                                     positive_status="active", align=PlayerTitle.Alignment.TOP_LEFT,
                                     end_of_game_ev_id=END_OF_GAME)

        player_title_2 = PlayerTitle(surface=self.display, name="2", active=False,
                                     font=font, event_id=SWAP_PLAYERS, negative_status="inactive",
                                     positive_status="active", align=PlayerTitle.Alignment.TOP_RIGHT,
                                     end_of_game_ev_id=END_OF_GAME)

        players = [player_title_1, player_title_2]

        player_sprite_b = CharacterSprite(filename_group='sprites.json', section='businessman_b',
                                          orientation=CharacterSprite.Orientation.RIGHT, x=100,
                                          y=350, step_width=25, move_event_id=SWAP_PLAYERS, slowness=3, active=True)
        player_sprite_w = CharacterSprite(filename_group='sprites.json', section='businessman_w',
                                          orientation=CharacterSprite.Orientation.LEFT, x=700,
                                          y=350, step_width=25, move_event_id=SWAP_PLAYERS, slowness=3, active=False)

        button_back = Button(display=self.display, width=75, height=70)

        bunch_of_coins = BunchOfCoins(coins=coins, max_delta_coins=max_delta_coins,
                                      x=400, y=400, filename_group='sprites.json', section='bunch_of_coins')

        input_box = InputBox(200, 160, 140, 32, font, text=str(max_delta_coins),
                             text_filter=lambda text: text.isdigit(),
                             action=lambda text: self.coins_in_bunch(coins=bunch_of_coins, delta_coins=text))

        toast = Toast(self.display, font, start_event_id=END_OF_GAME,
                      finish_event_id=FINISH_TOAST_EVENT_ID, time_in_millis=Toast.LENGTH_SHORT)

        while running.get_value():

            if not self.game_is_running:
                if player_sprite_w.active:
                    toast.set_text(text="Победил игрок " + player_title_1.name)
                else:
                    toast.set_text(text="Победил игрок " + player_title_2.name)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                for player in players:
                    player.handle_event(event)
                player_sprite_b.handle_event(event)
                player_sprite_w.handle_event(event)
                input_box.handle_event(event)
                toast.handle_event(event)

            self.display.fill((0, 0, 0))
            self.display.blit(player_sprite_b.image, player_sprite_b.rect)
            player_sprite_b.update()
            self.display.blit(player_sprite_w.image, player_sprite_w.rect)
            player_sprite_w.update()

            self.display.blit(bunch_of_coins.image, bunch_of_coins.rect)

            self.print_text(message="Забрать N монет (до " + str(max_delta_coins) + "):",
                            x=200, y=120, font_type=pygame.font.get_default_font(), font_color=(255, 255, 255))
            self.print_text(message="Всего монет осталось: " + str(bunch_of_coins.get_coins()),
                            x=200, y=80, font_type=pygame.font.get_default_font(), font_color=(255, 255, 255))

            for player in players:
                player.draw()

            input_box.update()
            input_box.draw(self.display)

            button_back.draw(x=20, y=100, message='  <', font_size=40, click_action=lambda: running.set_value(False))

            toast.draw()

            pygame.display.update()
            self.clock.tick(self.FPS)

    def coins_in_bunch(self, coins: BunchOfCoins, delta_coins):
        num = int(delta_coins)
        if num <= self.max_delta_coins and self.game_is_running:
            if num > coins.get_coins():
                coins.set_coins(0)
            else:
                coins.set_coins(coins.get_coins() - num)
            if coins.get_coins() == 0:
                self.game_is_running = False
                pygame.event.post(pygame.event.Event(END_OF_GAME))
            pygame.event.post(pygame.event.Event(SWAP_PLAYERS))
            return True
        else:
            return False

    def num_of_coins_control(self, new_num):
        num = int(new_num)
        if 3 < num < 10000 and self.max_delta_coins < num:
            self.num_of_coins = num
            pygame.event.post(pygame.event.Event(START_TOAST_EVENT_ID))
            return True
        else:
            return False

    def max_delta_control(self, new_delta):
        num = int(new_delta)
        if 1 <= num < self.num_of_coins:
            self.max_delta_coins = num
            pygame.event.post(pygame.event.Event(START_TOAST_EVENT_ID))
            return True
        else:
            return False

    def close(self):
        pygame.quit()
        quit()


game = Game()
