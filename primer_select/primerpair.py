class PrimerSet:
    def __init__(self, name):
        self.name = name
        self.set = []

    def __len__(self):
        len(self.set)

    def append(self, primer_pair):
        self.set.append(primer_pair)


class PrimerPair:
    def __init__(self, fwd, rev, name):
        self.fwd = fwd
        self.rev = rev
        self.name = name
        self.blast_hits  = [0, 0]