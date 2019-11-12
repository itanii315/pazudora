import pygame
from pygame.locals import QUIT
import sys
from view import View

class Screen:
    FPS = 60
    SCREEN_SIZE = (400, 600)

    def __init__(self):
        pygame.init()
        sys.setrecursionlimit(5000)
        pygame.display.set_caption("新しいウィンドウ")
        self.SCREEN = pygame.display.set_mode(self.SCREEN_SIZE)

    def main(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.FPS)
            self.SCREEN.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    for view in View.views:
                        view.on_destroy()
                    sys.exit()
                for view in View.views:
                    view.on_event(event)
            for view in View.views:
                view.on_update(self.SCREEN)
            pygame.display.update()