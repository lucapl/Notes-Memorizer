from random import shuffle

class Strings():

    def __init__(self):
        self.strings = ["E2", "A3", "D3", "G3", "B4", "E4"]
        self.string_order = list(range(len(self.strings)))

    def reshuffle(self):
        shuffle(self.string_order)

    def __iter__(self):
        for i in self.string_order:
            yield self.strings[i]

    def __getitem__(self, key):
        return self.strings[self.string_order[key]]

    def __len__(self):
        return len(self.strings)
