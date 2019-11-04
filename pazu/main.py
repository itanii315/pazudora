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
from screen_manager import ScreenManager
from skills_manager import SkillsManager
from sound_manager import SoundManager


class Pazudora:
    FPS = 60
    COMBO_INTERVAL = int(FPS * 0.4)
    SCREEN_SIZE = (400, 600)
    N_DROP_X = 6
    N_DROP_Y = 5
    MAX_MOVING_TIME = 4.00

    def __init__(self):
        pygame.init()
        sys.setrecursionlimit(5000)

        self.drops = DropsManager.new_drops(self.N_DROP_X, self.N_DROP_Y)

        self.is_moving = False
        self.moving_drop_index = (0, 0)
        self.moving_drop_pos = (0, 0)
        self.moving_drop_num = 0

        self.moving_start_time = 0
        self.moving_time = 0

        SoundManager.init()
        self.screen_manager = ScreenManager(self.drops, self.SCREEN_SIZE)
        self.drops_manager = DropsManager(self.drops, self.COMBO_INTERVAL)
        self.skills_manager = SkillsManager(self.drops)

    def main(self):
        SoundManager().play_bgm()
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                self._event_handler(event)

            if self.drops_manager.is_action_timing():
                self.drops_manager.action()
            self._update_moving_time()
            self._draw()

    def _update_moving_time(self):
        if self.is_moving:
            self.moving_time = time.time() - self.moving_start_time
            if self.moving_time > self.MAX_MOVING_TIME:
                self._mouse_up_action(None)

    def _draw(self):
        self.screen_manager.clear_screen()
        self.screen_manager.draw_drops()
        if self.is_moving:
            self.screen_manager.draw_drop(
                self.moving_drop_num, center=self.moving_drop_pos)

        info_dict = {
            "コンボ": self.drops_manager.erase_combo,
            "移動時間": "%.2f" % self.moving_time,
            "": self.drops_manager.erased_colors
        }
        self.screen_manager.draw_text(info_dict)
        self.screen_manager.update_display()

    def _event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self._mouse_down_action(event)
        elif event.type == MOUSEMOTION:
            self._mouse_move_action(event)
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self._mouse_up_action(event)
        elif event.type == KEYDOWN:
            if self.is_moving or self.drops_manager.is_erasing:
                return
            hanabi_dict = {K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6}
            if event.key in hanabi_dict:
                self.skills_manager.drops_to_hanabi(hanabi_dict[event.key])
            elif event.key == K_z:
                self.skills_manager.drops_to_max_combo()
            elif event.key == K_x:
                self.skills_manager.drops_to_can_all_clear()
            elif event.key == K_c:
                self.skills_manager.drops_to_exist_5colors()

    def _mouse_down_action(self, event):
        if self.drops_manager.is_erasing:
            return
        indices = self.screen_manager.to_index(event.pos)
        if self.screen_manager.is_in_drops_area(indices):
            self.is_moving = True
            self.moving_drop_pos = event.pos
            self.moving_drop_index = indices
            self.moving_drop_num = self.drops_manager.get_drop(indices)
            self.drops_manager.remove_drop(indices)
            # option
            self.erased_colors = []
            self.moving_start_time = time.time()

    def _mouse_move_action(self, event):
        if self.is_moving:
            self.moving_drop_pos = self.screen_manager.into_screen(event.pos)
            new_index = self.screen_manager.to_index(self.moving_drop_pos)
            if self.screen_manager.is_in_drops_area(new_index):
                if new_index != self.moving_drop_index:
                    SoundManager().play_se_moving()
                    self.drops_manager.swap(self.moving_drop_index, new_index)
                    self.moving_drop_index = new_index

    def _mouse_up_action(self, event):
        if self.is_moving:
            self.is_moving = False
            self.drops_manager.set_drop(
                self.moving_drop_index, self.moving_drop_num)
            self.drops_manager.start_erase()


if __name__ == "__main__":
    pazudora = Pazudora()
    pazudora.main()
