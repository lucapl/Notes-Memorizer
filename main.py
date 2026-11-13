from textual.app import App, ComposeResult, Screen
from textual.containers import Grid, Center
from textual.widgets import Static, Digits, Header, Footer, DataTable, Select
from rich.text import Text
import random
from datetime import datetime
import logging
import os
import time
from enum import Enum

logger = logging.getLogger(__name__)

class Notes_mode(Enum):
    FLATS = 0
    SHARPS = 1
    MIXED = 2

class Note():
    def __init__(self, note_string, mode = Notes_mode.MIXED):
        self.note_string = note_string
        self.sharp_name = None
        self.flat_name = None
        self._mode = mode
        if "/" in note_string:
            self.sharp_name, self.flat_name = self.note_string.split("/")

    def display(self, mode=None):
        if mode is None:
            mode = self.mode
        if mode == Notes_mode.FLATS:
            return self.flat_name if self.flat_name else self.note_string
        elif mode == Notes_mode.SHARPS:
            return self.sharp_name if self.sharp_name else self.note_string
        else:
            return self.note_string

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    def __str__(self):
        return self.display()


class NotesApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("space", "next_string", "Start/Next String"),
        ("backspace", "settings", "Settings")
        ]

    notes = list(map(Note, ["A", "A#/Bb", "B", "C", "C#/Db", "D",
             "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]))
    _mode = Notes_mode.MIXED
    notes_order = [i for i in range(len(notes))]
    strings = ["E2", "A3", "D3", "G3", "B4", "E4"]
    start_time = datetime.now()
    pauses = []
    end_time = datetime.now()
    running = False
    index = 0
    COUNTDOWN_S = 3
    countdown_count = 0

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.refresh_notes()
        self.refresh_strings()

    def compose(self):
        yield Header()
        yield Center(Grid(
            Center(Static(id="string"),id="string-container"),
            Center(DataTable(id="notes"),id="notes-container"),
            Center(Digits(id="clock",classes="clock success"))
        ))
        yield Footer()

    def on_mount(self):
        self.create_notes()
        self.refresh_strings()
        self.theme = "catppuccin-mocha"
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename=f"logs/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logger.info("App mounted")

    def create_notes(self):
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.add_column("id", width=3,key="id")
        table.add_column("Note", width=10)
        table.show_cursor = False
        #   table.show_header = False
        for i,string in enumerate(self.notes):
            table.add_row(i,Text(str(string), justify="center"))

    def refresh_notes(self):
        random.shuffle(self.notes_order)
        for note in self.notes:
            note.mode = self.mode
        table = self.query_one("#notes", DataTable)
        table.sort("id", key=lambda x: self.notes_order[x])

    def update_clock(self) -> None:
        if self.running:
            self.end_time = datetime.now()
        clock = self.end_time - self.start_time
        self.query_one(Digits).update(f"{clock}")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(0.01, self.update_clock)

    def next_string(self):
        #self.running = not self.running
        logger.debug(f"Is clock running?:{self.running}, String: {self.index}, {self.strings[self.index-1]}")
        self.index = (self.index + 1) % (len(self.strings)+1)
        if self.index == 0:
            self.refresh_clock()
            self.refresh_strings()
            self.running = False
            return
        elif self.index == 1:
            #self.countdown()
            self.start_clock()
            self.running = True
        text = self.strings[self.index-1]
        self.query_one("#string", Static).update(text)

    def refresh_clock(self):
        self.query_one(Digits).set_classes("clock success")
    
    async def countdown(self):
        self.countdown = self.COUNTDOWN_S
        await self.run_worker(1, self.countdown_step, repeat=self.COUNTDOWN_S)

    def countdown_step(self):
        self.query_one(Digits).update(f"{self.countdown}")
        self.countdown -= 1

    def start_clock(self):
        self.start_time = datetime.now()
        self.query_one(Digits).set_classes("clock running")

    def refresh_strings(self):
        random.shuffle(self.strings)
        self.index = 0
        text = "Press space to start"
        self.query_one("#string", Static).update(text)

    def action_refresh(self):
        self.refresh_clock()
        self.refresh_strings()
        self.running = False

    def action_next_string(self):
        self.next_string()
        self.refresh_notes()

    def action_settings(self):
        self.push_screen(SettingsScreen())

    # def on_key(self, event):
    #     if event.key == "enter":
    #         self.refresh_clock()
    #         self.refresh_strings()
    #     if event.key == "space":
    #         self.next_string()
    #         self.refresh_notes()

class SettingsScreen(Screen):
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("escape", "close", "Close"),
        ("q", "close", "Close")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(Static("Settings screen"))
        yield Center(Select(id="mode", prompt="Select mode:", options=[("Flats", Notes_mode.FLATS), ("Sharps", Notes_mode.SHARPS), ("Mixed", Notes_mode.MIXED)]))
        yield Footer()

    def action_close(self):
        self.app.pop_screen()

if __name__ == "__main__":
    NotesApp().run()