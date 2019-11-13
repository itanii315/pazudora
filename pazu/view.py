import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN, K_p

class View:
    views = []
    def __init__(self, x, y, w, h, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        View.views.append(self)
        self.is_update = True
        self.create(**kwargs)

    def on_update(self, screen):
        if self.is_update:
            self.update()
        self._screen = screen
        self.draw()

    def on_event(self, event):
        if event.type == KEYDOWN and event.key == K_p:
            self.is_update = not self.is_update
        if not self.is_update:
            return

        if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP):
            pos = self.get_pos_on_view(event.pos)
            if event.type == MOUSEBUTTONDOWN:
                if not self.is_in_view(pos):
                    return
            else:
                pos = self.into_view(pos)
            
            button = None if event.type == MOUSEMOTION else event.button
            self.mouse(event.type, button, pos)
            
        elif event.type == KEYDOWN:
            self.key(event.key)

    def on_destroy(self):
        self.destroy()

    def blit(self, sprite, pos):
        pos = self.get_pos_on_screen(pos)
        self._screen.blit(sprite, pos)

    def is_in_view(self, pos):
        return 0 <= pos[0] < self.w and 0 <= pos[1] < self.h

    def get_pos_on_view(self, pos):
        return pos[0] - self.x, pos[1] - self.y

    def get_pos_on_screen(self, pos):
        return pos[0] + self.x, pos[1] + self.y

    def view_pos_to_per(self, pos):
        return pos[0] / self.w, pos[1] / self.h

    def per_to_view_pos(self, per):
        return int(per[0] * self.w), int(per[1] * self.h)

    def into_view(self, pos):
        x, y = pos
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x >= self.w:
            x = self.w - 1
        if y >= self.h:
            y = self.h - 1
        return x, y