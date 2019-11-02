import random


class SkillsManager:
    def __init__(self, drops):
        self.drops = drops
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)
        self.N_DROP_ALL = self.N_DROP_X * self.N_DROP_Y
        self.N_COLOR = 6

    def drops_to_exist_5colors(self):
        N_LINED_DROP = 3 * 5
        choices = self._get_lined_drops()[:N_LINED_DROP] + \
            self._get_random_drops()[:self.N_DROP_ALL - N_LINED_DROP]
        self._set_drops(choices, is_shuffle=True)

    def drops_to_can_all_clear(self):
        self._set_drops(self._get_lined_drops(), is_shuffle=True)

    def drops_to_max_combo(self):
        self._set_drops(self._get_lined_drops())

    def drops_to_hanabi(self, drop_num):
        self._set_drops([drop_num] * self.N_DROP_ALL)

    def _get_lined_drops(self):
        return [(i // 3) % self.N_COLOR + 1 for i in range(self.N_DROP_ALL)]

    def _get_random_drops(self):
        return [random.randint(1, self.N_COLOR) for i in range(self.N_DROP_ALL)]

    def _set_drops(self, choices, is_shuffle=False):
        if is_shuffle:
            random.shuffle(choices)
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                self.drops[y][x] = choices.pop(0)
