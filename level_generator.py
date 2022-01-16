import pygame
import os
import sys


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

instruments_create = []
paneles_create = []


class GamePlace:
    def __init__(self, parent):
        self.parent = parent
        self.first_time = True
        self.was_move = True

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

        self.font_positions = {'': [0, 0],
                               }

        self.animation_lens = {'die': [15, 3, 1],
                               'boren': [33, 3, 1],
                               'dinamite': [12, 2, 3],
                               'lantern': [15, 3, 3],
                               'pikhouweel': [25, 1, 1],
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
                      }

    def render(self, level):
        if self.first_time:
            screen.blit(self.fon, (0, 0))
            self.board_loader(level)

        for btn in self.parent.btns_now[2:]:
            Button(self.btns[btn], self.btns_positions[btn], btn_sprites)

        self.render_bg_panels()
        self.render_instruments()
        self.draw_cell_field(level)

        bg_panels_sprites.draw(screen)
        btn_sprites.draw(screen)
        btn_sprites.empty()
        instruments_group.draw(screen)
        top_layer_sprites.draw(screen)
        field.draw(screen)
        field_minerals_and_stones.draw(screen)

        self.first_time = False

    def render_bg_panels(self):
        if self.first_time:
            for bg in self.bg_panels:
                paneles_create.append(Button(self.bg_panels[bg], self.bg_panels_pos[bg], bg_panels_sprites))

    def render_instruments(self):
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

    def draw_cell_field(self, level):
        if self.was_move:
            for ind_y, row in enumerate(self.board):
                for ind_x, elem in enumerate(row):
                    if elem != '_':
                        cell = 'simple'
                        if elem == '$':
                            cell = '$'
                        elif int(elem) >= 7:
                            cell = 'ore'
                        elif elem == '??????????????????????????????????????????????????????????????????':
                            cell = 'x2'
                        Button(self.cells[cell], [120 + 75 * ind_x, 30 + 75 * ind_y], field)
                        Button(self.stone_images[elem],
                               [121 + 75 * ind_x, 31 + 75 * ind_y], field_minerals_and_stones)
            self.was_move = False

    def board_loader(self, level):
        with open(f'assets/levels/level_{level}.txt', 'r', encoding='utf-8') as level_file:
            self.board = [list(line.rstrip('\n')) for line in level_file.readlines()]

    def click_check(self, coords):
        for panel in paneles_create:
            if (panel.rect.x < coords[0] < panel.rect.x + panel.rect.w and
                    panel.rect.y < coords[1] < panel.rect.y + panel.rect.h):
                for instr in instruments_create:
                    if (instr.rect.x < coords[0] < instr.rect.x + instr.rect.w and
                            instr.rect.y < coords[1] < instr.rect.y + instr.rect.h):
                        if instr.active:
                            instr.active = False
                        else:
                            instr.active = True
                        break


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.timer = 0
        self.play = True

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
