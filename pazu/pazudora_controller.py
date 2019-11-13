from screen import Screen
from view import View
from pazudora_view import PazudoraView
from sound_manager import SoundManager
from drops_manager import DropsManager
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN, K_SPACE
from pygame.key import get_pressed

class PazudoraController(Screen):
    def __init__(self):
        self.SCREEN_SIZE = (1000, 800)
        super().__init__()
        self.arrange_mode = 2
        self.touching_view = None

    def main(self):
        SoundManager.init()
        SoundManager().play_bgm()
        self._arrangement()
        super().main()

    def _arrangement(self):        
        DropsManager.CHAIN = 3
        DropsManager.IS_DIAGONAL = True
        if self.arrange_mode == 1:
            for i in range(2):
                for j in range(2):
                    PazudoraView(i*750, j*400, 250, 400)
            PazudoraView(300, 100, 400, 600)
        elif self.arrange_mode == 2:
            PazudoraView(0, 0, 1000, 800, 
                         n_drop_x=24, n_drop_y=10, combo_interval=0.1)

    def event(self, event, views):
        if self._is_multi_touch(event):
            self._all_move(event, views)
        else:
            super().event(event, views)

    def _all_move(self, event, views):
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
                per = self.touching_view.view_pos_to_per(pos)
                pos = view.per_to_view_pos(per)
                event.pos = view.get_pos_on_screen(pos)
            view.on_event(event)

    def _is_multi_touch(self, event):
        return self.is_mouse_action(event) and get_pressed()[K_SPACE]