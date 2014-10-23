__author__ = 'Steffen'
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
        fwd_string = ""
        rev_string = ""

        for primer_set in primer_sets:
            for pair in primer_set.set:
                fwd_string += ">" + primer_set.name + "\n" + pair.fwd + "\n\n"
                rev_string += ">" + primer_set.name + "\n" + pair.rev + "\n\n"

        cmd = self.config.blast_path + " -p blastn -m 8 -d " + self.config.blast_dbpath
        args = shlex.split(cmd)
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        blast_output = p.communicate(fwd_string)[0].strip()
        print fwd_string
        return primer_set
