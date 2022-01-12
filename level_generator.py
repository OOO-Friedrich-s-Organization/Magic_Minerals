import pygame
import os
import sys
from main_menu import Main


pygame.init()


WIDTH, HEIGHT = 1080, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 15

btn_sprites = pygame.sprite.Group()


btns_positions = {'laud_on': [1000, 640, 60, 60],
                  'laud_off': [1000, 640, 60, 60],
                  'back_btn': [20, 640, 60, 60]
                  }

btns = {'100x100': load_image('buttons/100x100_btn.png'),
        'circle': load_image('buttons/circle.png'),
        'laud_on': load_image('buttons/60x60_btn_laud_on.png'),
        'laud_off': load_image('buttons/60x60_btn_laud_off.png'),
        'back_btn': load_image('buttons/back_btn.png'),
        }

btns_now = ['laud_off', 'back_btn']

font_positions = {'': [0, 0],
                  }

animation_lens = {'die': [15, 3, 1],
                  'boren': [33, 3, 1],
                  'dinamite': [12, 2, 3],
                  'lantern': [15, 3, 3],
                  'pikhouweel': [25, 1, 1],
                  }

animations = {'die': load_image('animations/mineral_die_animate.png'),
              'boren': load_image('animations/boren_animate.png'),
              'dinamite': load_image('animations/dinamite_animate.png'),
              'lantern': load_image('animations/lantern_animate.png'),
              'pikhouweel': load_image('animations/pikhouweel_animate.png'),
              }


# def laud_control():
#     if btns_now[1] == 'laud_off':
#         btns_now[1] = 'laud_on'
#     else:
#         btns_now[1] = 'laud_off'
#
#
# def click_check(coords):
#     for ind, button in enumerate(btns_positions):
#         btn = btns_positions[button]
#         if (btn[0] < coords[0] < btn[0] + btn[2] and
#                 btn[1] < coords[1] < btn[1] + btn[3]):
#             if ind == 0 or ind == 1:
#                 laud_control()
#                 break
#             elif ind == 2:
#                 break


class GamePlace:
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon/bg.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        for btn in btns_now:
            Button(btns[btn], btns_positions[btn], btn_sprites)
        btn_sprites.draw(screen)
        btn_sprites.update()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, coords, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(coords[0], coords[1])

 
# if __name__ == '__main__':
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 click_check(event.pos)
# 
#         GamePlace()
# 
#         pygame.display.flip()
#         clock.tick(fps)
# 
# terminate()
