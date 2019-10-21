import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
import sys
import random

SCREEN_SIZE = (480, 840)
N_DROP_X = 6
N_DROP_Y = 5
FPS = 60
DROP_LENGTH = SCREEN_SIZE[0] // N_DROP_X
OFFSET_Y = SCREEN_SIZE[1] - DROP_LENGTH * N_DROP_Y

MODE_NORMAL = 0
MODE_ERASE = 1

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("パズドラゲーム")

class Pazudora:
    def __init__(self):
        self.drops = [[random.randint(1, 6) for i in range(N_DROP_X)] for j in range(N_DROP_Y) ]

    def main(self):
        is_moving = False
        moving_drop_index = (0, 0)
        moving_drop_pos = (0, 0)
        moving_drop_type = 0
        clock = pygame.time.Clock()

        erase_drops = []
        erase_motion_count = 0
        erase_mode = MODE_NORMAL
        while True:
            clock.tick(FPS)

            for event in pygame.event.get(): # 終了処理
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if erase_mode != MODE_NORMAL:
                        continue
                    x, y = self.to_index(event.pos)
                    if 0 <= x < N_DROP_X and 0 <= y < N_DROP_Y:
                        is_moving = True
                        moving_drop_pos = event.pos
                        moving_drop_index = (x, y)
                        moving_drop_type = self.drops[y][x]
                        self.drops[y][x] = 0
                if event.type == MOUSEMOTION:
                    if is_moving:
                        moving_drop_pos = event.pos
                        if moving_drop_pos[1] < OFFSET_Y:
                            moving_drop_pos = moving_drop_pos[0], OFFSET_Y
                        new_index = self.to_index(moving_drop_pos)
                        if not (0 <= new_index[0] < N_DROP_X and 0 <= new_index[1] < N_DROP_Y):
                            continue
                        if new_index != moving_drop_index:
                            self.drops[moving_drop_index[1]][moving_drop_index[0]] = self.drops[new_index[1]][new_index[0]]
                            self.drops[new_index[1]][new_index[0]] = 0
                            moving_drop_index = new_index
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    if is_moving:
                        is_moving = False
                        self.drops[moving_drop_index[1]][moving_drop_index[0]] = moving_drop_type
                        # erase
                        erase_drops = self.erase_drop()
                        erase_motion_count = 0
                        erase_mode = MODE_ERASE

            if erase_mode != MODE_NORMAL:
                if erase_motion_count == 0:
                    if erase_drops:
                        chain = erase_drops.pop(0)
                        for x, y in chain:
                            self.drops[y][x] = 0
                        # interval
                        erase_motion_count = FPS // 2
                    else:
                        has_erased = self.is_in_zero()
                        self.fall()
                        self.fall_new_drop()
                        if has_erased:
                            erase_drops = self.erase_drop()
                            erase_motion_count = FPS // 2
                        else:
                            erase_mode = MODE_NORMAL
                if erase_motion_count > 0:
                    erase_motion_count -= 1

            screen.fill((0,0,0))
            for y in range(N_DROP_Y):
                for x in range(N_DROP_X):
                    pos = self.to_pos(x, y)
                    self.draw_drop(pos, self.drops[y][x])

            if is_moving:
                self.draw_drop(moving_drop_pos, moving_drop_type)

            pygame.display.update() # 画面更新

    def draw_drop(self, pos, n):
        if 1 <= n <= 5:
            pygame.draw.circle(screen, self.to_color(n), pos, DROP_LENGTH // 2)
            pygame.draw.circle(screen, (255,255,255), pos, DROP_LENGTH // 2, 2)
        if n == 6:
            rect_length = int(DROP_LENGTH * 0.9)
            rect = pygame.locals.Rect(
                pos[0] - rect_length // 2,
                pos[1] - rect_length // 2,
                rect_length,
                rect_length,
            )
            pygame.draw.rect(screen, self.to_color(n), rect)
            pygame.draw.rect(screen, (255,255,255), rect, 2)

    def to_index(self, pos):
        x_index = pos[0] // DROP_LENGTH
        y_index =  (pos[1] - OFFSET_Y) // DROP_LENGTH
        return x_index, y_index

    def to_pos(self, x, y):
        pos_x = DROP_LENGTH * x + DROP_LENGTH // 2
        pos_y = DROP_LENGTH * y + DROP_LENGTH // 2 + OFFSET_Y
        return pos_x, pos_y

    def to_color(self, n):
        if n == 1:
            return (255, 96, 32)
        if n == 2:
            return (0, 192, 255)
        if n == 3:
            return (0, 192, 64)
        if n == 4:
            return (255, 255, 128)
        if n == 5:
            return (96, 0, 192)
        if n == 6:
            return (255, 160, 255)

    def is_in_zero(self):
        for y in range(N_DROP_Y):
            for x in range(N_DROP_X):
                if self.drops[y][x] == 0:
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
            self.chain_drops.append((x, y))
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