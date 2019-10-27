# -*- coding: utf-8 -*-
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN
from pygame.locals import K_1, K_2, K_3, K_4, K_5, K_6, K_z, K_x, K_c
import sys
import os
import random
import glob
import time

from drops_manager import DropsManager
from draw_manager import DrawManager
from skills_manager import SkillsManager

SCREEN_SIZE = (400, 600)
N_DROP_X = 6
N_DROP_Y = 5
FPS = 60
COMBO_INTERVAL = int(FPS * 0.4)
DROP_LENGTH = SCREEN_SIZE[0] // N_DROP_X
OFFSET_Y = SCREEN_SIZE[1] - DROP_LENGTH * N_DROP_Y

pygame.mixer.init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("パズドラゲーム")

pygame.mixer.music.load("bgm_02.ogg")
pygame.mixer.music.play(-1)
SOUNDS = {filename: pygame.mixer.Sound(filename)
          for filename in glob.glob("se_*.ogg")}
IMAGES = {int(os.path.basename(filename)[0]): pygame.transform.smoothscale(
    pygame.image.load(filename).convert_alpha(), (DROP_LENGTH, DROP_LENGTH))
    for filename in glob.glob("images/*.png")}
FONT = pygame.font.Font("ipaexg.ttf", 40)


class Pazudora:
    def __init__(self):
        sys.setrecursionlimit(5000)

        self.drops = DropsManager.new_drops(N_DROP_X, N_DROP_Y)

        self.is_moving = False
        self.moving_drop_index = (0, 0)
        self.moving_drop_pos = (0, 0)
        self.moving_drop_type = 0

        self.moving_start_time = 0
        self.moving_time = 0

        self.draw_manager = DrawManager(self.drops, screen, IMAGES)
        self.drops_manager = DropsManager(self.drops, SOUNDS, COMBO_INTERVAL)
        self.skills_manager = SkillsManager(self.drops)

    def main(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                self._event_handler(event)

            if self.drops_manager.is_erase_timing():
                if self.drops_manager.can_erase():
                    self.drops_manager.erase()
                else:
                    if self.drops_manager.can_fall():
                        self.drops_manager.fall()
                        self.drops_manager.reset_will_erased_drops()
                    else:
                        self.drops_manager.finish_erase()

            if self.is_moving:
                self.moving_time = time.time() - self.moving_start_time

            self._draw()

    def _draw(self):
        screen.fill((0, 0, 0))

        self.draw_manager.draw_drops(self.drops)
        if self.is_moving:
            self.draw_manager.draw_drop(
                self.moving_drop_type, center=self.moving_drop_pos)

        dictionary = {
            "コンボ": self.drops_manager.erase_combo,
            "移動時間": "%.2f" % self.moving_time,
            "": self.drops_manager.erased_colors
        }
        self.draw_manager.draw_text(screen, FONT, dictionary)

        pygame.display.update()

    def _event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self._mouse_down_action(event)
        if event.type == MOUSEMOTION:
            self._mouse_move_action(event)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self._mouse_up_action(event)
        if event.type == KEYDOWN:
            if self.is_moving or self.drops_manager.is_erasing:
                return
            if event.key == K_z:
                self.skills_manager.drops_to_max_combo()
            if event.key == K_x:
                self.skills_manager.drops_to_can_all_clear()
            if event.key == K_c:
                self.skills_manager.drops_to_exist_5colors()
            hanabi_dict = {K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6}
            if event.key in hanabi_dict:
                self.skills_manager.drops_to_hanabi(hanabi_dict[event.key])

    def _mouse_down_action(self, event):
        if not self.is_moving:
            x, y = self.draw_manager.to_index(event.pos)
            if self.draw_manager.is_in_drops_area(x, y):
                self.is_moving = True
                self.moving_drop_pos = event.pos
                self.moving_drop_index = (x, y)
                self.moving_drop_type = self.drops[y][x]
                self.drops[y][x] = 0
                # option
                self.erased_colors = []
                self.moving_start_time = time.time()

    def _mouse_move_action(self, event):
        if self.is_moving:
            self.moving_drop_pos = event.pos[0], max(event.pos[1], OFFSET_Y)
            new_index = self.draw_manager.to_index(self.moving_drop_pos)
            if self.draw_manager.is_in_drops_area(*new_index):
                if new_index != self.moving_drop_index:
                    SOUNDS["se_004.ogg"].play()
                    x, y = self.moving_drop_index
                    self.drops[y][x] = self.drops[new_index[1]][new_index[0]]
                    self.drops[new_index[1]][new_index[0]] = 0
                    self.moving_drop_index = new_index

    def _mouse_up_action(self, event):
        if self.is_moving:
            self.is_moving = False
            self.drops[self.moving_drop_index[1]
                       ][self.moving_drop_index[0]] = self.moving_drop_type
            self.drops_manager.start_erase()


if __name__ == "__main__":
    pazudora = Pazudora()
    pazudora.main()
