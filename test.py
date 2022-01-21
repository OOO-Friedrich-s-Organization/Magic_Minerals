import pygame
import sys
import os


WIDTH, HEIGHT = 1080, 720

first_time = True
first_time_in_ore = True
victory = False
double_stones_in_ores = True


class Board:
    def __init__(self):
        self.c1 = (None, None)
        self.c2 = (None, None)
        self.width = 8
        self.height = 8
        with open('stones/fall.txt', 'rt') as f:
            file = f.readlines()
        self.queue = list(file[0])
        self.global_del_list = []
        self.statistic_minerals = []
        self.double_stones_in_ores = True

    def to_statistic(self, stone_num, quantity, prize=False):
        for ind, st in enumerate(self.statistic_minerals):
            if st[0] == stone_num:
                self.statistic_minerals[ind][1] = str(int(self.statistic_minerals[ind][1]) + quantity)
        # if prize:
        #     extra = 7
        # else:
        #     extra = 1
        # if stone_num in list(map(lambda x: x[0], self.statistic_minerals)):
        #     game_result.update_score(15 * quantity * extra)
        # else:
        #     game_result.update_score(5 * quantity * extra)

    def next_in_queue(self, stone):
        if stone != '0':
            next = self.queue[0]
            del self.queue[0]
        else:
            next = '0'
        return next

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
                    if o != '$':
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

    def activate_double_stone(self, lighted_cells):
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
                self.horizontal_reduce(self.board, lighted_cells)
                self.vertical_reduce(self.board, lighted_cells)
        return lighted_cells

    def tools_into_battle(self, cell, instrument_quadra, board, stat, lighted_cells, ore_coords):
        self.ore_coords = ore_coords
        self.statistic_minerals = stat
        self.board, animate = board, False
        cell = cell[1], cell[0]
        for ins in instrument_quadra:
            if ins.active and not ins.used:
                if ins.name == 'pikhouweel' and not ins.used:
                    self.to_statistic(self.board[cell[0]][cell[1]], 1)
                    if cell in lighted_cells:
                        self.to_statistic(self.board[cell[0]][cell[1]], 1)
                    line = list(self.board[cell[0]])
                    if self.board[cell[0]][cell[1]] not in ['7', '8', '9', '$']:
                        line[cell[1]] = self.next_in_queue(line[cell[1]])
                        self.board[cell[0]] = ''.join(line)
                    else:
                        self.check_near_ores([(cell[0], cell[1])], it_is_stone=True)

                    instrument_quadra[0].used = True
                    animate = ins.name
                    self.global_del_list += [[cell]]
                elif ins.name == 'boren' and not ins.used:
                    i = 0
                    for elem in self.board[cell[0]]:
                        self.to_statistic(elem, 1)
                        if tuple([cell[0], i]) in lighted_cells:
                            self.to_statistic(elem, 1)
                        i += 1
                    line = list(self.board[cell[0]])
                    for i in range(self.width):
                        if line[i] not in ['7', '8', '9', '$']:
                            line[i] = self.next_in_queue(line[i])
                        else:
                            self.check_near_ores([tuple([(cell[0]), i])], it_is_stone=True)
                            line[i] = self.board[cell[0]][i]
                        self.board[cell[0]] = ''.join(line)
                    instrument_quadra[1].used = True
                    animate = ins.name
                    for ind, elem in enumerate(line):
                        if elem != '$':
                            line[ind] = [cell[0], ind]
                    self.global_del_list += [line]
                elif ins.name == 'dinamite':
                    lines = []
                    boom_pole = []
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
                        ln = list(self.board[ln_index])
                        if cell[1] - 1 > -1:
                            self.to_statistic(ln[cell[1] - 1], 1)
                            if tuple([ln_index, cell[1] - 1]) in lighted_cells:
                                self.to_statistic(ln[cell[1] - 1], 1)
                            if ln[cell[1] - 1] not in ['7', '8', '9', '$']:
                                ln[cell[1] - 1] = self.next_in_queue(ln[cell[1] - 1])
                            else:
                                self.check_near_ores([(ln_index, cell[1] - 1)], it_is_stone=True)
                                ln[cell[1] - 1] = self.board[ln_index][cell[1] - 1]
                        self.to_statistic(ln[cell[1]], 1)
                        if tuple([ln_index, cell[1]]) in lighted_cells:
                            self.to_statistic(ln[cell[1]], 1)
                        if ln[cell[1]] not in ['7', '8', '9', '$']:
                            ln[cell[1]] = self.next_in_queue(ln[cell[1]])
                        else:
                            self.check_near_ores([(ln_index, cell[1])], it_is_stone=True)
                            ln[cell[1]] = self.board[ln_index][cell[1]]
                        if cell[1] + 1 < self.width:
                            self.to_statistic(ln[cell[1] + 1], 1)
                            if tuple([ln_index, cell[1] + 1]) in lighted_cells:
                                self.to_statistic(ln[cell[1] + 1], 1)
                            if ln[cell[1] + 1] not in ['7', '8', '9', '$']:
                                ln[cell[1] + 1] = self.next_in_queue(ln[cell[1] + 1])
                            else:
                                self.check_near_ores([(ln_index, cell[1] + 1)], it_is_stone=True)
                                ln[cell[1] + 1] = self.board[ln_index][cell[1] + 1]
                        self.board[ln_index] = ''.join(ln)
                        faze += 1
                        boom_pole.append(ln)
                    instrument_quadra[2].used = True
                    animate = ins.name
                    self.global_del_list = [[]]
                    for ind_y, line in enumerate(boom_pole):
                        for ind_x, elem in enumerate(line):
                            if elem not in ['7', '8', '9', '$', '_'] and elem != lines[ind_y][ind_x]:
                                self.global_del_list[0].append([cell[0] + ind_y - 1, ind_x])
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
                        ln = list(self.board[self.board.index(line)])
                        if cell[1] - 1 > -1 and self.board[cell[0] + faze][cell[1] - 1] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1] - 1))
                        if self.board[cell[0] + faze][cell[1]] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1]))
                        if cell[1] + 1 < 8 and self.board[cell[0] + faze][cell[1] + 1] != '0':
                            lighted_cells.append((cell[0] + faze, cell[1] + 1))
                        faze += 1
                    instrument_quadra[3].used = True
                    animate = ins.name
                self.horizontal_reduce(self.board, lighted_cells)
                self.vertical_reduce(self.board, lighted_cells)
            ins.active = False
            self.vertical_reduce(self.board, lighted_cells)
            self.horizontal_reduce(self.board, lighted_cells)
        lighted_cells = self.activate_double_stone(lighted_cells)
        return self.board, animate, lighted_cells

    def on_click(self, cell, board, stat, lighted_cells, ore_coords):
        self.ore_coords = ore_coords
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
            if c1 not in self.ore_coords and c2 not in self.ore_coords and\
                    self.board[c1[0]][c1[1]] not in ['7', '8', '9', '$'] and\
                    self.board[c2[0]][c2[1]] not in ['7', '8', '9', '$']:
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
                    self.horizontal_reduce(self.board, lighted_cells)
                    self.vertical_reduce(self.board, lighted_cells)
                elif c1[0] == c2[0] and abs(c1[1] - c2[1]) == 1:
                    line1, line2 = list(self.board[c1[1]]), list(self.board[c2[1]])
                    stone1, stone2 = line1[c1[0]], line2[c2[0]]
                    del line1[c1[0]]
                    del line2[c2[0]]
                    line1.insert(c2[0], stone2)
                    line2.insert(c1[0], stone1)
                    line1, line2 = ''.join(line1), ''.join(line2)
                    self.board[c1[1]], self.board[c2[1]] = line1, line2
                    self.horizontal_reduce(self.board, lighted_cells)
                    self.vertical_reduce(self.board, lighted_cells)
        #         move_pad.minus()
        lighted_cells = self.activate_double_stone(lighted_cells)
        return self.board, self.statistic_minerals, lighted_cells

    def horizontal_reduce(self, board, lighted_cells):
        self.board = board
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
                            self.to_statistic(cur_st, score, prize=prize)
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
        return self.board

    def vertical_reduce(self, board, lighted_cells):
        self.board = board
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
                            self.to_statistic(cur_st, score, prize=prize)
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
        return self.board

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
