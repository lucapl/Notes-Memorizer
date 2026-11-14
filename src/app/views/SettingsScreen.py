from textual import on
from textual.app import Screen, ComposeResult
from textual.widgets import Static,Select,Header,Footer
from textual.containers import Center
from app.models import NoteModes

class SettingsScreen(Screen):
    #CSS_PATH = "style.tcss"
    BINDINGS = [
        ("backspace", "close", "Close"),
        ("q", "close", "Close")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(Static("Settings screen"))
        yield Center(Select(id="mode",
                            prompt="Select mode:",
                            options=[
                                ("Flats", NoteModes.FLATS),
                                ("Sharps", NoteModes.SHARPS),
                                ("Mixed", NoteModes.MIXED)]))
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event):
        self.app.mode = event.value


    def action_close(self):
        self.app.pop_screen()

