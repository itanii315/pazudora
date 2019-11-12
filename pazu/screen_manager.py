import pygame
import glob
import os


class ScreenManager:
    def __init__(self, drops, view):
        self.drops = drops
        self.view = view
        
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)
        self.DROP_LENGTH = view.w // self.N_DROP_X
        self.OFFSET_Y = view.h - self.DROP_LENGTH * self.N_DROP_Y

        self.FONT = pygame.font.Font("ipaexg.ttf", view.w // 10)
        self.IMAGES = {
            int(os.path.basename(filename)[0]): pygame.transform.smoothscale(
                pygame.image.load(filename).convert_alpha(),
                (self.DROP_LENGTH, self.DROP_LENGTH),
            ) for filename in glob.glob("images/*.png")}

    def into_screen(self, pos):
        return self.view.into_screen(pos)

    def draw_drops(self):
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                self.draw_drop(self.drops[y][x], center=self.to_pos(x, y))

    def draw_drop(self, drop_num, left_up=None, center=None):
        if drop_num in self.IMAGES:
            image = self.IMAGES[drop_num]
            if center:
                x = center[0] - image.get_width() // 2
                y = center[1] - image.get_height() // 2
                left_up = (x, y)
            self.view.blit(image, left_up)

    def draw_text(self, info_dict):
        y = self.view.h // 30
        for key in info_dict:
            text = f"{key}: {info_dict[key]}"
            sprite = self.FONT.render(text, True, (255, 255, 255))
            self.view.blit(sprite, (20, y))
            y += self.view.h // 10

    def to_pos(self, x, y):
        pos_x = self.DROP_LENGTH * x + self.DROP_LENGTH // 2
        pos_y = self.DROP_LENGTH * y + self.DROP_LENGTH // 2 + self.OFFSET_Y
        return pos_x, pos_y

    def to_index(self, pos):
        x_index = pos[0] // self.DROP_LENGTH
        y_index = (pos[1] - self.OFFSET_Y) // self.DROP_LENGTH
        return x_index, y_index