import pygame
import os
import sys
# from level_generator import GamePlace


pygame.init()

WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_menu_sprites = pygame.sprite.Group()
btn_levels_sprites = pygame.sprite.Group()
levels_sprites = pygame.sprite.Group()


class Main:
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

        self.btns_now = ['Начать игру', 'Уровни', 'laud_off', 'back_btn']

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

    def click_check_levels_menu(self, coords):
        for ind, button in enumerate(self.btns_positions):
            btn = self.btns_positions[button]
            if (btn[0] < coords[0] < btn[0] + btn[2] and
                    btn[1] < coords[1] < btn[1] + btn[3]):
                if ind == 0:
                    self.condition = 'game'
                elif ind == 1:
                    self.condition = 'levels'
                elif ind == 2 or ind == 3:
                    self.laud_control()
                    break
                elif ind == 4:
                    self.condition = 'menu'

    def laud_control(self):
        if 'laud_off' in self.btns_now:
            self.btns_now[self.btns_now.index('laud_off')] = 'laud_on'
        else:
            self.btns_now[self.btns_now.index('laud_on')] = 'laud_off'


class Menu(Main):
    def __init__(self):
        super().__init__()
        fon = pygame.transform.scale(self.load_image('fon/bg_logo.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        for btn in self.btns_now[:-1]:
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


class LevelsMenu(Main):
    def __init__(self):
        super().__init__()
        fon = pygame.transform.scale(self.load_image('fon/bg.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

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


class Button(pygame.sprite.Sprite):
    def __init__(self, image, coords, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(coords[0], coords[1])


main = Main()
if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main.click_check_levels_menu(event.pos)

        if main.condition == 'menu':
            Menu()
        elif main.condition == 'levels':
            LevelsMenu()
        elif main.condition == 'game':
            GamePlace()

        pygame.display.flip()
        clock.tick(15)

main.terminate()
