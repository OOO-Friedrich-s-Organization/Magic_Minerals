import pygame
import os
import sys
from level_generator import GamePlace, Button


pygame.init()

WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_menu_sprites = pygame.sprite.Group()
btn_levels_sprites = pygame.sprite.Group()
levels_sprites = pygame.sprite.Group()

last_level = 1


class Main:
    btns_now = ['Начать игру', 'Уровни', 'laud_off', 'back_btn']

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

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, color_key=None):
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

    def click_check_main(self, coords):
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

    def laud_control(self):
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
            Button(self.btns[btn], self.btns_positions[btn], btn_menu_sprites)
        btn_menu_sprites.draw(screen)
        btn_menu_sprites.update()

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 53)
        for button in self.font_positions:
            string_rendered = font.render(button, 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = self.font_positions[button][1]
            text_rect.x = self.font_positions[button][0]
            screen.blit(string_rendered, text_rect)

    def click_check(self, coords):
        for ind, button in enumerate(self.btns_positions):
            if ind < 2:
                btn = self.btns_positions[button]
                if (btn[0] < coords[0] < btn[0] + btn[2] and
                        btn[1] < coords[1] < btn[1] + btn[3]):
                    if ind == 0:
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
            self.first_time = False

        for btn in self.btns_now[2:]:
            Button(self.btns[btn], self.btns_positions[btn], btn_levels_sprites)
        for circle in self.circles_pos:
            Button(self.btns['circle'], circle, btn_levels_sprites)
        for btn in self.btns_levels_pos:
            Button(self.btns['100x100'], btn, btn_levels_sprites)
        btn_levels_sprites.draw(screen)
        btn_levels_sprites.update()

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 70)
        for button in range(1, 6):
            string_rendered = font.render(str(button), 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = self.btns_levels_pos[button - 1][1] + 20
            text_rect.x = self.btns_levels_pos[button - 1][0] + 35
            screen.blit(string_rendered, text_rect)

    def click_check(self, coords):
        for ind, button in enumerate(self.btns_positions):
            if ind < 2:
                btn = self.btns_positions[button]
                if (btn[0] < coords[0] < btn[0] + btn[2] and
                        btn[1] < coords[1] < btn[1] + btn[3]):
                    pass


main = Main()
menu = Menu()
levels = LevelsMenu()
game = 0


def game_start():
    global game
    game = GamePlace(main)


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
