from screen import Screen
from view import View
from pazudora_view import PazudoraView
from sound_manager import SoundManager
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN

class PazudoraController(Screen):
    def __init__(self):
        # config
        self.SCREEN_SIZE = (1000, 800)
        self.is_all_move = True

        super().__init__()
        self.touching_view = None

    def main(self):
        SoundManager.init()
        SoundManager().play_bgm()
        for i in range(4):
            for j in range(2):
                PazudoraView(i*250, j*400, 250, 400)
        super().main()

    def event(self, event, views):
        if self.is_all_move:
            self.all_move(event, views)
        else:
            super().event(event, views)

    def all_move(self, event, views):
        if event.type == MOUSEBUTTONDOWN:
            for view in views:
                pos = view.get_pos_on_view(event.pos)
                if view.is_in_view(pos):
                    self.touching_view = view
        elif event.type == MOUSEBUTTONUP:
            self.touching_view = None

        if self.is_mouse_action(event):
            original_pos = event.pos
        for view in views:
            if self.touching_view and self.is_mouse_action(event):
                pos = self.touching_view.get_pos_on_view(original_pos)
                event.pos = view.get_pos_on_screen(pos)
            view.on_event(event)
