class DrawManager:
    def __init__(self, drops, screen, images):
        self.SCREEN = screen
        self.IMAGES = images
        self.N_DROP_X = len(drops[0])
        self.N_DROP_Y = len(drops)
        self.DROP_LENGTH = self.SCREEN.get_width() // self.N_DROP_X

    def is_in_drops_area(self, x, y):
        return 0 <= x < self.N_DROP_X and 0 <= y < self.N_DROP_Y

    def draw_drops(self, drops):
        for y in range(len(drops)):
            for x in range(len(drops[0])):
                pos = self.to_pos(x, y)
                self.draw_drop(drops[y][x], center=pos)

    def draw_drop(self, drop_num, left_up=None, center=None):
        if drop_num in self.IMAGES:
            image = self.IMAGES[drop_num]
            if center:
                x = center[0] - image.get_width() // 2
                y = center[1] - image.get_height() // 2
                left_up = (x, y)
            self.SCREEN.blit(image, left_up)

    def draw_text(self, screen, font, info_dict):
        y = 20
        for key in info_dict:
            text = f"{key}: {info_dict[key]}"
            sprite = font.render(text, True, (255, 255, 255))
            screen.blit(sprite, (20, y))
            y += 50

    def to_pos(self, x, y):
        OFFSET_Y = self.SCREEN.get_height() - self.DROP_LENGTH * self.N_DROP_Y
        pos_x = self.DROP_LENGTH * x + self.DROP_LENGTH // 2
        pos_y = self.DROP_LENGTH * y + self.DROP_LENGTH // 2 + OFFSET_Y
        return pos_x, pos_y

    def to_index(self, pos):
        OFFSET_Y = self.SCREEN.get_height() - self.DROP_LENGTH * self.N_DROP_Y
        x_index = pos[0] // self.DROP_LENGTH
        y_index = (pos[1] - OFFSET_Y) // self.DROP_LENGTH
        return x_index, y_index
