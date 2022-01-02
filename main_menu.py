import pygame
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1080, 720
BUTTONS_COORDS = [[390, 300, 300, 100],
                  [390, 450, 300, 100],
                  [1000, 640, 60, 60]]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

levels_sprites = pygame.sprite.Group()

condition = 'menu'
levels = 8


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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


def menu_screen():
    for button in BUTTONS_COORDS:
        pygame.draw.rect(screen, (255, 175, 24),
                         (button[0], button[1], button[2], button[3]))
    buttons_text = {'Новая игра': [410, 330, 1],
                    'Уровни': [440, 480, 1],
                    'Продолжить': [394, 330, 0]}
    font = pygame.font.Font(None, 50)
    for button in buttons_text:
        if buttons_text[button][2]:
            string_rendered = font.render(button, 1, (255, 255, 255))
            text_rect = string_rendered.get_rect()
            text_rect.top = buttons_text[button][1]
            text_rect.x = buttons_text[button][0]
            screen.blit(string_rendered, text_rect)


def levels_screen():
    y, x = 200, 310
    for _ in range(levels // 4):
        for _ in range(4):
            pygame.draw.rect(screen, (255, 175, 24), (x, y, 100, 100))
            x += 120
        x = 310
        y += 120
    for _ in range(levels % 4):
        pygame.draw.rect(screen, (255, 175, 24), (x, y, 100, 100))
        x += 120
    font = pygame.font.Font(None, 70)
    y, x = 230, 340
    for text in range(1, levels + 1):
        string_rendered = font.render(str(text), 1, (255, 255, 255))
        text_rect = string_rendered.get_rect()
        text_rect.top = y
        text_rect.x = x
        screen.blit(string_rendered, text_rect)
        x += 120
        if text % 4 == 0:
            y += 120
            x = 340


def start_levels_menu():
    global condition
    condition = 'levels'


def click_check(coords):
    for ind, button in enumerate(BUTTONS_COORDS):
        if (button[0] < coords[0] < button[0] + button[2] and
                button[1] < coords[1] < button[1] + button[3]):
            if ind == 0:
                pass
            elif ind == 1:
                start_levels_menu()


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_check(event.pos)

        screen.fill((117, 66, 61))

        # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        # screen.blit(fon, (0, 0))
        if condition == 'menu':
            menu_screen()
        else:
            levels_screen()

        pygame.display.flip()

terminate()
