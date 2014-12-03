
class Primer:
    def __init__(self, sequence, position, reverse=False):
        self.sequence = sequence
        self.position = position
        self.reverse = reverse

    def __len__(self):
        return len(self.sequence)

class PrimerSet:

    def __init__(self, name):
        self.name = name
        self.set = []

    def __len__(self):
        return len(self.set)

    def append(self, primer):
        self.set.append(primer)
