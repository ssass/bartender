from __future__ import print_function
import shlex
import subprocess

class Cofolder:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def cofold(self, primer_sets):

        cofold_string = ""
        pos = 0
        positions = dict()

        for i in xrange(0, len(primer_sets)):
            for j in xrange(i+1, len(primer_sets)):
                for pair1 in primer_sets[i].set:
                    for pair2 in primer_sets[j].set:
                        positions[pair1.name + "&" + pair2.name] = pos
                        pos += 12
                        cofold_string += ">" + pair1.name + "_fwd" + "&" + pair2.name +"_fwd" + "\n"
                        cofold_string += pair1.fwd + "&" + pair2.fwd + "\n"
                        cofold_string += ">" + pair1.name + "_rev" + "&" + pair2.name +"_rev" + "\n"
                        cofold_string += pair1.rev + "&" + pair2.rev + "\n"
                        cofold_string += ">" + pair1.name + "_fwd" + "&" + pair2.name +"_rev" + "\n"
                        cofold_string += pair1.fwd + "&" + pair2.rev + "\n"
                        cofold_string += ">" + pair1.name + "_rev" + "&" + pair2.name +"_fwd" + "\n"
                        cofold_string += pair1.rev + "&" + pair2.fwd + "\n"

        cmd = self.config.rnacf_path + " -noPS"
        args = shlex.split(cmd)

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        rnac_output = p.communicate(cofold_string)[0].strip()

        for pos in positions:
            print(pos, positions[pos])

        return primer_sets
