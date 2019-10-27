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

    def draw_drop(self, n, left_up=None, center=None):
        if n in self.IMAGES:
            image = self.IMAGES[n]
            if center:
                left_up = center[0] - image.get_width() // 2, center[1] - image.get_height() // 2
            self.SCREEN.blit(image, left_up)

    def draw_text(self, screen, font, dictionary):
        y = 20
        for key in dictionary:
            sprite = font.render(f"{key}: {dictionary[key]}", True, (255, 255, 255))
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
        y_index =  (pos[1] - OFFSET_Y) // self.DROP_LENGTH
        return x_index, y_index