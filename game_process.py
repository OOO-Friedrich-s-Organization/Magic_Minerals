import pygame
import sys
import os


WIDTH, HEIGHT = 1080, 720

first_time = True
first_time_in_ore = True
victory = False
double_stones_in_ores = True


class Board:
    def __init__(self, movies, level_now):
        self.c1 = (None, None)
        self.c2 = (None, None)
        self.width = 8
        self.height = 8
        self.score = 0
        with open(f'assets/levels/fall_{level_now}.txt', 'rt') as f:
            file = f.readlines()
        self.queue = list(file[0])
        self.global_del_list = []
        self.statistic_minerals = []
        self.double_stones_in_ores = True
        self.movies = movies

    def to_statistic(self, stone_num, quantity, prize=False):  # отправление собранных камней
        # в статистику и подсчёт очков
        for ind, st in enumerate(self.statistic_minerals):
            if st[0] == stone_num:
                self.statistic_minerals[ind][1] = str(int(self.statistic_minerals[ind][1]) + quantity)
        if prize:
            extra = 7
        else:
            extra = 1
        if stone_num in list(map(lambda x: x[0], self.statistic_minerals)):
            self.update_score(15 * quantity * extra)
        else:
            self.update_score(5 * quantity * extra)

    def update_score(self, plus):
        self.score += plus
    
    def end_checker(self):  # проверка на возможность окончания игры
        stater = 0
        for stat in self.statistic_minerals:
            if int(stat[1]) >= int(stat[2]):
                stater += 1
        if stater == 3:
            return True, self.score
        elif self.movies == 0:
            return False, self.score
        else:
            return False, None

    def next_in_queue(self, stone):  # получение следующего камня в очереди
        if stone != '0':
            next = self.queue[0]
            del self.queue[0]
        else:
            next = '0'
        return next

    def check_near_ores(self, del_list, it_is_stone=False):  # проверка на наличие руд по близости
        allowed = False
        a = 1
        b = 0
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

    def activate_double_stone(self, lighted_cells):  # активация удвоения у камня удвоения
        for line in self.board:
            if '$' in line:
                lst_index_dblst = []
                lst_index = self.board.index(line)
                i = 0
                for elem in line:
                    if elem == "$":
                        lst_index_dblst.append(i)
                    i += 1
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

    def tools_into_battle(self, cell, instrument_quadra, board, stat, lighted_cells, ore_coords):  # выполение
        # действий инструментов
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
                        self.check_near_ores([(cell[1], cell[0])], it_is_stone=True)

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
                            self.check_near_ores([(i, cell[0])], it_is_stone=True)
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
                                self.check_near_ores([(cell[1] - 1, ln_index)], it_is_stone=True)
                                ln[cell[1] - 1] = self.board[ln_index][cell[1] - 1]
                        self.to_statistic(ln[cell[1]], 1)
                        if tuple([ln_index, cell[1]]) in lighted_cells:
                            self.to_statistic(ln[cell[1]], 1)
                        if ln[cell[1]] not in ['7', '8', '9', '$']:
                            ln[cell[1]] = self.next_in_queue(ln[cell[1]])
                        else:
                            self.check_near_ores([(cell[1], ln_index)], it_is_stone=True)
                            ln[cell[1]] = self.board[ln_index][cell[1]]
                        if cell[1] + 1 < self.width:
                            self.to_statistic(ln[cell[1] + 1], 1)
                            if tuple([ln_index, cell[1] + 1]) in lighted_cells:
                                self.to_statistic(ln[cell[1] + 1], 1)
                            if ln[cell[1] + 1] not in ['7', '8', '9', '$']:
                                ln[cell[1] + 1] = self.next_in_queue(ln[cell[1] + 1])
                            else:
                                self.check_near_ores([(cell[1] + 1, ln_index)], it_is_stone=True)
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
        win, score_win = self.end_checker()
        lighted_cells = self.activate_double_stone(lighted_cells)
        return self.board, animate, lighted_cells, win, score_win

    def on_click(self, cell, board, stat, lighted_cells, ore_coords):  # передвижение камней по полю
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
                    self.board[c1[1]][c1[0]] not in ['7', '8', '9', '$'] and\
                    self.board[c2[1]][c2[0]] not in ['7', '8', '9', '$']:
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
                self.movies -= 1
        win, score_win = self.end_checker()
        lighted_cells = self.activate_double_stone(lighted_cells)
        return self.board, self.statistic_minerals, lighted_cells, win, score_win

    def horizontal_reduce(self, board, lighted_cells):  # горизонтальное уничжение камней
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

    def vertical_reduce(self, board, lighted_cells):  # вертикальное уничтожение камней
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
