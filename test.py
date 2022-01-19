import pygame
import sys
import os


WIDTH, HEIGHT = 1080, 720

first_time = True
first_time_in_ore = True
victory = False
double_stones_in_ores = True


# def load_image(name,  directory='stones', color_key=None):
#     full_name = os.path.join(directory, name)
#     if full_name not in loaded_images.keys():
#         try:
#             image = pygame.image.load(full_name)
#         except pygame.error as message:
#             print(f'В папке отсутствует файл {name}')
#             raise SystemExit(message)
#
#         if color_key is not None:
#             if color_key == -1:
#                 color_key = image.get_at((0, 0))
#             image.set_colorkey(color_key)
#         else:
#             image = image.convert_alpha()
#         loaded_images[full_name] = image
#         return image
#     else:
#         return loaded_images[full_name]


# def load_level(filename):
#     filename = os.path.join('stones', filename)
#     # читаем уровень, убирая символы перевода строки
#     with open(filename, 'r') as mapFile:
#         level_map = [line.strip() for line in mapFile]
#
#     # и подсчитываем максимальную длину
#     max_width = max(map(len, level_map))
#
#     # дополняем каждую строку пустыми клетками ('.')
#     return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# def generate_level(level):
#     x, y = None, None
#     for y in range(len(level)):
#         for x in range(len(level[y])):
#             Stone(level[y][x], x, y)
#     return x, y


# def terminate():
#     pygame.quit()
#     sys.exit()


# def draw_cell_field():
#     fon_sprites.draw(screen)
#     board.render(screen)
#     stones_group.draw(screen)


# def draw_instruments():
#     pygame.draw.rect(screen, pygame.Color('brown'), (630, 130, 90, 360), 0)
#     pygame.draw.rect(screen, pygame.Color('wheat'), (630, 130, 90, 360), 3)
#     for i in range(4):
#         if first_time:
#             instrument_quadra.append(Instrument(instruments[i], 0, i))
#         else:
#             if instrument_quadra[i].active:
#                 pygame.draw.ellipse(screen, pygame.Color('skyblue'), (630, 130 + 90 * i, 90, 90), 0)
#             else:
#                 pygame.draw.ellipse(screen, pygame.Color('lightsalmon'), (630, 130 + 90 * i, 90, 90), 0)
#             if instrument_quadra[i].used:
#                 pygame.draw.ellipse(screen, pygame.Color('red'), (630, 130 + 90 * i, 90, 90), 0)
#             pygame.draw.ellipse(screen, pygame.Color('wheat'), (630, 130 + 90 * i, 90, 90), 2)
#     instruments_group.draw(screen)


# def write_statistic(*stones):
#     text = ''
#     x, y = 1.5, 8
#     coeff = 10
#     global first_time
#     if first_time:
#         for stone in stones:
#             st = NecessaryStone(stone[0], x, y, stone[1])
#             necessary_stones.append(st)
#             text += ' ' * coeff + f'0/{stone[1]}'
#             x += 2
#             coeff = 19
#             first_time = False
#     else:
#         for stone in necessary_stones:
#             text += ' ' * coeff + f'{stone.text[0]}/{stone.text[1]}'
#             x += 2
#             coeff = 19
#             if stone.text[0] >= stone.text[1]:
#                 cm = Checkmark(stone.x, stone.y)
#     text = [text]
#     font = pygame.font.Font(None, 30)
#     text_coord = 650
#     necessary_stones_group.draw(screen)
#     for line in text:
#         string_rendered = font.render(line, 1, pygame.Color('white'))
#         text_rect = string_rendered.get_rect()
#         text_coord += 10
#         text_rect.top = text_coord
#         text_rect.x = 130
#         text_coord += text_rect.height
#         screen.blit(string_rendered, text_rect)
#     count = 0
#     for stone in necessary_stones:
#         if stone.text[0] >= stone.text[1]:
#             count += 1
#     if count == len(necessary_stones):
#         game_result.victory()


# stone_images = {
#     '1': load_image('amber.png'),
#     '2': load_image('amethyst.png'), '3': load_image('diamond.png'),
#     '4': load_image('emerald.png'), '5': load_image('ruby.png'),
#     '6': load_image('sapphire.png'), '7': load_image('ore_1.png'),
#     '8': load_image('ore_2.png'), '9': load_image('ore_3.png'), '$': load_image('double_stone.png')
# }
#
# instrument_animations = {'pikhouweel': load_image('pikhouweel_animate.png', directory='assets/animations'),
#                          'boren': load_image('boren_animate.png', directory='assets/animations'),
#                          'dinamite': load_image('dinamite_animate.png', directory='assets/animations'),
#                          'lantern': load_image('lantern_animate.png', directory='assets/animations')}

# instruments = ['pikhouweel', 'boren', 'dinamite', 'lantern']
# instrument_images = {}
# instrument_quadra = []
#
# for i in range(1, 10):
#     stone_images[str(i)] = pygame.transform.scale(stone_images[str(i)], (75, 75))
# stone_images['$'] = pygame.transform.scale(stone_images['$'], (75, 75))
#
# for ins in instruments:
#     instrument_images[ins] = load_image(f'{ins}.png', directory='assets/instruments')
#     instrument_images[ins] = pygame.transform.scale(instrument_images[ins], (90, 90))


# tile_width = tile_height = 75


class Board:
    def __init__(self):
        self.c1 = (None, None)
        self.c2 = (None, None)
        self.width = 8
        self.height = 8
        self.ore_coords = []
        with open('stones/fall.txt', 'rt') as f:
            file = f.readlines()
        self.queue = list(file[0])
        self.global_del_list = []
        self.statistic_minerals = []

    def to_statistic(self, stone_num, quantity):
        for ind, st in enumerate(self.statistic_minerals):
            if st[0] == stone_num:
                self.statistic_minerals[ind][1] = str(int(self.statistic_minerals[ind][1]) + quantity)

    def next_in_queue(self):
        next = self.queue[0]
        del self.queue[0]
        return next

    # def find_ores(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             if self.board[y][x] == '7':
    #                 self.ore_coords.append((y, x))

    # def check_near_ores(self, del_list):
    #     for ore in self.ore_coords:
    #         next_ore = False
    #         for st in del_list:
    #             if next_ore:
    #                 break
    #             if st[0] + 1 == ore[0] and st[1] == ore[1] or \
    #                     st[0] - 1 == ore[0] and st[1] == ore[1] or \
    #                     st[0] == ore[0] and st[1] + 1 == ore[1] or \
    #                     st[0] == ore[0] and st[1] - 1 == ore[1]:
    #                 o = self.board[ore[0]][ore[1]]
    #                 o = str(int(o) + 1)
    #                 if o == '10':
    #                     if double_stones_in_ores:
    #                         sym = '$'
    #                     else:
    #                         sym = self.next_in_queue()
    #                     line = list(self.board[ore[0]])
    #                     line[ore[1]] = sym
    #                     self.board[ore[0]] = ''.join(line)
    #                     del self.ore_coords[self.ore_coords.index(ore)]
    #                 else:
    #                     line = list(self.board[ore[0]])
    #                     line[ore[1]] = o
    #                     self.board[ore[0]] = ''.join(line)
    #                 next_ore = True

    # def tools_into_battle(self, cell):
    #     for ins in instrument_quadra:
    #         if ins.active and not ins.used:
    #             an = AnimatedSprite(instrument_animations[ins.name], 6, 1,
    #                                 cell[0] * self.cell_size, cell[1] * self.cell_size)
    #             if ins.name == 'pikhouweel' and not ins.used:
    #                 to_statistic(self.board[cell[1]][cell[0]], 1)
    #                 line = list(self.board[cell[1]])
    #                 line[cell[0]] = self.next_in_queue()
    #                 self.board[cell[1]] = ''.join(line)
    #                 instrument_quadra[instruments.index(ins.name)].used = True
    #                 boom = AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
    #                                       3, 1, cell[0] * self.cell_size, cell[1] * self.cell_size)
    #             elif ins.name == 'boren' and not ins.used:
    #                 for elem in self.board[cell[1]]:
    #                     to_statistic(elem, 1)
    #                 line = ''
    #                 for i in range(8):
    #                     line += self.next_in_queue()
    #                     boom = AnimatedSprite(load_image('mineral_die_animate.png', directory='assets/animations'),
    #                                           3, 1, i * self.cell_size, cell[1] * self.cell_size)
    #                 self.board[cell[1]] = line
    #                 instrument_quadra[instruments.index(ins.name)].used = True
    #             # elif ins.name
    #             [st.kill() for st in stones_group]
    #             self.horizontal_reduce()
    #             self.vertical_reduce()
    #         ins.active = False
    #         # self.c1, self.c2 = None, None
    #     instrument_pad.active_instrument = None

    def on_click(self, cell, board, stat):
        self.statistic_minerals = stat
        self.board = board
        self.global_del_list = []
        if self.c1 == (None, None) and self.c2 == (None, None):
            self.c1 = cell
        elif self.c1 != (None, None) and self.c2 == (None, None):
            self.c2 = cell
        else:
            self.c1 = cell
            self.c2 = (None, None)
        if self.c1 != (None, None) and self.c2 != (None, None) and self.c1 != self.c2:
            c1, c2 = self.c1, self.c2
            old_board = self.board[:]
            # for i, st in enumerate(stones_group):
            #     if i == c1[0] * 8 + c1[1]:
            #         st.kill()
            #     if i == c2[0] * 8 + c2[1]:
            #         st.kill()
            # if self.board[c1[0]][c1[1]] not in ['7', '8', '9'] and self.board[c2[0]][c2[1]] not in ['7', '8', '9']:
            if c1 not in self.ore_coords and c2 not in self.ore_coords:
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
                    old_line = self.board[self.c1[1]][:]
                    self.board[self.c1[1]] = line1
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
                # move_pad.minus()
                # board.horizontal_reduce()
                # board.vertical_reduce()
        # self.tools_into_battle(cell)
        return self.board

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
                        self.to_statistic(cur_st, len(del_list))
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
                    # self.check_near_ores(del_list)
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
                        self.to_statistic(cur_st, len(del_list))
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
                    # self.check_near_ores(del_list)
                    del_list = []
            j += 1
            i = 0


# class Fon(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__(all_sprites, fon_sprites)
#         self.image = load_image(name='bg.png', directory='assets/fon')
#         self.rect = self.image.get_rect().move(0, 0)


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y):
#         super().__init__(animated_group)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = pygame.transform.scale(self.frames[self.cur_frame], (90, 90))
#         self.rect = self.rect.move(x, y)
#         self.i = 0
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         if self.i < len(self.frames):
#             self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#             self.image = pygame.transform.scale(self.frames[self.cur_frame], (90, 90))
#             self.i += 1
#         else:
#             self.kill()
#             board.on_click(board.c1)


# class Checkmark(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__(checkmark_group, all_sprites)
#         self.image = pygame.transform.scale(load_image('checkmark.png'), (60, 45))
#         self.rect = self.image.get_rect().move(
#             5 + tile_width * pos_x, 30 + tile_height * pos_y)


# class Stone(pygame.sprite.Sprite):
#     def __init__(self, tile_type, pos_x, pos_y):
#         super().__init__(stones_group, all_sprites)
#         self.image = stone_images[tile_type]
#         self.rect = self.image.get_rect().move(
#             10 + tile_width * pos_x, 10 + tile_height * pos_y)


# class Move:
#     def __init__(self, n):
#         self.n = n
#
#     def minus(self):
#         self.n -= 1
#
#     def show(self):
#         pygame.draw.ellipse(screen, 'YellowGreen', (630, 10, 90, 90), 0)
#         pygame.draw.ellipse(screen, 'DarkGreen', (630, 10, 90, 90), 5)
#         text = [str(self.n).rjust(2, ' ')]
#         font = pygame.font.Font(None, 70)
#         text_coord = 17
#         for line in text:
#             string_rendered = font.render(line, 1, pygame.Color('DarkGreen'))
#             text_rect = string_rendered.get_rect()
#             text_coord += 10
#             text_rect.top = text_coord
#             text_rect.x = 645
#             text_coord += text_rect.height
#             screen.blit(string_rendered, text_rect)


# class WinOrDefeat:
#     def __init__(self, moves):
#         self.moves = moves
#
#     def check_moves(self):
#         if self.moves == 0 and not victory:
#             self.defeat()
#
#     def defeat(self):
#         text = 'Неудача!'
#         font = pygame.font.Font(None, 200)
#         text_coord = 17
#         string_rendered = font.render(text, 1, pygame.Color('White'))
#         text_rect = string_rendered.get_rect()
#         text_rect.top = text_coord
#         text_rect.x = 10
#         screen.blit(string_rendered, text_rect)
#
#     def victory(self):
#         global victory
#         text = 'Изумительно!' if self.moves < 3 else 'Прелестно!'
#         font = pygame.font.Font(None, 200)
#         text_coord = 17
#         string_rendered = font.render(text, 1, pygame.Color('White'))
#         text_rect = string_rendered.get_rect()
#         text_rect.top = text_coord
#         text_rect.x = 10
#         screen.blit(string_rendered, text_rect)
#         victory = True


# board = Board(8, 8, 10, 10, 75)
# instrument_pad = InstrumentPad()
# move_pad = Move(20)
# running = True
# while running:
#     game_result = WinOrDefeat(move_pad.n)
#     level_x, level_y = generate_level(board.board)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             board.get_click(event.pos)
#             instrument_pad.get_click(event.pos)
#     # board.horizontal_reduce()
#     # board.vertical_reduce()
#     draw_cell_field()
#     draw_instruments()
#     move_pad.show()
#     write_statistic(('5', 10), ('6', 15), ('4', 20))
#     game_result.check_moves()
#     animated_group.draw(screen)
#     animated_group.update()
#     checkmark_group.draw(screen)
#     pygame.display.flip()
#     screen.fill('black')
#     clock.tick(FPS)
# terminate()
