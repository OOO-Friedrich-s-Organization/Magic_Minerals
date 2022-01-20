import pygame
import sys
import os
import random

pygame.init()
FPS = 15
WIDTH = 1080
HEIGHT = 720
STEP = 10

NECES_PAD_X = 5
NECES_PAD_Y = 8
INSTR_PAD_X = 900
INSTR_PAD_Y = 200
BOARD_X = 170
BOARD_Y = 20

first_time = True
first_time_in_ore = True
victory = False
double_stones_in_ores = True

# группы спрайтов
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Minerals')
clock = pygame.time.Clock()
background_image = pygame.image.load('assets/fon/bg.png')

all_sprites = pygame.sprite.Group()
animated_group = pygame.sprite.Group()
checkmark_group = pygame.sprite.Group()
stones_group = pygame.sprite.Group()
fly_stones_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
fon_sprites = pygame.sprite.Group()
necessary_stones = []  # список необходимых камней (объектов класса NecessaryStone)
necessary_stones_group = pygame.sprite.Group()
instruments_group = pygame.sprite.Group()

loaded_images = {}

all_sprites.add(pygame.sprite.Sprite())


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
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))


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
    fon_sprites.draw(screen)
    board.render(screen)
    stones_group.draw(screen)


def draw_instruments():
    pygame.draw.rect(screen, pygame.Color('brown'), (INSTR_PAD_X, INSTR_PAD_Y, 90, 360), 0)
    pygame.draw.rect(screen, pygame.Color('wheat'), (INSTR_PAD_X, INSTR_PAD_Y, 90, 360), 3)
    for i in range(4):
        if first_time:
            instrument_quadra.append(Instrument(instruments[i], 0, i))
        else:
            if instrument_quadra[i].active:
                pygame.draw.ellipse(screen, pygame.Color('skyblue'), (INSTR_PAD_X, INSTR_PAD_Y + 90 * i, 90, 90), 0)
            else:
                pygame.draw.ellipse(screen, pygame.Color('lightsalmon'), (INSTR_PAD_X, INSTR_PAD_Y + 90 * i, 90, 90), 0)
            if instrument_quadra[i].used:
                pygame.draw.ellipse(screen, pygame.Color('red'), (INSTR_PAD_X, INSTR_PAD_Y + 90 * i, 90, 90), 0)
            pygame.draw.ellipse(screen, pygame.Color('wheat'), (INSTR_PAD_X, INSTR_PAD_Y + 90 * i, 90, 90), 2)
    instruments_group.draw(screen)


def draw_fly_stones():
    for i in range(30):
        st = str(random.randint(1, 6))
        x, y = random.randint(0, 100), random.randint(0, 100)
        stone = FlyStone(st, x, y)


def to_statistic(stone_num, quantity, prize=False):
    for st in necessary_stones:
        if st.tile_type == stone_num:
            st.text[0] += quantity
    if prize:
        extra = 7
    else:
        extra = 1
    if stone_num in necessary_stones:
        game_result.update_score(15 * quantity * extra)
    else:
        game_result.update_score(5 * quantity * extra)


def write_statistic(*stones):
   # text = ''
    text = []
    x, y = NECES_PAD_X, NECES_PAD_Y
    coeff = 10
    global first_time
    if first_time:
        for stone in stones:
            st = NecessaryStone(stone[0], x, y, stone[1])
            necessary_stones.append(st)
            text.append(f'0/{stone[1]}')
            # text += ' ' * coeff + f'0/{stone[1]}'
            y += 2
            # coeff = 19
            first_time = False
    else:
        for stone in necessary_stones:
           # text += ' ' * coeff + f'{stone.text[0]}/{stone.text[1]}'
            text.append(f'{stone.text[0]}/{stone.text[1]}')
            y += 2
            coeff = 19
            if stone.text[0] >= stone.text[1]:
                cm = Checkmark(stone.x, stone.y)
   # text = [text]
    font = pygame.font.Font(None, 30)
    text_coord = BOARD_Y + 50
    necessary_stones_group.draw(screen)
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        text_rect = string_rendered.get_rect()
        text_coord += 120
        text_rect.x = BOARD_X - 110
        text_rect.top = text_coord
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)
    count = 0
    for stone in necessary_stones:
        if stone.text[0] >= stone.text[1]:
            count += 1
    if count == len(necessary_stones):
        game_result.victory()


stone_images = {
    '0': load_image('none.png'), '1': load_image('amber.png'),
    '2': load_image('amethyst.png'), '3': load_image('diamond.png'),
    '4': load_image('emerald.png'), '5': load_image('ruby.png'),
    '6': load_image('sapphire.png'), '7': load_image('ore_1.png'),
    '8': load_image('ore_2.png'), '9': load_image('ore_3.png'), '$': load_image('double_stone.png')
}

instrument_animations = {'pikhouweel': load_image('pikhouweel_animate.png', directory='assets/animations'),
                         'boren': load_image('boren_animate.png', directory='assets/animations'),
                         'dinamite': load_image('dinamite_animate.png', directory='assets/animations'),
                         'lantern': load_image('lantern_animate.png', directory='assets/animations')}

instruments = ['pikhouweel', 'boren', 'dinamite', 'lantern']
instrument_images = {}
instrument_quadra = []
lighted_cells = []

for i in range(1, 10):
    stone_images[str(i)] = pygame.transform.scale(stone_images[str(i)], (75, 75))
stone_images['$'] = pygame.transform.scale(stone_images['$'], (75, 75))

for ins in instruments:
    instrument_images[ins] = load_image(f'{ins}.png', directory='assets/instruments')
    instrument_images[ins] = pygame.transform.scale(instrument_images[ins], (90, 90))


tile_width = tile_height = 75


class Board:
    def __init__(self, width, height,
                 left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = load_level('level_1.txt')
        self.org_board = self.board[:]
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.c1 = (None, None)
        self.c2 = (None, None)
        self.ore_coords = []

        with open('stones/fall.txt', 'rt') as f:
            file = f.readlines()
        self.queue = list(file[0])
        self.global_del_list = []

    def next_in_queue(self, stone):
        if stone != '0':
            next = self.queue[0]
            del self.queue[0]
        else:
            next = '0'
        return next

    def find_ores(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == '7':
                    self.ore_coords.append((y, x))

    def check_near_ores(self, del_list, it_is_stone=False):
        allowed = False
        a = 0
        b = 1
        for ore in self.ore_coords:
            next_ore = False
            for st in del_list:
                if next_ore:
                    break
                if it_is_stone:
                    if st == ore:
                        allowed = True
                else:
                    if st[0] + 1 == ore[a] and st[1] == ore[b] or \
                            st[0] - 1 == ore[a] and st[1] == ore[b] or \
                            st[0] == ore[a] and st[1] + 1 == ore[b] or \
                            st[0] == ore[a] and st[1] - 1 == ore[b]:
                        allowed = True
                if allowed:
                    o = self.board[ore[a]][ore[b]]
                    o = str(int(o) + 1)
                    if o == '10':
                        if double_stones_in_ores:
                            sym = '$'
                        else:
                            sym = self.next_in_queue(1)
                        # self.ore_coords.pop(self.ore_coords.index(st))
                        line = list(self.board[ore[a]])
                        line[ore[b]] = sym
                        self.board[ore[a]] = ''.join(line)
                        del self.ore_coords[self.ore_coords.index(ore)]
                    else:
                        line = list(self.board[ore[a]])
                        line[ore[b]] = o
                        self.board[ore[a]] = ''.join(line)
                    next_ore = True
                    allowed = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        global first_time_in_ore
        if first_time_in_ore:
            self.find_ores()
            first_time_in_ore = False
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != '0':
                    pygame.draw.rect(screen, pygame.Color('white'),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 1)
                if self.board[y][x] in ['7', '8', '9']:
                    pygame.draw.rect(screen, pygame.Color('yellowgreen'),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                if self.board[y][x] == '$':
                    pygame.draw.rect(screen, pygame.Color('pink'),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                if (y, x) in lighted_cells:
                    pygame.draw.rect(screen, pygame.Color('skyblue'),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
        for lst in self.global_del_list:
            for x, y in lst:
                boom = AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                      3, 1, BOARD_X + y * self.cell_size, BOARD_Y + x * self.cell_size)

    def activate_double_stone(self):
        for line in self.board:
            if '$' in line:
                lst_index_dblst = []
                lst_index = self.board.index(line)
                i = 0
                for elem in line:
                    if elem == "$":
                        lst_index_dblst.append(i)
                    i += 1
                #cell = (line.index("$"), )
                for elem in lst_index_dblst:
                    cell = (lst_index, elem)
                    lines = []
                    faze = -1
                    if cell[0] - 1 > -1:
                        lines.append(self.board[cell[0] - 1])
                    else:
                        faze = 0
                    lines.append(self.board[cell[0]])
                    if cell[0] + 1 < 8:
                        lines.append(self.board[cell[0] + 1])
                    for line in lines:
                        if cell[1] - 1 > -1:
                            if (cell[0] + faze, cell[1] - 1) not in lighted_cells and\
                                    self.board[cell[0] + faze][cell[1] - 1] != '0':
                                lighted_cells.append((cell[0] + faze, cell[1] - 1))
                        if (cell[0] + faze, cell[1]) not in lighted_cells and\
                                self.board[cell[0] + faze][cell[1]] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1]))
                        if cell[1] + 1 < self.width:
                            if (cell[0] + faze, cell[1] + 1) not in lighted_cells and\
                                    self.board[cell[0] + faze][cell[1] + 1] != '0':
                                lighted_cells.append((cell[0] + faze, cell[1] + 1))
                        faze += 1
                self.horizontal_reduce()
                self.vertical_reduce()

    def tools_into_battle(self, cell):
        for ins in instrument_quadra:
            if ins.active and not ins.used:
                if ins.name in ['lantern', 'dynamite']:
                    an = AnimatedSprite(instrument_animations[ins.name], 6, 1,
                                        BOARD_X + cell[1] * self.cell_size, BOARD_Y + cell[0] * self.cell_size,
                                        big=True)
                else:
                    an = AnimatedSprite(instrument_animations[ins.name], 6, 1,
                                        BOARD_X + cell[1] * self.cell_size, BOARD_Y + cell[0] * self.cell_size)
                if ins.name == 'pickaxe' and not ins.used:
                    to_statistic(self.board[cell[0]][cell[1]], 1)
                    if cell in lighted_cells:
                        to_statistic(self.board[cell[0]][cell[1]], 1)
                    line = list(self.board[cell[0]])
                    if self.board[cell[0]][cell[1]] not in ['7', '8', '9', '$']:
                        line[cell[1]] = self.next_in_queue(line[cell[1]])
                        self.board[cell[0]] = ''.join(line)
                    else:
                        self.check_near_ores([(cell[0], cell[1])], it_is_stone=True)

                    instrument_quadra[instruments.index(ins.name)].used = True
                    boom = AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                          3, 1, BOARD_X + cell[1] * self.cell_size, BOARD_Y + cell[0] * self.cell_size)
                elif ins.name == 'drill' and not ins.used:
                    i = 0
                    for elem in self.board[cell[0]]:
                        to_statistic(elem, 1)
                        if tuple([cell[0], i]) in lighted_cells:
                            to_statistic(elem, 1)
                        i += 1
                    line = list(self.board[cell[0]])
                    for i in range(self.width):
                        if line[i] not in ['7', '8', '9', '$']:
                            line[i] = self.next_in_queue(line[i])
                        else:
                            self.check_near_ores([tuple([(cell[0]), i])], it_is_stone=True)
                            line[i] = self.board[cell[0]][i]
                        self.board[cell[0]] = ''.join(line)
                        AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                              3, 1, BOARD_X + i * self.cell_size, BOARD_Y + cell[0] * self.cell_size)
                    instrument_quadra[instruments.index(ins.name)].used = True
                elif ins.name == 'dynamite':
                    lines = []
                    faze = -1
                    if cell[0] - 1 > -1:
                        lines.append(self.board[cell[0] - 1])
                    else:
                        faze = 0
                    lines.append(self.board[cell[0]])
                    if cell[0] + 1 < 8:
                        lines.append(self.board[cell[0] + 1])
                    for line in lines:
                        ln_index = self.board.index(line)
                        l = list(self.board[ln_index])
                        if cell[1] - 1 > -1:
                            to_statistic(l[cell[1] - 1], 1)
                            if tuple([ln_index, cell[1] - 1]) in lighted_cells:
                                to_statistic(l[cell[1] - 1], 1)
                            if l[cell[1] - 1] not in ['7', '8', '9', '$']:
                                l[cell[1] - 1] = self.next_in_queue(l[cell[1] - 1])
                            else:
                                self.check_near_ores([(ln_index, cell[1] - 1)], it_is_stone=True)
                                l[cell[1] - 1] = self.board[ln_index][cell[1] - 1]
                            AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                                  3, 1, BOARD_X + (cell[1] - 1) * self.cell_size,
                                                  BOARD_Y + (cell[0] + faze) * self.cell_size)
                        to_statistic(l[cell[1]], 1)
                        if tuple([ln_index, cell[1]]) in lighted_cells:
                            to_statistic(l[cell[1]], 1)
                        if l[cell[1]] not in ['7', '8', '9', '$']:
                            l[cell[1]] = self.next_in_queue(l[cell[1]])
                        else:
                            self.check_near_ores([(ln_index, cell[1])], it_is_stone=True)
                            l[cell[1]] = self.board[ln_index][cell[1]]
                        AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                              3, 1, BOARD_X + cell[1] * self.cell_size,
                                              BOARD_Y + (cell[0] + faze) * self.cell_size)
                        if cell[1] + 1 < self.width:
                            to_statistic(l[cell[1] + 1], 1)
                            if tuple([ln_index, cell[1] + 1]) in lighted_cells:
                                to_statistic(l[cell[1] + 1], 1)
                            if l[cell[1] + 1] not in ['7', '8', '9', '$']:
                                l[cell[1] + 1] = self.next_in_queue(l[cell[1] + 1])
                            else:
                                self.check_near_ores([(ln_index, cell[1] + 1)], it_is_stone=True)
                                l[cell[1] + 1] = self.board[ln_index][cell[1] + 1]
                            AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
                                                  3, 1, BOARD_X + (cell[1] + 1) * self.cell_size,
                                                  BOARD_Y + (cell[0] + faze) * self.cell_size)
                        self.board[ln_index] = ''.join(l)
                        faze += 1
                    instrument_quadra[instruments.index(ins.name)].used = True
                elif ins.name == 'lantern':
                    lines = []
                    faze = -1
                    if cell[1] - 1 > -1:
                        lines.append(self.board[cell[0] - 1])
                    else:
                        faze = 0
                    lines.append(self.board[cell[0]])
                    if cell[1] + 1 < 8:
                        lines.append(self.board[cell[0] + 1])
                    for line in lines:
                        l = list(self.board[self.board.index(line)])
                        if cell[1] - 1 > -1 and self.board[cell[0] + faze][cell[1] - 1] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1] - 1))
                        if self.board[cell[0] + faze][cell[1]] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1]))
                        if cell[1] + 1 < 8 and self.board[cell[0]+ faze][cell[1] + 1] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1] + 1))
                        faze += 1
                    instrument_quadra[instruments.index(ins.name)].used = True
                self.horizontal_reduce()
                self.vertical_reduce()
                [st.kill() for st in stones_group]
            ins.active = False
            self.vertical_reduce()
            self.horizontal_reduce()
        instrument_pad.active_instrument = None

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
            if c1 not in self.ore_coords and c2 not in self.ore_coords and\
                    self.board[c1[0]][c1[1]] not in ['7', '8', '9', '$'] and\
                    self.board[c2[0]][c2[1]] not in ['7', '8', '9', '$']:
                if c1[0] == c2[0] and abs(c1[1] - c2[1]) == 1:
                    line1 = list(self.board[c1[0]])
                    stone1, stone2 = line1[c1[1]], line1[c2[1]]
                    if c1[1] < c2[1]:
                        del line1[c1[1]]
                        del line1[c2[1] - 1]
                        line1.insert(c2[1] - 1, stone1)
                        line1.insert(c1[1], stone2)
                    else:
                        del line1[c2[1]]
                        del line1[c1[1] - 1]
                        line1.insert(c1[1] - 1, stone2)
                        line1.insert(c2[1], stone1)
                    line1 = ''.join(line1)
                    old_line = self.board[self.c1[0]][:]
                    self.board[self.c1[0]] = line1
                    # i, j = self.c1[1], 0
                    # count = 1
                    # cur_st = self.board[i][j]
                    # while j < self.width:
                    #     j += 1
                    #     if j == self.width - 1:
                    #         break
                    #     if self.board[i][j] == cur_st:
                    #         while self.board[i][j] == cur_st:
                    #             count += 1
                    #             j += 1
                    #             if j == self.width - 1:
                    #                 break
                    #     else:
                    #         cur_st = self.board[i][j]
                    # if count >= 3:
                    self.horizontal_reduce()
                    self.vertical_reduce()
                    # else:
                    #     self.board[self.c1[1]] = old_line
                elif c1[1] == c2[1] and abs(c1[0] - c2[0]) == 1:
                    line1, line2 = list(self.board[c1[0]]), list(self.board[c2[0]])
                    stone1, stone2 = line1[c1[1]], line2[c2[1]]
                    del line1[c1[1]]
                    del line2[c2[1]]
                    line1.insert(c2[1], stone2)
                    line2.insert(c1[1], stone1)
                    line1, line2 = ''.join(line1), ''.join(line2)
                    self.board[c1[0]], self.board[c2[0]] = line1, line2
                    self.horizontal_reduce()
                    self.vertical_reduce()
                move_pad.minus()
                board.horizontal_reduce()
                board.vertical_reduce()
        self.tools_into_battle(cell)
        self.activate_double_stone()

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_y, cell_x   #row, col

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and self.board[cell[0]][cell[1]] != '0':
            self.on_click(cell)

    # def check_move_possibility(self, old_board):
    #     i, j = self.c1[1], 0
    #     count = 1
    #     cur_st = self.board[i][j]
    #     while j < self.width:
    #         j += 1
    #         if j == self.width - 1:
    #             break
    #         if self.board[i][j] == cur_st:
    #             while self.board[i][j] == cur_st:
    #                 count += 1
    #                 j += 1
    #                 if j == self.width - 1:
    #                     break
    #         else:
    #             cur_st = self.board[i][j]
    #     if count >= 3:
    #         self.horizontal_reduce()
    #         self.vertical_reduce()
    #     else:
    #         self.board = old_board

    def horizontal_reduce(self):
        i, j = 0, 0
        while i < self.height:
            del_list = []
            while j < self.width:
                cur_st = self.board[i][j]
                if cur_st != '0':
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
                            score = 0
                            prize = False
                            for st in del_list:
                                if st in lighted_cells:
                                    score += 2
                                    prize = True
                                else:
                                    score += 1
                            to_statistic(cur_st, score, prize=prize)
                        else:  # последовательность меньше 3-х удаляем из списка удалений
                            if j < self.width:
                                cur_st = self.board[i][j]
                            del_list = []
                    else:
                        cur_st = self.board[i][j]
                        del_list = []
                    if len(del_list) >= 3:
                        self.global_del_list.append(del_list)
                        tmp_line = list(self.board[i])
                        for tpl in del_list:
                            tmp_line[tpl[1]] = self.next_in_queue(tmp_line[tpl[1]])
                        tmp_line = ''.join(tmp_line)
                        self.board[i] = tmp_line
                        self.check_near_ores(del_list)
                        del_list = []
                else:
                    j += 1
            i += 1
            j = 0

    def vertical_reduce(self):
        i, j = 0, 0
        while j < self.height:
            del_list = []
            while i < self.width:
                cur_st = self.board[i][j]
                if cur_st != '0':
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
                            score = 0
                            prize = False
                            for st in del_list:
                                if st in lighted_cells:
                                    score += 2
                                    prize = True
                                else:
                                    score += 1
                            to_statistic(cur_st, score, prize=prize)
                        else:  # последовательность меньше 3-х удаляем из списка удалений
                            if i < self.height:
                                cur_st = self.board[i][j]
                            del_list = []
                    else:
                        cur_st = self.board[i][j]
                        del_list = []
                    if len(del_list) >= 3:
                        # tmp_line = list(self.board[i])
                        self.global_del_list.append(del_list)
                        for tpl in del_list:
                            tmp_line = list(self.board[tpl[0]])
                            tmp_line[tpl[1]] = self.next_in_queue(tmp_line[tpl[1]])
                            tmp_line = ''.join(tmp_line)
                            self.board[tpl[0]] = tmp_line
                        self.check_near_ores(del_list)
                        del_list = []
                else:
                    i += 1
            j += 1
            i = 0


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, fon_sprites)
        self.image = load_image(name='bg.png', directory='assets/fon')
        self.rect = self.image.get_rect().move(0, 0)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, big=False):
        super().__init__(animated_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.c = 1
        if big:
            self.c = 3
            x -= 90
            y -= 90
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (90 * self.c, 90 * self.c))
        self.rect = self.rect.move(x, y)
        self.i = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.i < len(self.frames):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (90 * self.c, 90 * self.c))
            self.i += 1
        else:
            self.kill()
            board.on_click(board.c1)


class Checkmark(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(checkmark_group, all_sprites)
        self.image = pygame.transform.scale(load_image('checkmark.png'), (60, 45))
        self.rect = self.image.get_rect().move(
            5 + tile_width * pos_x, 30 + tile_height * pos_y)


class Stone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(stones_group, all_sprites)
        self.image = stone_images[tile_type]
        self.rect = self.image.get_rect().move(
            BOARD_X + tile_width * pos_x, BOARD_Y + tile_height * pos_y)


class NecessaryStone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, need):
        super().__init__(necessary_stones_group, all_sprites)
        self.tile_type = tile_type
        self.image = stone_images[tile_type]
        self.text = [0, need]
        self.rect = self.image.get_rect().move(
           # BOARD_X + tile_width * pos_x, BOARD_Y + tile_height * pos_y)
            BOARD_X - 100, BOARD_Y - 525 + tile_height * pos_y)
        self.x, self.y = pos_x, pos_y


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class FlyStone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(fly_stones_group, all_sprites)
        self.tile_type = tile_type
        self.image = stone_images[tile_type]
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Instrument(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(instruments_group, all_sprites)
        self.name = tile_type
        self.image = instrument_images[tile_type]
        self.animation = instrument_animations[tile_type]
        self.rect = self.image.get_rect().move(
            INSTR_PAD_X, INSTR_PAD_Y + 90 * pos_y)
        self.active = False
        self.used = False


class InstrumentPad:
    def __init__(self):
        self.width, self.height = 1, 4
        self.cell_size = 90
        self.left, self.top = INSTR_PAD_X, INSTR_PAD_Y
        self.mouse_pos = (0, 0)
        self.active_instrument = None

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        self.mouse_pos = mouse_pos
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        if self.get_cell(self.mouse_pos) == cell:
            if not self.active_instrument:
                instrument_quadra[cell[1]].active = True
                self.active_instrument = instrument_quadra[cell[1]]


class Move:
    def __init__(self, n):
        self.n = n

    def minus(self):
        self.n -= 1
        if self.n < 0:
            self.n = 0

    def show(self):
        pygame.draw.ellipse(screen, 'YellowGreen', (INSTR_PAD_X, INSTR_PAD_Y - 110, 90, 90), 0)
        pygame.draw.ellipse(screen, 'DarkGreen', (INSTR_PAD_X, INSTR_PAD_Y - 110, 90, 90), 5)
        text = [str(self.n).rjust(2, ' ')]
        font = pygame.font.Font(None, 70)
        text_coord = 17
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('DarkGreen'))
            text_rect = string_rendered.get_rect()
            text_coord += 10
            text_rect.top = INSTR_PAD_Y - 90#text_coord
            text_rect.x = INSTR_PAD_X + 15
            text_coord += text_rect.height
            screen.blit(string_rendered, text_rect)


class WinOrDefeat:
    def __init__(self, moves):
        self.moves = moves
        self.score = 0

    def check_moves(self):
        if self.moves == 0 and not victory:
            self.defeat()

    def update_score(self, plus):
        self.score += plus

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
        global victory
        text = 'Изумительно!' if self.moves < 3 else 'Прелестно!'
        font = pygame.font.Font(None, 200)
        text_coord = 17
        string_rendered = font.render(text, 1, pygame.Color('White'))
        text_rect = string_rendered.get_rect()
        text_rect.top = text_coord
        text_rect.x = 10
        screen.blit(string_rendered, text_rect)
        victory = True
        draw_fly_stones()


Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH- 5, 5, WIDTH - 5, HEIGHT - 5)

board = Board(8, 8, BOARD_X, BOARD_Y, 75)
instrument_pad = InstrumentPad()
move_pad = Move(20)
running = True
game_result = WinOrDefeat(move_pad.n)
while running:
    level_x, level_y = generate_level(board.board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
            instrument_pad.get_click(event.pos)
    # board.horizontal_reduce()
    # board.vertical_reduce()
    draw_cell_field()
    draw_instruments()
    move_pad.show()
    write_statistic(('5', 10), ('6', 15), ('4', 20))
    game_result.check_moves()
    fly_stones_group.draw(screen)
    fly_stones_group.update()
    animated_group.draw(screen)
    animated_group.update()
    checkmark_group.draw(screen)
    pygame.display.flip()
    #screen.fill('black')
    screen.blit(background_image, (0, 0))
    clock.tick(FPS)
terminate()
