import random
from sound_manager import SoundManager


class DropsManager:
    EMPTY = 0
    N_COLOR = 6

    @classmethod
    def new_drops(cls, x, y):
        return [[cls.get_random_drop() for i in range(x)] for j in range(y)]

    @classmethod
    def get_random_drop(self):
        return random.randint(1, self.N_COLOR)

    def __init__(self, drops, combo_interbal):
        self.drops = drops
        self.COMBO_INTERVAL = combo_interbal
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)

        self.will_erased_drops = []
        self.interval_count = 0
        self.is_erasing = False
        self.erase_combo = 0
        self.erased_colors = []

    def set_drop(self, indices, num):
        self.drops[indices[1]][indices[0]] = num

    def get_drop(self, indices):
        return self.drops[indices[1]][indices[0]]

    def is_empty(self, indices):
        return self.get_drop(indices) == self.EMPTY

    def remove_drop(self, pos):
        self.set_drop(pos, self.EMPTY)

    def is_action_timing(self):
        if self.is_erasing:
            self.interval_count -= 1
            return (self.interval_count <= 0)
        return False

    def action(self):
        if self.can_erase():
            self.erase()
        elif self.can_fall():
            self.fall()
            self.reset_will_erased_drops()
        else:
            self.finish_erase()

    def can_erase(self):
        return bool(self.will_erased_drops)

    def can_fall(self):
        return self.exists_in_drops(self.EMPTY)

    def exists_in_drops(self, drop_num):
        for row in self.drops:
            if drop_num in row:
                return True
        return False

    def erase(self):
        self.erase_combo += 1
        SoundManager().play_se_combo(min(self.erase_combo, 12))
        chain = self.will_erased_drops.pop(0)
        for x, y, drop_num in chain:
            self.remove_drop((x, y))
            if drop_num not in self.erased_colors:
                self.erased_colors.append(drop_num)
                self.erased_colors.sort()
        self.reset_interval()

    def fall(self):
        self._fall_exist_drops()
        self._fall_new_drops()

    def reset_will_erased_drops(self):
        self.will_erased_drops = self._get_will_erased_drops()
        if self.will_erased_drops:
            self.reset_interval()
        else:
            self.finish_erase()

    def reset_interval(self):
        self.interval_count = self.COMBO_INTERVAL

    def start_erase(self):
        self.erase_combo = 0
        self.is_erasing = True
        self.will_erased_drops = self._get_will_erased_drops()

    def finish_erase(self):
        self.interval_count = 0
        self.is_erasing = False

    def swap(self, pos1, pos2):
        tmp = self.drops[pos1[1]][pos1[0]]
        self.drops[pos1[1]][pos1[0]] = self.drops[pos2[1]][pos2[0]]
        self.drops[pos2[1]][pos2[0]] = tmp

    def _fall_new_drops(self):
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                if self.is_empty((x, y)):
                    self.set_drop((x, y), self.get_random_drop())

    def _fall_exist_drops(self):
        for y in range(self.N_DROP_Y)[::-1]:
            for x in range(self.N_DROP_X):
                if self.is_empty((x, y)):
                    above_y = self._get_above_drop_y(x, y)
                    self.swap((x, y), (x, above_y))

    def _get_above_drop_y(self, x, y):
        for i in range(y)[::-1]:
            if not self.is_empty((x, i)):
                return i
        return y

    def _get_will_erased_drops(self):
        line_drops = self._get_lined_drops(3)
        chain_drops_list = self._get_chain_drops_list(line_drops)
        return chain_drops_list

    def _get_lined_drops(self, n):
        lined_drops = [[self.EMPTY for i in range(self.N_DROP_X)]
                       for j in range(self.N_DROP_Y)]
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X - n + 1):
                drop_type = self.drops[y][x]
                for i in range(n):
                    if self.drops[y][x+i] != drop_type:
                        break
                else:
                    for i in range(n):
                        lined_drops[y][x+i] = drop_type

        for x in range(self.N_DROP_X):
            for y in range(self.N_DROP_Y - n + 1):
                drop_type = self.drops[y][x]
                for i in range(n):
                    if self.drops[y+i][x] != drop_type:
                        break
                else:
                    for i in range(n):
                        lined_drops[y+i][x] = drop_type

        for x in range(self.N_DROP_X - n + 1):
            for y in range(self.N_DROP_Y - n + 1):
                drop_type = self.drops[y][x]
                for i in range(n):
                    if self.drops[y+i][x+i] != drop_type:
                        break
                else:
                    for i in range(n):
                        lined_drops[y+i][x+i] = drop_type

        for x in range(self.N_DROP_X - n + 1):
            for y in range(self.N_DROP_Y - n + 1):
                drop_type = self.drops[y+n-1][x]
                for i in range(n):
                    if self.drops[y+n-1-i][x+i] != drop_type:
                        break
                else:
                    for i in range(n):
                        lined_drops[y+n-1-i][x+i] = drop_type

        return lined_drops

    def _get_chain_drops_list(self, line_drops):
        self.line_drops = line_drops
        self.checked_drops = [[self.EMPTY for i in range(self.N_DROP_X)]
                              for j in range(self.N_DROP_Y)]
        chain_drops_list = []
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                if line_drops[y][x]:
                    self.chain_drops = []
                    self._find_chain(x, y, line_drops[y][x])
                    if self.chain_drops:
                        chain_drops_list.append(self.chain_drops)

        return chain_drops_list

    def _find_chain(self, x, y, n):
        is_in_drops_area = (0 <= x < self.N_DROP_X and 0 <= y < self.N_DROP_Y)
        if not is_in_drops_area or self.checked_drops[y][x]:
            return

        if self.line_drops[y][x] == n:
            self.chain_drops.append((x, y, n))
            self.checked_drops[y][x] = True
            self._find_chain(x - 1, y, n)
            self._find_chain(x + 1, y, n)
            self._find_chain(x, y - 1, n)
            self._find_chain(x, y + 1, n)
            self._find_chain(x - 1, y - 1, n)
            self._find_chain(x + 1, y - 1, n)
            self._find_chain(x - 1, y + 1, n)
            self._find_chain(x + 1, y + 1, n)
