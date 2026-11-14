from textual.app import App
from textual.containers import Center
import logging
import os

from datetime import datetime

from .models import Notes, Strings, NoteModes
from .views import MainView, SettingsScreen

logger = logging.getLogger(__name__)

class NotesApp(App):
    CSS_PATH = "views/style.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = NoteModes.MIXED
        self.notes = Notes(self._mode)
        self.strings = Strings()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.notes.mode = self._mode

    def on_mount(self):
        self.theme = "catppuccin-mocha"
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename=f"logs/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.push_screen(MainView())
        logger.info("App mounted")
