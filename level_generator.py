import pygame
import os
import sys
from test import Board


pygame.init()


WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 15

btn_sprites = pygame.sprite.Group()
bg_panels_sprites = pygame.sprite.Group()
instruments_group = pygame.sprite.Group()
top_layer_sprites = pygame.sprite.Group()
field = pygame.sprite.Group()
field_minerals_and_stones = pygame.sprite.Group()
stat_group = pygame.sprite.Group()
anim_die_sprites = pygame.sprite.Group()
anim_instr_sprites = pygame.sprite.Group()

instruments_create = []
paneles_create = []

board = Board()


class GamePlace:
    def __init__(self, parent):
        self.parent = parent
        self.first_time = True
        self.was_move = True
        self.move_now = False
        self.statistik_update = True
        self.move_wasnt_done = False
        self.animation_active = False
        self.instrument_active = False
        self.move_x = self.move_y = 0

        self.lighted_cells = []
        self.ore_coords = []

        self.fon = pygame.transform.scale(self.parent.load_image('fon/bg.png'), (WIDTH, HEIGHT))

        self.bg_panels = {'board_panel': self.parent.load_image('windows/game_pole.png', -1),
                          'instrumets_panel': self.parent.load_image('windows/instruments_panel.png', -1),
                          }
        self.bg_panels_pos = {'board_panel': [90, 0, ],
                              'instrumets_panel': [760, 30]
                              }

        self.btns_positions = {'laud_on': [1000, 640, 60, 60],
                               'laud_off': [1000, 640, 60, 60],
                               'back_btn': [20, 640, 60, 60]
                               }

        self.btns = {'100x100': self.parent.load_image('buttons/100x100_btn.png', -1),
                     'circle': self.parent.load_image('buttons/circle.png', -1),
                     'laud_on': self.parent.load_image('buttons/60x60_btn_laud_on.png', -1),
                     'laud_off': self.parent.load_image('buttons/60x60_btn_laud_off.png', -1),
                     'back_btn': self.parent.load_image('buttons/back_btn.png', -1),
                     'selected_instrument': self.parent.load_image('buttons/selected_instrument.png', -1),
                     'deactive_instrument': self.parent.load_image('buttons/deactive_instrument.png', -1),
                     'instrumet_btn': self.parent.load_image('buttons/instrumet_btn.png', -1),
                     }

        self.instruments = {'pikhouweel': self.parent.load_image('instruments/pikhouweel.png', -1),
                            'boren': self.parent.load_image('instruments/boren.png', -1),
                            'dinamite': self.parent.load_image('instruments/dinamite.png', -1),
                            'lantern': self.parent.load_image('instruments/lantern.png', -1),
                            }

        for instr in self.instruments:
            self.instruments[instr] = pygame.transform.scale(self.instruments[instr], (90, 90))

        self.animation_lens = {'die': [15, 5, 75],
                               'boren': [33, 6, 100],
                               'dinamite': [24, 4, 270],
                               'lantern': [32, 4, 225],
                               'pikhouweel': [20, 2, 100],
                               }

        self.animations = {'die': self.parent.load_image('animations/mineral_die_animate.png'),
                           'boren': self.parent.load_image('animations/boren_animate.png'),
                           'dinamite': self.parent.load_image('animations/dinamite_animate.png'),
                           'lantern': self.parent.load_image('animations/lantern_animate.png'),
                           'pikhouweel': self.parent.load_image('animations/pikhouweel_animate.png'),
                           }

        self.stone_images = {'1': self.parent.load_image('minerals/amber.png', -1),
                             '2': self.parent.load_image('minerals/amethyst.png', -1),
                             '3': self.parent.load_image('minerals/diamond.png', -1),
                             '4': self.parent.load_image('minerals/emerald.png', -1),
                             '5': self.parent.load_image('minerals/ruby.png', -1),
                             '6': self.parent.load_image('minerals/sapphire.png', -1),
                             '7': self.parent.load_image('stones/ore_1.png'),
                             '8': self.parent.load_image('stones/ore_2.png'),
                             '9': self.parent.load_image('stones/ore_3.png'),
                             '$': self.parent.load_image('stones/double_stone.png')
                             }
        for num in self.stone_images:
            self.stone_images[num] = pygame.transform.scale(self.stone_images[num], (69, 69))
        self.cells = {'simple': self.parent.load_image('cells/cell.png'),
                      'x2': self.parent.load_image('cells/cell_blue.png'),
                      'ore': self.parent.load_image('cells/cell_green.png'),
                      '$': self.parent.load_image('cells/cell_pink.png'),
                      'sel1': self.parent.load_image('cells/cell_sel.png'),
                      'sel2': self.parent.load_image('cells/cell_sel2.png'),
                      'x2_sel1': self.parent.load_image('cells/cell_blue_sel.png'),
                      'x2_sel2': self.parent.load_image('cells/cell_blue_sel2.png'),
                      }

        self.statistik = [['5', '0', '10'], ['6', '0', '15'], ['4', '0', '20']]

    def render(self, level):
        if self.first_time:
            screen.blit(self.fon, (0, 0))
            self.board_loader(level)

        for btn in self.parent.btns_now[2:]:
            Button(self.btns[btn], self.btns_positions[btn], btn_sprites)

        old_board = self.board[:]
        self.board = board.horizontal_reduce(self.board, self.lighted_cells)
        self.board = board.vertical_reduce(self.board, self.lighted_cells)
        if self.board != old_board:
            self.was_move = True

        self.render_bg_panels()
        self.render_instruments()
        self.draw_cell_field()
        self.render_statistik()
        self.render_die_animate()

        bg_panels_sprites.draw(screen)
        btn_sprites.draw(screen)
        btn_sprites.empty()
        instruments_group.draw(screen)
        field.draw(screen)
        field_minerals_and_stones.draw(screen)
        stat_group.draw(screen)
        anim_die_sprites.draw(screen)
        anim_die_sprites.update()
        anim_instr_sprites.draw(screen)
        anim_instr_sprites.update()

        top_layer_sprites.draw(screen)
        top_layer_sprites.empty()

        # font = pygame.font.Font('assets/font/Boncegro FF 4F.otf', 40)
        # string_rendered = font.render(f'Ходов: 13', 3, (180, 100, 0))
        # text_rect = string_rendered.get_rect()
        # text_rect.top = 540
        # text_rect.x = 800
        # screen.blit(string_rendered, text_rect)

        self.first_time = False

    def render_bg_panels(self):
        if self.first_time:
            bg_panels_sprites.empty()
            paneles_create.clear()
            for bg in self.bg_panels:
                paneles_create.append(Button(self.bg_panels[bg], self.bg_panels_pos[bg], bg_panels_sprites))

    def render_instruments(self):
        if self.first_time:
            instruments_create.clear()
            instruments_group.empty()
        for ind, instrument in enumerate(self.instruments):
            if self.first_time:
                instruments_create.append(Instrument(instrument, ind,
                                                     self.instruments[instrument], self.animations[instrument]))
            if instruments_create[ind].active:
                Button(self.btns['selected_instrument'], [805, 55 + 110 * ind], btn_sprites)
            else:
                Button(self.btns['instrumet_btn'], [820, 70 + 110 * ind], btn_sprites)
            if instruments_create[ind].used:
                Button(self.btns['deactive_instrument'], [820, 70 + 110 * ind], top_layer_sprites)

    def render_instruments_animate(self, cell, animate):
        if animate == 'pikhouweel':
            instr = AnimatedSprite(self.animations[animate],
                                   6, 1, 50 + 75 * cell[0], 75 * cell[1], self.animation_lens[animate])
        elif animate == 'boren':
            instr = AnimatedSprite(self.animations[animate],
                                   6, 1, 50 + 75 * cell[0], 75 * cell[1] - 30, self.animation_lens[animate])
        elif animate == 'dinamite':
            instr = AnimatedSprite(self.animations[animate],
                                   6, 1, 25 + 75 * cell[0], 75 * cell[1] - 65, self.animation_lens[animate])
        elif animate == 'lantern':
            instr = AnimatedSprite(self.animations[animate],
                                   6, 1, 45 + 75 * cell[0], 75 * cell[1] - 45, self.animation_lens[animate])

    def draw_cell_field(self):
        if self.first_time:
            board.c1, board.c2 = (None, None), (None, None)
        if self.was_move or self.move_now:
            field.empty()
            field_minerals_and_stones.empty()
            if self.move_now:
                self.stone_move()
            for ind_y, row in enumerate(self.board):
                for ind_x, elem in enumerate(row):
                    if elem != '0':
                        cell = 'simple'
                        if (ind_x, ind_y) == board.c1 and not self.move_wasnt_done:
                            cell = 'sel1'
                        elif (ind_x, ind_y) == board.c2 and not self.move_wasnt_done:
                            cell = 'sel2'
                        if elem == '$':
                            cell = '$'
                        elif int(elem) >= 7:
                            cell = 'ore'
                            if (ind_x, ind_y) not in self.ore_coords:
                                self.ore_coords += [(ind_x, ind_y)]
                        elif (ind_y, ind_x) in self.lighted_cells:
                            cell = 'x2'
                            if (ind_x, ind_y) == board.c1 and not self.move_wasnt_done:
                                cell = 'x2_sel1'
                            elif (ind_x, ind_y) == board.c2 and not self.move_wasnt_done:
                                cell = 'x2_sel2'
                        Button(self.cells[cell], [120 + 75 * ind_x, 30 + 75 * ind_y], field)
                        move_x = move_y = 0
                        if (ind_x, ind_y) == board.c1:
                            move_x += self.move_x
                            move_y += self.move_y
                        elif (ind_x, ind_y) == board.c2:
                            move_x -= self.move_x
                            move_y -= self.move_y
                        Button(self.stone_images[elem],
                               [121 + 75 * ind_x + move_x,
                                31 + 75 * ind_y + move_y], field_minerals_and_stones)
            self.was_move = False

    def render_die_animate(self):
        self.del_list = board.global_del_list
        if self.del_list:
            for die in self.del_list[0]:
                boom = AnimatedSprite(self.animations['die'],
                                      3, 1, 120 + 75 * die[1], 30 + 75 * die[0], self.animation_lens['die'])
            self.del_list.clear()

    def render_statistik(self):
        if self.first_time:
            for ind, mineral in enumerate(self.statistik):
                Button(self.stone_images[mineral[0]], [12, ind * 150 + 105], stat_group)

        if self.statistik_update:
            screen.blit(self.fon, (0, 0))
            font = pygame.font.Font(None, 40)
            for ind, stat in enumerate(self.statistik):
                if int(stat[1]) < int(stat[2]):
                    string_rendered = font.render('/'.join(stat[1:]), 3, (180, 100, 0))
                else:
                    string_rendered = font.render(f'{stat[2]}/{stat[2]}', 3, (180, 100, 0))
                text_rect = string_rendered.get_rect()
                text_rect.top = ind * 150 + 180
                text_rect.x = 20 if len(stat[1]) == 1 else 13
                screen.blit(string_rendered, text_rect)
                if int(stat[1]) >= int(stat[2]):
                    checkmark = pygame.transform.scale(self.parent.load_image('buttons/checkmark.png'), (60, 45))
                    Button(checkmark, [12, ind * 150 + 135], top_layer_sprites)

    def stone_move(self):
        if abs(self.move_x) == 70 or abs(self.move_y) == 70:
            self.move_x = self.move_y = 0
            self.move_now = False
            self.was_move = True
            self.board, self.old_board = self.old_board[:], self.board[:]
        elif board.c1[0] == board.c2[0]:
            if board.c1[1] < board.c2[1]:
                self.move_y += 10
            else:
                self.move_y -= 10
        elif board.c1[1] == board.c2[1]:
            if board.c1[0] < board.c2[0]:
                self.move_x += 10
            else:
                self.move_x -= 10

    def board_loader(self, level):
        with open(f'assets/levels/level_{level}.txt', 'r', encoding='utf-8') as level_file:
            self.board = [line.rstrip('\n') for line in level_file.readlines()]

    def click_check(self, coords):
        for ind, panel in enumerate(paneles_create):
            if (panel.rect.x < coords[0] < panel.rect.x + panel.rect.w and
                    panel.rect.y < coords[1] < panel.rect.y + panel.rect.h):
                if ind == 1:
                    for instr in instruments_create:
                        if (instr.rect.x < coords[0] < instr.rect.x + instr.rect.w and
                                instr.rect.y < coords[1] < instr.rect.y + instr.rect.h):
                            if not instr.active and not self.instrument_active and not instr.used:
                                instr.active = True
                                self.instrument_active = True
                            elif instr.active and self.instrument_active:
                                instr.active = False
                                self.instrument_active = False
                else:
                    if self.get_click(coords) and not self.move_now and not self.instrument_active:
                        self.old_board = self.board[:]
                        if self.move_wasnt_done:
                            self.move_wasnt_done = False
                        self.board, self.statistik, self.lighted_cells = board.on_click(self.get_cell(coords),
                                                                                        self.board,
                                                                                        self.statistik,
                                                                                        self.lighted_cells,
                                                                                        self.ore_coords)
                        self.animation_active = True
                        if type(board.c1[0]) == int and type(board.c2[0]) == int and self.board == self.old_board:
                            self.move_wasnt_done = True
                        elif type(board.c1[0]) == int and type(board.c2[0]) == int and self.board != self.old_board:
                            self.move_now = True
                            self.board, self.old_board = self.old_board[:], self.board[:]
                        self.was_move = True
                        self.statistik_update = True
                    elif self.get_click(coords) and self.instrument_active:
                        self.old_board = self.board[:]
                        self.board, animate, self.lighted_cells = board.tools_into_battle(self.get_cell(coords),
                                                                                          instruments_create,
                                                                                          self.board,
                                                                                          self.statistik,
                                                                                          self.lighted_cells,
                                                                                          self.ore_coords)
                        self.instrument_active = False
                        if self.board != self.old_board:
                            self.was_move = True
                            self.statistik_update = True
                            if animate:
                                self.render_instruments_animate(self.get_cell(coords), animate)
                        elif animate == 'lantern':
                            self.was_move = True
                            self.render_instruments_animate(self.get_cell(coords), animate)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - 120) // 75
        cell_y = (mouse_pos[1] - 30) // 75
        if cell_x < 0 or cell_x >= WIDTH or cell_y < 0 or cell_y >= HEIGHT:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return True
        return False


class Button(pygame.sprite.Sprite):
    def __init__(self, image, coords, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(coords[0], coords[1])


class Instrument(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_y, image, animation):
        super().__init__(instruments_group)
        self.name = tile_type
        self.image = image
        self.animation = animation
        self.rect = self.image.get_rect().move(
            825, 75 + 110 * pos_y)
        self.active = False
        self.used = False


class NecessaryStone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, need):
        super().__init__(necessary_stones_group, all_sprites)
        self.tile_type = tile_type
        self.image = stone_images[tile_type]
        self.text = [0, need]
        self.rect = self.image.get_rect().move(
            10 + tile_width * pos_x, 10 + tile_height * pos_y)
        self.x, self.y = pos_x, pos_y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, frame_info):
        if columns == 3:
            self.group = anim_die_sprites
        else:
            self.group = anim_instr_sprites
        super().__init__(self.group)
        self.frames = []
        self.frame_info = frame_info
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                            (self.frame_info[2], self.frame_info[2]))
        self.rect = self.rect.move(x, y)
        self.i = 0
        self.timer = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.timer % self.frame_info[1] == 0:
            if self.timer < self.frame_info[0]:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                                    (self.frame_info[2], self.frame_info[2]))
                self.i += 1
            else:
                self.kill()
                self.group.empty()
        self.timer += 1
