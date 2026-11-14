from textual.app import Screen
from textual.containers import Grid, Center
from textual.widgets import Static, Digits, Header, Footer, DataTable, Select
from rich.text import Text

from datetime import datetime

import logging
import os

from app.models import Notes, NoteModes, Strings
from .SettingsScreen import SettingsScreen

logger = logging.getLogger(__name__)

class MainView(Screen):
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("space", "next_string", "Start/Next String"),
        ("backspace", "settings", "Settings"),
    ]

    start_time = datetime.now()
    pauses = []
    end_time = datetime.now()
    running = False
    index = 0
    COUNTDOWN_S = 3
    countdown_count = 0

    def compose(self):
        yield Header()
        yield Center(Grid(
            Center(Static(id="string"),id="string-container"),
            Center(DataTable(id="notes"),id="notes-container"),
            Center(Digits(id="clock",classes="clock success"))
        ))
        yield Footer()

    @property
    def notes(self):
        return self.app.notes

    @property
    def mode(self):
        return self.app.mode

    @property
    def strings(self):
        return self.app.strings

    def on_mount(self):
        self.create_notes()
        self.refresh_strings()

    def create_notes(self):
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.add_column("id", width=3,key="id")
        table.add_column("Note", width=10)
        table.show_cursor = False
        #   table.show_header = False
        for i,note in enumerate(self.notes):
            table.add_row(i,Text(str(note), justify="center"))

    def refresh_notes(self):
        self.notes.reshuffle()

        table = self.query_one("#notes", DataTable)
        table.sort("id", key=lambda x: self.notes.notes_order[x])

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
        self.strings.reshuffle()
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
        self.app.push_screen(SettingsScreen())

    # def on_key(self, event):
    #     if event.key == "enter":
    #         self.refresh_clock()
    #         self.refresh_strings()
    #     if event.key == "space":
    #         self.next_string()
    #         self.refresh_notes()