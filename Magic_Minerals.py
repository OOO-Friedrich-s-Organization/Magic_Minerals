import pygame
import sys
import os

pygame.init()
FPS = 50
WIDTH = 1080
HEIGHT = 720
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Minerals')
clock = pygame.time.Clock()

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
necessary_stones_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    full_name = os.path.join('stones', name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print(f'В папке отсутствует файл {name}')
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join('stones', filename)
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(level[y][x], x, y)
    return x, y


def terminate():
    pygame.quit()
    sys.exit()


def draw_cell_field():
    for y in range(6):
        for x in range(6):
            pygame.draw.rect(screen, pygame.Color('white'),
                             (10 + x * tile_width,
                              10 + y * tile_height,
                              tile_width, tile_height), 1)


def write_statistic(*stones):
    text = ''
    x, y = 0, 6
    for stone in stones:
        NecessaryStone(stone[0], x, y)
        text += f'          0/{stone[1]}'
        x += 1.3
    text = [text]
    font = pygame.font.Font(None, 30)
    text_coord = 500
    necessary_stones_group.draw(screen)
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        text_rect = string_rendered.get_rect()
        text_coord += 10
        text_rect.top = text_coord
        text_rect.x = 10
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)


tile_images = {
    '1': load_image('amber.png'),
    '2': load_image('amethyst.png'), '3': load_image('diamond.png'),
    '4': load_image('emerald.png'), '5': load_image('ruby.png'),
    '6': load_image('sapphire.png'),
}
for i in range(1, 7):
    tile_images[str(i)] = pygame.transform.scale(tile_images[str(i)], (75, 75))

tile_width = tile_height = 75


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            10 + tile_width * pos_x, 10 + tile_height * pos_y)


class NecessaryStone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(necessary_stones_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            10 + tile_width * pos_x, 10 + tile_height * pos_y)


level_x, level_y = generate_level(load_level('level.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    draw_cell_field()
    write_statistic(('5', 10), ('6', 15), ('1', 20))
    tiles_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
