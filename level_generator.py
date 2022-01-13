import pygame
import os
import sys


pygame.init()


WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 15

btn_sprites = pygame.sprite.Group()


class GamePlace:
    def __init__(self, parent):
        self.parent = parent
        self.btns_positions = {'laud_on': [1000, 640, 60, 60],
                               'laud_off': [1000, 640, 60, 60],
                               'back_btn': [20, 640, 60, 60]
                               }

        self.btns = {'100x100': self.parent.load_image('buttons/100x100_btn.png'),
                     'circle': self.parent.load_image('buttons/circle.png'),
                     'laud_on': self.parent.load_image('buttons/60x60_btn_laud_on.png'),
                     'laud_off': self.parent.load_image('buttons/60x60_btn_laud_off.png'),
                     'back_btn': self.parent.load_image('buttons/back_btn.png'),
                     }

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

        self.stone_images = {'1': load_image('amber.png'),
                             '2': load_image('amethyst.png'),
                             '3': load_image('diamond.png'),
                             '4': load_image('emerald.png'),
                             '5': load_image('ruby.png'),
                             '6': load_image('sapphire.png'),
                             }

    def render(self):
        fon = pygame.transform.scale(self.parent.load_image('fon/bg.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        for btn in self.parent.btns_now[2:]:
            Button(self.btns[btn], self.btns_positions[btn], btn_sprites)
        btn_sprites.draw(screen)
        btn_sprites.update()

        # self.rendre_board()
        self.render_instruments()


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


class Button(pygame.sprite.Sprite):
    def __init__(self, image, coords, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(coords[0], coords[1])