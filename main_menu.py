import pygame
import os
import sys
import csv
from level_generator import GamePlace, Image


pygame.init()

WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_menu_sprites = pygame.sprite.Group()
btn_levels_sprites = pygame.sprite.Group()
levels_sprites = pygame.sprite.Group()
locked_group = pygame.sprite.Group()


def get_last_level():  # получение номера последенего открытого уровня
    with open('assets/data/levels_menu.csv', 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';', quotechar='"')
        data = list(data)
        if len(data) == 6:
            del data[5]
        return int(list(filter(lambda x: x[1] == 'open', data))[-1][0])


def get_locked_levels():  # получение списка открытых уровней
    with open('assets/data/levels_menu.csv', 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';', quotechar='"')
        data = list(data)
        if len(data) == 6:
            del data[5]
        data = list(filter(lambda x: x[1] == 'locked', data))
        data = list(map(lambda x: int(x[0]), data))
    return data


def open_new_level():  # открытие нового уровня
    global last_level
    if last_level != 5:
        with open('assets/data/levels_menu.csv', 'r', encoding='utf-8') as file:
            data = csv.reader(file, delimiter=';', quotechar='"')
            data = list(data)
            if len(data) == 6:
                del data[5]
        with open('assets/data/levels_menu.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"')
            for ind, elem in enumerate(data):
                if last_level == ind:
                    elem[1] = 'open'
                writer.writerow(elem)


last_level = get_last_level()


class Main:
    btns_now = ['Начать игру', 'Уровни', 'laud_on', 'back_btn']

    def __init__(self):
        self.condition = 'menu'

        self.btns_positions = {'Начать игру': [390, 300, 300, 100],
                               'Уровни': [390, 450, 300, 100],
                               'laud_on': [1000, 640, 60, 60],
                               'laud_off': [1000, 640, 60, 60],
                               'back_btn': [20, 640, 60, 60]
                               }
        self.btns = {'Начать игру': self.load_image('buttons/300x100_btn.png'),
                     'Уровни': self.load_image('buttons/300x100_btn.png'),
                     '100x100': self.load_image('buttons/100x100_btn.png'),
                     'locked': self.load_image('buttons/locked.png'),
                     'circle': self.load_image('buttons/circle.png'),
                     'laud_on': self.load_image('buttons/60x60_btn_laud_on.png'),
                     'laud_off': self.load_image('buttons/60x60_btn_laud_off.png'),
                     'back_btn': self.load_image('buttons/back_btn.png'),
                     }
        self.font_positions = {'Начать игру': [410, 327],
                               'Уровни': [464, 477],
                               }

        self.btns_levels_pos = [[177, 179, 100, 100], [300, 364, 100, 100], [563, 257, 100, 100],
                                [730, 434, 100, 100], [884, 253, 100, 100]]
        self.circles_pos = [[210, 287], [216, 327], [235, 364], [267, 395], [400, 404], [435, 375],
                            [462, 336], [491, 305], [530, 287], [668, 294], [689, 327],
                            [679, 368], [668, 409], [666, 446], [694, 471], [833, 472],
                            [866, 453], [895, 430], [917, 355], [913, 394]]

    def terminate(self):  # завершение работы программы
        pygame.quit()
        sys.exit()

    def load_image(self, name, color_key=None):  # загрузка изображений
        fullname = os.path.join('assets', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

        if color_key is None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image

    def click_check_main(self, coords):  # основная функция обработки нажатий мыши
        if self.condition == 'game' and type(game.score) == int:
            if game.win:
                for button in game.end_win_btns_positions:
                    btn = game.end_win_btns_positions[button]
                    if (btn[0] < coords[0] < btn[0] + 100 and
                            btn[1] < coords[1] < btn[1] + 100):
                        if button == 'repeat':
                            main.condition = 'game'
                            game_start()
                            open_new_level()
                        elif button == 'levels':
                            main.condition = 'levels'
                            levels.first_time = True
                            open_new_level()
                        elif button == 'skip':
                            global last_level
                            open_new_level()
                            if last_level != 5:
                                main.condition = 'game'
                                last_level += 1
                                game_start()
                            else:
                                self.condition = 'menu'
                                menu.first_time = True
                                game_start()
            elif not game.win:
                for button in game.end_lose_btns_positions:
                    btn = game.end_lose_btns_positions[button]
                    if (btn[0] < coords[0] < btn[0] + 100 and
                            btn[1] < coords[1] < btn[1] + 100):
                        if button == 'repeat':
                            main.condition = 'game'
                            game_start()
                        elif button == 'levels':
                            main.condition = 'levels'
                            levels.first_time = True
        else:
            for ind, button in enumerate(self.btns_positions):
                if ind >= 2:
                    btn = self.btns_positions[button]
                    if (btn[0] < coords[0] < btn[0] + btn[2] and
                            btn[1] < coords[1] < btn[1] + btn[3]):
                        if ind == 2 or ind == 3:
                            self.laud_control()
                            break
                        elif ind == 4:
                            self.condition = 'menu'
                            menu.first_time = True
                            game_start()
                    elif ind == 4:
                        if self.condition == 'menu':
                            menu.click_check(coords)
                            break
                        elif self.condition == 'levels':
                            levels.click_check(coords)
                            break
                        elif self.condition == 'game':
                            game.click_check(coords)
                            break

    def laud_control(self):  # включение/выключение звука
        if 'laud_off' in self.btns_now:
            self.btns_now[self.btns_now.index('laud_off')] = 'laud_on'
        else:
            self.btns_now[self.btns_now.index('laud_on')] = 'laud_off'


class Menu(Main):
    def __init__(self):
        super().__init__()
        self.fon = pygame.transform.scale(self.load_image('fon/bg_logo.png'), (WIDTH, HEIGHT))
        self.first_time = True

    def render(self):
        if self.first_time:
            screen.blit(self.fon, (0, 0))
            self.first_time = False

        for btn in self.btns_now[:-1]:
            if btn == 'loud_on':
                print(1)
            Image(self.btns[btn], self.btns_positions[btn], btn_menu_sprites)
        btn_menu_sprites.draw(screen)
        btn_menu_sprites.update()

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 53)
        for button in self.font_positions:
            string_rendered = font.render(button, 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = self.font_positions[button][1]
            text_rect.x = self.font_positions[button][0]
            screen.blit(string_rendered, text_rect)

    def click_check(self, coords):  # локальная функция обработки нажатий в главном меню
        for ind, button in enumerate(self.btns_positions):
            if ind < 2:
                btn = self.btns_positions[button]
                if (btn[0] < coords[0] < btn[0] + btn[2] and
                        btn[1] < coords[1] < btn[1] + btn[3]):
                    if ind == 0:
                        global last_level
                        last_level = get_last_level()
                        main.condition = 'game'
                        game_start()
                    elif ind == 1:
                        main.condition = 'levels'
                        levels.first_time = True


class LevelsMenu(Main):
    def __init__(self):
        super().__init__()
        self.fon = pygame.transform.scale(self.load_image('fon/bg.png'), (WIDTH, HEIGHT))
        self.first_time = True

    def render(self):
        screen.blit(self.fon, (0, 0))
        if self.first_time:
            screen.blit(self.fon, (0, 0))

        for btn in self.btns_now[2:]:
            Image(self.btns[btn], self.btns_positions[btn], btn_levels_sprites)
        if self.first_time:
            btn_levels_sprites.empty()
            locked_group.empty()
            for circle in self.circles_pos:
                Image(self.btns['circle'], circle, btn_levels_sprites)
            for btn in self.btns_levels_pos:
                Image(self.btns['100x100'], btn, btn_levels_sprites)
            data = get_locked_levels()
            for ind, btn in enumerate(self.btns_levels_pos):
                if ind + 1 in data:
                    Image(self.btns['locked'], btn, locked_group)
            self.first_time = False

        btn_levels_sprites.draw(screen)

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 70)
        for button in range(1, 6):
            string_rendered = font.render(str(button), 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = self.btns_levels_pos[button - 1][1] + 20
            text_rect.x = self.btns_levels_pos[button - 1][0] + 35
            screen.blit(string_rendered, text_rect)

        locked_group.draw(screen)

    def click_check(self, coords):  # локальная функция обработки нажатий в меню уровней
        data = get_locked_levels()
        for ind, button in enumerate(self.btns_levels_pos):
            if ind + 1 not in data:
                btn = self.btns_levels_pos[ind]
                if (btn[0] < coords[0] < btn[0] + btn[2] and
                        btn[1] < coords[1] < btn[1] + btn[3]):
                    global last_level
                    last_level = ind + 1
                    main.condition = 'game'
                    game_start()


main = Main()
menu = Menu()
levels = LevelsMenu()
game = None


def game_start():
    global game
    del game
    game = GamePlace(main, last_level)
    game.cleaner()


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                main.click_check_main(event.pos)

        if main.condition == 'menu':
            menu.render()
        elif main.condition == 'levels':
            levels.render()
        elif main.condition == 'game':
            game.render(last_level)

        pygame.display.flip()
        clock.tick(30)

main.terminate()
