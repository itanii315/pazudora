from screen import Screen
from pazudora_view import PazudoraView
from sound_manager import SoundManager

class PazudoraController(Screen):
    def __init__(self):
        self.SCREEN_SIZE = (1000, 500)
        super().__init__()

    def main(self):
        SoundManager.init()
        SoundManager().play_bgm()
        PazudoraView(0, 0, 300, 500, n_drop_x=8, n_drop_y=8)
        PazudoraView(300, 0, 300, 500)
        PazudoraView(800, 0, 200, 250)
        PazudoraView(800, 250, 200, 250)
        super().main()
