import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN

class View:
    views = []
    def __init__(self, x, y, w, h, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        View.views.append(self)
        self.create(**kwargs)

    def on_update(self, screen):
        self.update()
        self._screen = screen
        self.draw()

    def on_event(self, event):
        if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP):
            pos = self._get_pos_on_view(event.pos)
            if self._is_in_view(pos):
                button = None if event.type == MOUSEMOTION else event.button
                self.mouse(event.type, button, pos)
        elif event.type == KEYDOWN:
            self.key(event.key)

    def on_destroy(self):
        self.destroy()

    def blit(self, sprite, pos):
        pos = self._get_pos_on_screen(pos)
        self._screen.blit(sprite, pos)

    def _is_in_view(self, pos):
        return 0 <= pos[0] < self.w and 0 <= pos[1] < self.h

    def _get_pos_on_view(self, pos):
        return pos[0] - self.x, pos[1] - self.y

    def _get_pos_on_screen(self, pos):
        return pos[0] + self.x, pos[1] + self.y

    def into_screen(self, pos):
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