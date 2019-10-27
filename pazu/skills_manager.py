import random


class SkillsManager:
    def __init__(self, drops):
        self.drops = drops
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)

    def drops_to_exist_5colors(self):
        n_prepare_drops = 3 * 5
        choices = [(i // 3) % 6 + 1 for i in range(n_prepare_drops)]
        choices += [random.randint(1, 6) for i in
                    range(self.N_DROP_X * self.N_DROP_Y - n_prepare_drops)]
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                index = random.randrange(len(choices))
                self.drops[y][x] = choices.pop(index)

    def drops_to_can_all_clear(self):
        choices = [(i // 3) %
                   6 + 1 for i in range(self.N_DROP_X * self.N_DROP_Y)]
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                index = random.randrange(len(choices))
                self.drops[y][x] = choices.pop(index)

    def drops_to_max_combo(self):
        choices = [(i // 3) %
                   6 + 1 for i in range(self.N_DROP_X * self.N_DROP_Y)]
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                self.drops[y][x] = choices.pop(0)

    def drops_to_hanabi(self, n):
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                self.drops[y][x] = n
