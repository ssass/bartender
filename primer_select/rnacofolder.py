from __future__ import print_function
import shlex
import subprocess

class Cofolder:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def cofold(self, primer_sets):

        cofold_string = ""
        for i in xrange(0, len(primer_sets)):
            for j in xrange(i, len(primer_sets)):
                for pair1 in primer_sets[i].set:
                    for pair2 in primer_sets[j].set:
                        cofold_string += ">" + pair1.name + "_fwd" + "&" + pair2.name +"_fwd" + "\n"
                        cofold_string += pair1.fwd + "&" + pair2.fwd + "\n"
                        cofold_string += ">" + pair1.name + "_rev" + "&" + pair2.name +"_rev" + "\n"
                        cofold_string += pair1.rev + "&" + pair2.rev + "\n"
                        cofold_string += ">" + pair1.name + "_fwd" + "&" + pair2.name +"_rev" + "\n"
                        cofold_string += pair1.fwd + "&" + pair2.rev + "\n"
                        cofold_string += ">" + pair1.name + "_rev" + "&" + pair2.name +"_fwd" + "\n"
                        cofold_string += pair1.rev + "&" + pair2.fwd + "\n"

        print(cofold_string)
        return primer_sets
