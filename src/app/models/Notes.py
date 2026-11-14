from enum import Enum
from random import shuffle

class NoteModes(Enum):
    FLATS = 0
    SHARPS = 1
    MIXED = 2


class Note():
    def __init__(self, note_string, mode = NoteModes.MIXED):
        self.note_string = note_string
        self.sharp_name = None
        self.flat_name = None
        self.mode = mode
        if "/" in note_string:
            self.sharp_name, self.flat_name = self.note_string.split("/")

    def display(self, mode=None):
        if mode is None:
            mode = self.mode
        if mode == NoteModes.FLATS:
            return self.flat_name if self.flat_name else self.note_string
        elif mode == NoteModes.SHARPS:
            return self.sharp_name if self.sharp_name else self.note_string
        else:
            return self.note_string

    def __str__(self):
        return self.display()

class Notes():
    def __init__(self, mode = NoteModes.MIXED):
        self.notes = list(map(Note, ["A", "A#/Bb", "B", "C", "C#/Db", "D",
                    "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]))
        self.notes_order = list(range(len(self.notes)))
        self._mode = mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        for n in self.notes:
            n.mode = self._mode

    def reshuffle(self):
        shuffle(self.notes_order)

    def __len__(self):
        return len(self.notes)

    def __iter__(self):
        for i in self.notes_order:
            yield self.notes[i]
