import os
import glob
import pygame


class SoundManager:
    @classmethod
    def init(cls):
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(64)

        cls.SOUNDS = {os.path.basename(filename): pygame.mixer.Sound(filename)
                      for filename in glob.glob("sounds/se_*.ogg")}

    def play_bgm(self):
        pygame.mixer.music.load("sounds/bgm_02.ogg")
        pygame.mixer.music.play(-1)

    def play_se_combo(self, combo_num):
        self.SOUNDS["se_006p%03d.ogg" % combo_num].play()

    def play_se_moving(self):
        self.SOUNDS["se_004.ogg"].play()
