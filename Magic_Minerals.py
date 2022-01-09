import pygame
import sys
import os

pygame.init()
FPS = 50
WIDTH = 1080
HEIGHT = 720
STEP = 10

first_time = True

# группы спрайтов
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Minerals')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
animated_group = pygame.sprite.Group()
stones_group = pygame.sprite.Group()
necessary_stones = []  # список необходимых камней (объектов класса NecessaryStone)
necessary_stones_group = pygame.sprite.Group()
instruments_group = pygame.sprite.Group()

loaded_images = {}


def load_image(name,  directory='stones', color_key=None):
    full_name = os.path.join(directory, name)
    if full_name not in loaded_images.keys():
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
        loaded_images[full_name] = image
        return image
    else:
        return loaded_images[full_name]


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
            Stone(level[y][x], x, y)
    return x, y


def terminate():
    pygame.quit()
    sys.exit()


def draw_cell_field():
    board.render(screen)
    stones_group.draw(screen)
    # animated_group.draw(screen)
    # animated_group.update()
    # [b.kill() for b in animated_group]


def draw_instruments():
    pygame.draw.rect(screen, pygame.Color('brown'), (630, 130, 90, 360), 0)
    pygame.draw.rect(screen, pygame.Color('wheat'), (630, 130, 90, 360), 3)
    for i in range(4):
        pygame.draw.ellipse(screen, pygame.Color('lightsalmon'), (630, 130 + 90 * i, 90, 90), 0)
        pygame.draw.ellipse(screen, pygame.Color('wheat'), (630, 130 + 90 * i, 90, 90), 2)
        Instrument(instruments[i], 0, i)
    instruments_group.draw(screen)


def to_statistic(stone_num, quantity):
    for st in necessary_stones:
        if st.tile_type == stone_num:
            st.text[0] += quantity


def write_statistic(*stones):
    text = ''
    x, y = 0, 8
    coeff = 10
    global first_time
    if first_time:
        for stone in stones:
            st = NecessaryStone(stone[0], x, y, stone[1])
            necessary_stones.append(st)
            text += ' ' * coeff + f'0/{stone[1]}'
            x += 2
            coeff = 19
            first_time = False
    else:
        for stone in necessary_stones:
            text += ' ' * coeff + f'{stone.text[0]}/{stone.text[1]}'
            x += 2
            coeff = 19
    text = [text]
    font = pygame.font.Font(None, 30)
    text_coord = 650
    necessary_stones_group.draw(screen)
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        text_rect = string_rendered.get_rect()
        text_coord += 10
        text_rect.top = text_coord
        text_rect.x = 10
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)
    count = 0
    for stone in necessary_stones:
        if stone.text[0] >= stone.text[1]:
            count += 1
    if count == len(necessary_stones):
        game_result.victory()


stone_images = {
    '1': load_image('amber.png'),
    '2': load_image('amethyst.png'), '3': load_image('diamond.png'),
    '4': load_image('emerald.png'), '5': load_image('ruby.png'),
    '6': load_image('sapphire.png'),
}

instruments = ['pickaxe', 'drill', 'dynamite', 'lantern']
instrument_images = {}

for i in range(1, 7):
    stone_images[str(i)] = pygame.transform.scale(stone_images[str(i)], (75, 75))

for ins in instruments:
    instrument_images[ins] = load_image(f'{ins}.png', directory='assets/instruments')
    instrument_images[ins] = pygame.transform.scale(instrument_images[ins], (90, 90))


tile_width = tile_height = 75


class Board:
    def __init__(self, width, height,
                 left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = load_level('level.txt')
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.c1 = (None, None)
        self.c2 = (None, None)
        with open('stones/fall.txt', 'rt') as f:
            file = f.readlines()
        self.queue = list(file[0])
        self.global_del_list = []

    def next_in_queue(self):
        next = self.queue[0]
        del self.queue[0]
        return next

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.c1:
                    pygame.draw.rect(screen, pygame.Color('lightgreen'),
                                     (self.left + self.c1[0] * self.cell_size,
                                      self.top + self.c1[1] * self.cell_size, self.cell_size, self.cell_size), 0)
                if (x, y) == self.c2:
                    pygame.draw.rect(screen, pygame.Color('pink'),
                                     (self.left + self.c2[0] * self.cell_size,
                                      self.top + self.c2[1] * self.cell_size, self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

        for lst in self.global_del_list:
            for x, y in lst:
                pygame.draw.rect(screen, pygame.Color('Khaki'),
                                 (self.left + y * self.cell_size,
                                  self.top + x * self.cell_size, self.cell_size, self.cell_size), 0)
                boom = AnimatedSprite(load_image("boom.jpg"), 6, 5, x * self.cell_size, y * self.cell_size)

    def on_click(self, cell):
        self.global_del_list = []
        if self.c1 == (None, None) and self.c2 == (None, None):
            self.c1 = cell
        elif self.c1 != (None, None) and self.c2 == (None, None):
            self.c2 = cell
        else:
            self.c1 = cell
            self.c2 = (None, None)
        if self.c1 != (None, None) and self.c2 != (None, None) and self.c1 != self.c2:
            [st.kill() for st in stones_group]
            c1, c2 = self.c1, self.c2
            # for i, st in enumerate(stones_group):
            #     if i == c1[0] * 8 + c1[1]:
            #         st.kill()
            #     if i == c2[0] * 8 + c2[1]:
            #         st.kill()
            if c1[1] == c2[1] and abs(c1[0] - c2[0]) == 1:
                line1 = list(self.board[c1[1]])
                stone1, stone2 = line1[c1[0]], line1[c2[0]]
                if c1[0] < c2[0]:
                    del line1[c1[0]]
                    del line1[c2[0] - 1]
                    line1.insert(c2[0] - 1, stone1)
                    line1.insert(c1[0], stone2)
                else:
                    del line1[c2[0]]
                    del line1[c1[0] - 1]
                    line1.insert(c1[0] - 1, stone2)
                    line1.insert(c2[0], stone1)
                line1 = ''.join(line1)
                self.board[self.c1[1]] = line1
                self.horizontal_reduce()
                self.vertical_reduce()
            elif c1[0] == c2[0] and abs(c1[1] - c2[1]) == 1:
                line1, line2 = list(self.board[c1[1]]), list(self.board[c2[1]])
                stone1, stone2 = line1[c1[0]], line2[c2[0]]
                del line1[c1[0]]
                del line2[c2[0]]
                line1.insert(c2[0], stone2)
                line2.insert(c1[0], stone1)
                line1, line2 = ''.join(line1), ''.join(line2)
                self.board[c1[1]], self.board[c2[1]] = line1, line2
                self.horizontal_reduce()
                self.vertical_reduce()
            move_pad.minus()

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def horizontal_reduce(self):
        i, j = 0, 0
        while i < self.height:
            del_list = []
            while j < self.width:
                cur_st = self.board[i][j]
                del_list.append((i, j))
                j += 1
                if j == self.width:
                    break
                if self.board[i][j] == cur_st:
                    while self.board[i][j] == cur_st:
                        del_list.append((i, j))
                        j += 1
                        if j == self.width:
                            break
                    if len(del_list) >= 3:
                        to_statistic(cur_st, len(del_list))
                else:
                    cur_st = self.board[i][j]
                    del_list = []
                if len(del_list) >= 3:
                    self.global_del_list.append(del_list)
                    tmp_line = list(self.board[i])
                    for tpl in del_list:
                        tmp_line[tpl[1]] = self.next_in_queue()
                    tmp_line = ''.join(tmp_line)
                    self.board[i] = tmp_line
                    del_list = []
            i += 1
            j = 0

    def vertical_reduce(self):
        i, j = 0, 0
        while j < self.height:
            del_list = []
            while i < self.width:
                cur_st = self.board[i][j]
                del_list.append((i, j))
                i += 1
                if i == self.height:
                    break
                if self.board[i][j] == cur_st:
                    while self.board[i][j] == cur_st:
                        del_list.append((i, j))
                        i += 1
                        if i == self.height:
                            break
                    if len(del_list) >= 3:
                        to_statistic(cur_st, len(del_list))
                else:
                    cur_st = self.board[i][j]
                    del_list = []
                if len(del_list) >= 3:
                    # tmp_line = list(self.board[i])
                    self.global_del_list.append(del_list)
                    for tpl in del_list:
                        tmp_line = list(self.board[tpl[0]])
                        tmp_line[tpl[1]] = self.next_in_queue()
                        tmp_line = ''.join(tmp_line)
                        self.board[tpl[0]] = tmp_line
                    del_list = []
            j += 1
            i = 0


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(animated_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Stone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(stones_group, all_sprites)
        self.image = stone_images[tile_type]
        self.rect = self.image.get_rect().move(
            10 + tile_width * pos_x, 10 + tile_height * pos_y)


class NecessaryStone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, need):
        super().__init__(necessary_stones_group, all_sprites)
        self.tile_type = tile_type
        self.image = stone_images[tile_type]
        self.text = [0, need]
        self.rect = self.image.get_rect().move(
            10 + tile_width * pos_x, 10 + tile_height * pos_y)


class Instrument(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(instruments_group, all_sprites)
        self.image = instrument_images[tile_type]
        self.rect = self.image.get_rect().move(
            630, 130 + 90 * pos_y)


class Move:
    def __init__(self, n):
        self.n = n

    def minus(self):
        self.n -= 1

    def show(self):
        pygame.draw.ellipse(screen, 'YellowGreen', (630, 10, 90, 90), 0)
        pygame.draw.ellipse(screen, 'DarkGreen', (630, 10, 90, 90), 5)
        text = [str(self.n).rjust(2, ' ')]
        font = pygame.font.Font(None, 70)
        text_coord = 17
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('DarkGreen'))
            text_rect = string_rendered.get_rect()
            text_coord += 10
            text_rect.top = text_coord
            text_rect.x = 645
            text_coord += text_rect.height
            screen.blit(string_rendered, text_rect)


class WinOrDefeat:
    def __init__(self, moves):
        self.moves = moves

    def check_moves(self):
        if self.moves == 0:
            self.defeat()

    def defeat(self):
        text = 'Неудача!'
        font = pygame.font.Font(None, 200)
        text_coord = 17
        string_rendered = font.render(text, 1, pygame.Color('White'))
        text_rect = string_rendered.get_rect()
        text_rect.top = text_coord
        text_rect.x = 10
        screen.blit(string_rendered, text_rect)

    def victory(self):
        text = 'Изумительно!' if self.moves < 3 else 'Прелестно!'
        font = pygame.font.Font(None, 200)
        text_coord = 17
        string_rendered = font.render(text, 1, pygame.Color('White'))
        text_rect = string_rendered.get_rect()
        text_rect.top = text_coord
        text_rect.x = 10
        screen.blit(string_rendered, text_rect)


board = Board(8, 8, 10, 10, 75)
move_pad = Move(20)
running = True
while running:
    game_result = WinOrDefeat(move_pad.n)
    level_x, level_y = generate_level(board.board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
    draw_cell_field()
    draw_instruments()
    move_pad.show()
    write_statistic(('5', 10), ('6', 15), ('4', 20))
    game_result.check_moves()
    pygame.display.flip()
    screen.fill('black')
    clock.tick(FPS)
terminate()
