import random

class DropsManager:
    @classmethod
    def new_drops(cls, x, y):
        return [[random.randint(1, 6) for i in range(x)] for j in range(y)]

    def __init__(self, drops, sounds, combo_interbal):
        self.drops = drops
        self.COMBO_INTERVAL = combo_interbal
        self.SOUNDS = sounds
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)

        self.will_erased_drops = []
        self.erase_motion_count = 0
        self.is_erasing = False
        self.erase_combo = 0
        self.erased_colors = []

    def is_time_to_erase(self):
        if self.is_erasing:
            self.erase_motion_count -= 1
            return self.erase_motion_count <= 0

    def can_erase(self):
        return bool(self.will_erased_drops)

    def can_fall(self):
        for row in self.drops:
            if 0 in row:
                return True
        return False

    def erase(self):
        self.erase_combo += 1
        sound_num = min(self.erase_combo, 12)
        self.SOUNDS["se_006p%03d.ogg" % sound_num].play()
        chain = self.will_erased_drops.pop(0)
        for x, y, n in chain:
            self.drops[y][x] = 0
            if n not in self.erased_colors:
                self.erased_colors.append(n)
                self.erased_colors.sort()
        self.reset_interval()
    
    def fall(self):
        self.fall_exist_drops()
        self.fall_new_drops()
        self.will_erased_drops = self.get_will_erased_drops()
        if self.will_erased_drops:
            self.reset_interval()
        else:
            self.finish_erase()

    def reset_interval(self):
        self.erase_motion_count = self.COMBO_INTERVAL

    def start_erase(self):
        self.erase_combo = 0
        self.is_erasing = True
        self.will_erased_drops = self.get_will_erased_drops()

    def finish_erase(self):
        self.erase_motion_count = 0
        self.is_erasing = False
    
    def fall_new_drops(self):
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                if self.drops[y][x] == 0:
                    self.drops[y][x] = random.randint(1, 6)

    def fall_exist_drops(self):
        for y in range(self.N_DROP_Y)[::-1]:
            for x in range(self.N_DROP_X):
                if self.drops[y][x] == 0:
                    self.drops[y][x] = self.rob_above(x, y)

    def rob_above(self, x, y):
        for i in range(y)[::-1]:
            if self.drops[i][x]:
                result = self.drops[i][x]
                self.drops[i][x] = 0
                return result
        return self.drops[y][x]

    def get_will_erased_drops(self):
        line_drops = self.get_line_drops()
        chain_drops_list = self.get_chain_drops_list(line_drops)
        return chain_drops_list

    def get_line_drops(self):
        line_drops = [[0 for i in range(self.N_DROP_X)] for j in range(self.N_DROP_Y) ]
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X - 2):
                if self.drops[y][x] == self.drops[y][x+1] == self.drops[y][x+2]:
                    drop_type = self.drops[y][x]
                    line_drops[y][x] = drop_type
                    line_drops[y][x+1] = drop_type
                    line_drops[y][x+2] = drop_type
        
        for x in range(self.N_DROP_X):
            for y in range(self.N_DROP_Y - 2):
                if self.drops[y][x] == self.drops[y+1][x] == self.drops[y+2][x]:
                    drop_type = self.drops[y][x]
                    line_drops[y][x] = drop_type
                    line_drops[y+1][x] = drop_type
                    line_drops[y+2][x] = drop_type

        return line_drops

    def get_chain_drops_list(self, line_drops):
        self.line_drops = line_drops
        self.checked_drops = [[0 for i in range(self.N_DROP_X)] for j in range(self.N_DROP_Y)]
        chain_drops_list = []
        for y in range(self.N_DROP_Y):
            for x in range(self.N_DROP_X):
                if line_drops[y][x]:
                    self.chain_drops = []
                    self.find_chain(x, y, line_drops[y][x])
                    if self.chain_drops:
                        chain_drops_list.append(self.chain_drops)

        return chain_drops_list
        
    def find_chain(self, x, y, n):
        if not (0 <= x < self.N_DROP_X and 0 <= y < self.N_DROP_Y):
            return
        if self.checked_drops[y][x]:
            return

        if self.line_drops[y][x] == n:
            self.chain_drops.append((x, y, n))
            self.checked_drops[y][x] = True
        else:
            return

        self.find_chain(x - 1, y, n)
        self.find_chain(x + 1, y, n)
        self.find_chain(x, y - 1, n)
        self.find_chain(x, y + 1, n)
