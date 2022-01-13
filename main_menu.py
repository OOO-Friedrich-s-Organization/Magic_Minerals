import pygame
import os
import sys


pygame.init()

WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_menu_sprites = pygame.sprite.Group()
btn_levels_sprites = pygame.sprite.Group()
levels_sprites = pygame.sprite.Group()

condition = 'menu'
levels = 8


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)#.convert()
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


btns_positions = {'Новая игра': [390, 300, 300, 100],
                  'Продолжить': [390, 300, 300, 100],
                  'Уровни': [390, 450, 300, 100],
                  'laud_on': [1000, 640, 60, 60],
                  'laud_off': [1000, 640, 60, 60]
                  }

btns_levels_pos = [[177, 179, 100, 100], [300, 364, 100, 100], [563, 257, 100, 100],
                   [730, 434, 100, 100], [884, 253, 100, 100]]
circles_pos = [[210, 287], [216, 327], [235, 364], [267, 395], [400, 404], [435, 375],
               [462, 336], [491, 305], [530, 287], [668, 294], [689, 327],
               [679, 368], [668, 409], [666, 446], [694, 471], [833, 472],
               [866, 453], [895, 430], [917, 355], [913, 394]]

btns = {'Новая игра': load_image('buttons/300x100_btn.png'),
        'Продолжить': load_image('buttons/300x100_btn.png'),
        'Уровни': load_image('buttons/300x100_btn.png'),
        '100x100': load_image('buttons/100x100_btn.png'),
        'circle': load_image('buttons/circle.png'),
        'laud_on': load_image('buttons/60x60_btn_laud_on.png'),
        'laud_off': load_image('buttons/60x60_btn_laud_off.png'),
        }

font_positions = {'Новая игра': [420, 327],
                  'Продолжить': [410, 327],
                  'Уровни': [464, 477],
                  }

btns_now = ['Новая игра', 'Уровни', 'laud_off']
fonts_now = ['Новая игра', 'Уровни']


class Menu:
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon/bg_logo.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        for btn in btns_now:
            Button(btns[btn], btns_positions[btn], btn_menu_sprites)
        btn_menu_sprites.draw(screen)
        btn_menu_sprites.update()

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 53)
        for button in fonts_now:
            string_rendered = font.render(button, 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = font_positions[button][1]
            text_rect.x = font_positions[button][0]
            screen.blit(string_rendered, text_rect)


class LevelsMenu:
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon/bg.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        Button(btns[btns_now[2]], btns_positions[btns_now[2]], btn_levels_sprites)
        for circle in circles_pos:
            Button(btns['circle'], circle, btn_levels_sprites)
        for btn in btns_levels_pos:
            Button(btns['100x100'], btn, btn_levels_sprites)
        btn_levels_sprites.draw(screen)
        btn_levels_sprites.update()

        font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 70)
        for button in range(1, 6):
            string_rendered = font.render(str(button), 3, (122, 63, 0))
            text_rect = string_rendered.get_rect()
            text_rect.top = btns_levels_pos[button - 1][1] + 20
            text_rect.x = btns_levels_pos[button - 1][0] + 35
            screen.blit(string_rendered, text_rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, coords, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(coords[0], coords[1])


def start_levels_menu():
    global condition
    condition = 'levels'


def laud_control():
    if btns_now[2] == 'laud_off':
        btns_now[2] = 'laud_on'
    else:
        btns_now[2] = 'laud_off'


def click_check(coords):
    for ind, button in enumerate(btns_positions):
        btn = btns_positions[button]
        if (btn[0] < coords[0] < btn[0] + btn[2] and
                btn[1] < coords[1] < btn[1] + btn[3]):
            if ind == 0 or ind == 1:
                break
            elif ind == 2:
                start_levels_menu()
            elif ind == 3 or ind == 4:
                laud_control()
                break


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_check(event.pos)

        if condition == 'menu':
            Menu()
        elif condition == 'levels':
            LevelsMenu()

        pygame.display.flip()
        clock.tick(15)

terminate()
