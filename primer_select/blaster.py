__author__ = 'Steffen'
from __future__ import print_function
from Bio import SeqIO
import shlex
import subprocess
from primer_select.primerpair import PrimerPair
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq

class Blaster:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def blast_primer_set(self, primer_sets):

        num_hits = []

        cmd = self.config.blast_path + " -p blastn -m 8 -d " + self.config.blast_dbpath
        args = shlex.split(cmd)

        for primer_set in primer_sets:
            fwd_string = ""
            rev_string = ""
            for pair in primer_set.set:
                fwd_string += ">" + pair.name + "\n" + pair.fwd + "\n\n"
                rev_string += ">" + pair.name + "\n" + pair.rev + "\n\n"
                p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                blast_output = p.communicate(fwd_string)[0].strip()
                print(blast_output)
        return primer_set
