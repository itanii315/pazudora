# -*- coding: utf-8 -*-
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN
from pygame.locals import K_1, K_2, K_3, K_4, K_5, K_6, K_z, K_x, K_c
import sys
import random
import glob
import time

sys.setrecursionlimit(5000)

SCREEN_SIZE = (400, 600)
N_DROP_X = 6
N_DROP_Y = 5
FPS = 60
COMBO_INTERVAL = int(FPS * 0.4)
DROP_LENGTH = SCREEN_SIZE[0] // N_DROP_X
OFFSET_Y = SCREEN_SIZE[1] - DROP_LENGTH * N_DROP_Y

MODE_NORMAL = 0
MODE_ERASE = 1

pygame.mixer.init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("パズドラゲーム")

pygame.mixer.music.load("bgm_02.ogg")
pygame.mixer.music.play(-1)
SOUNDS = {filename: pygame.mixer.Sound(filename) for filename in glob.glob("se_*.ogg")}
IMAGES = {filename: pygame.transform.smoothscale(pygame.image.load(filename).convert_alpha(), (DROP_LENGTH, DROP_LENGTH)) for filename in glob.glob("*.png")}
FONT = pygame.font.Font("ipaexg.ttf", 40)

class Pazudora:
    def __init__(self):
        self.drops = [[random.randint(1, 6) for i in range(N_DROP_X)] for j in range(N_DROP_Y) ]

        self.is_moving = False
        self.moving_drop_index = (0, 0)
        self.moving_drop_pos = (0, 0)
        self.moving_drop_type = 0

        self.erase_drops = []
        self.erase_motion_count = 0
        self.erase_mode = MODE_NORMAL
        self.erase_combo = 0

        self.moving_start_time = 0
        self.moving_time = 0
        self.erased_colors = []

    def main(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)

            for event in pygame.event.get(): # 終了処理
                if event.type == QUIT:
                    sys.exit()
                self.check_event(event)

            self.erase_motion()

            self.draw()

    def draw(self):
        screen.fill((0,0,0))
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                pos = self.to_pos(x, y)
                self.draw_drop(pos, self.drops[y][x])
        if self.is_moving:
            self.draw_drop(self.moving_drop_pos, self.moving_drop_type)

        # 文字
        sprite = FONT.render(f"{self.erase_combo}コンボ", True, (255, 255, 255))
        screen.blit(sprite, (20, 20))
        if self.is_moving:
            self.moving_time = time.time() - self.moving_start_time
        sprite = FONT.render("移動時間：%.2f秒" % self.moving_time, True, (255, 255, 255))
        screen.blit(sprite, (20, 70))
        sprite = FONT.render(f"{self.erased_colors}", True, (255, 255, 255))
        screen.blit(sprite, (20, 120))

        pygame.display.update()

    def erase_motion(self):
        if self.erase_mode == MODE_NORMAL:
            return

        self.erase_motion_count -= 1
        if self.erase_motion_count > 0:
            return

        if self.erase_combo == 0:
            self.erase_drops = self.erase_drop()

        if self.erase_drops:
            # 消す
            self.erase_combo += 1
            sound_num = min(self.erase_combo, 12)
            SOUNDS["se_006p%03d.ogg" % sound_num].play()
            chain = self.erase_drops.pop(0)
            for x, y, n in chain:
                self.drops[y][x] = 0
                if n not in self.erased_colors:
                    self.erased_colors.append(n)
                    self.erased_colors.sort()
            self.erase_motion_count = COMBO_INTERVAL
        else:
            if self.is_in_zero():
                # 落下
                self.fall()
                self.fall_new_drop()
                self.erase_drops = self.erase_drop()
                if self.erase_drops:
                    self.erase_motion_count = COMBO_INTERVAL
                else:
                    self.finish_erase()
            else:
                self.finish_erase()

    def start_erase(self):
        self.erase_combo = 0
        self.erase_mode = MODE_ERASE

    def finish_erase(self):
        self.erase_motion_count = 0
        self.erase_mode = MODE_NORMAL

    def check_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_down_action(event)
        if event.type == MOUSEMOTION:
            self.mouse_move_action(event)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.mouse_up_action(event)
        if event.type == KEYDOWN:
            if self.is_moving or self.erase_mode == MODE_ERASE:
                return
            if event.key == K_z:
                self.drops_to_max_combo()
            if event.key == K_x:
                self.drops_to_can_all_clear()
            if event.key == K_c:
                self.drops_to_exist_5colors()
            if event.key == K_1:
                self.drops_to_hanabi(1)
            if event.key == K_2:
                self.drops_to_hanabi(2)
            if event.key == K_3:
                self.drops_to_hanabi(3)
            if event.key == K_4:
                self.drops_to_hanabi(4)
            if event.key == K_5:
                self.drops_to_hanabi(5)
            if event.key == K_6:
                self.drops_to_hanabi(6)

    def drops_to_exist_5colors(self):
        n_prepare_drops = 3 * 5
        choices = [(i // 3) % 6 + 1 for i in range(n_prepare_drops)]
        choices += [random.randint(1, 6) for i in range(N_DROP_X * N_DROP_Y - n_prepare_drops)]
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                index = random.randrange(len(choices))
                self.drops[y][x] = choices.pop(index)

    def drops_to_can_all_clear(self):
        choices = [(i // 3) % 6 + 1 for i in range(N_DROP_X * N_DROP_Y)]
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                index = random.randrange(len(choices))
                self.drops[y][x] = choices.pop(index)

    def drops_to_max_combo(self):
        choices = [(i // 3) % 6 + 1 for i in range(N_DROP_X * N_DROP_Y)]
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                self.drops[y][x] = choices.pop(0)

    def drops_to_hanabi(self, n):
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                self.drops[y][x] = n

    def mouse_down_action(self, event):
        if self.erase_mode == MODE_NORMAL:
            x, y = self.to_index(event.pos)
            if 0 <= x < N_DROP_X and 0 <= y < N_DROP_Y:
                self.is_moving = True
                self.moving_drop_pos = event.pos
                self.moving_drop_index = (x, y)
                self.moving_drop_type = self.drops[y][x]
                self.drops[y][x] = 0
                # option
                self.erased_colors = []
                self.moving_start_time = time.time()

    def mouse_move_action(self, event):
        if self.is_moving:
            self.moving_drop_pos = event.pos[0], max(event.pos[1], OFFSET_Y)
            new_index = self.to_index(self.moving_drop_pos)
            if 0 <= new_index[0] < N_DROP_X and 0 <= new_index[1] < N_DROP_Y:
                if new_index != self.moving_drop_index:
                    SOUNDS["se_004.ogg"].play()
                    self.drops[self.moving_drop_index[1]][self.moving_drop_index[0]] = self.drops[new_index[1]][new_index[0]]
                    self.drops[new_index[1]][new_index[0]] = 0
                    self.moving_drop_index = new_index

    def mouse_up_action(self, event):
        if self.is_moving:
            self.is_moving = False
            self.drops[self.moving_drop_index[1]][self.moving_drop_index[0]] = self.moving_drop_type
            self.start_erase()

    def draw_drop(self, pos, n):
        left_up = pos[0] - DROP_LENGTH // 2, pos[1] - DROP_LENGTH // 2
        if n == 1:
            screen.blit(IMAGES["red.png"], left_up)
        if n == 2:
            screen.blit(IMAGES["blue.png"], left_up)
        if n == 3:
            screen.blit(IMAGES["green.png"], left_up)
        if n == 4:
            screen.blit(IMAGES["purple.png"], left_up)
        if n == 5:
            screen.blit(IMAGES["yellow.png"], left_up)
        if n == 6:
            screen.blit(IMAGES["pink.png"], left_up)

    def to_index(self, pos):
        x_index = pos[0] // DROP_LENGTH
        y_index =  (pos[1] - OFFSET_Y) // DROP_LENGTH
        return x_index, y_index

    def to_pos(self, x, y):
        pos_x = DROP_LENGTH * x + DROP_LENGTH // 2
        pos_y = DROP_LENGTH * y + DROP_LENGTH // 2 + OFFSET_Y
        return pos_x, pos_y

    def is_in_zero(self):
        for row in self.drops:
            if 0 in row:
                return True
        return False
    
    def fall_new_drop(self):
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                if self.drops[y][x] == 0:
                    self.drops[y][x] = random.randint(1, 6)

    def fall(self):
        for y in range(N_DROP_Y)[::-1]:
            for x in range(N_DROP_X):
                if self.drops[y][x] == 0:
                    self.drops[y][x] = self.rob_above(x, y)

    def rob_above(self, x, y):
        for i in range(y)[::-1]:
            if self.drops[i][x]:
                result = self.drops[i][x]
                self.drops[i][x] = 0
                return result
        return self.drops[y][x]

    def erase_drop(self):
        line_drops = self.get_line_drops()
        chain_drops_list = self.get_chain_drops_list(line_drops)
        return chain_drops_list

    def get_line_drops(self):
        line_drops = [[0 for i in range(N_DROP_X)] for j in range(N_DROP_Y) ]
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X - 2):
                if self.drops[y][x] == self.drops[y][x+1] == self.drops[y][x+2]:
                    drop_type = self.drops[y][x]
                    line_drops[y][x] = drop_type
                    line_drops[y][x+1] = drop_type
                    line_drops[y][x+2] = drop_type
        
        for x in range(N_DROP_X):
            for y in range(N_DROP_Y - 2):
                if self.drops[y][x] == self.drops[y+1][x] == self.drops[y+2][x]:
                    drop_type = self.drops[y][x]
                    line_drops[y][x] = drop_type
                    line_drops[y+1][x] = drop_type
                    line_drops[y+2][x] = drop_type

        return line_drops

    def get_chain_drops_list(self, line_drops):
        self.line_drops = line_drops
        self.checked_drops = [[0 for i in range(N_DROP_X)] for j in range(N_DROP_Y)]
        chain_drops_list = []
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                if line_drops[y][x]:
                    self.chain_drops = []
                    self.find_chain(x, y, line_drops[y][x])
                    if self.chain_drops:
                        chain_drops_list.append(self.chain_drops)

        return chain_drops_list
        
    def find_chain(self, x, y, n):
        if not (0 <= x < N_DROP_X and 0 <= y < N_DROP_Y):
            return
        if self.checked_drops[y][x]:
            return

        if self.line_drops[y][x] == n:
            self.chain_drops.append((x, y, n))
            self.checked_drops[y][x] = True
        else:
            return

        self.find_chain(x - 1, y, n)
        self.find_chain(x + 1, y, n)
        self.find_chain(x, y - 1, n)
        self.find_chain(x, y + 1, n)


if __name__ == "__main__":
    pazudora = Pazudora()
    pazudora.main()