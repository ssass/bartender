__author__ = 'Steffen'
from Bio import SeqIO
import shlex
import subprocess
from primer_select.primerpair import *


class PrimerPredictor:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def predict_primer_set(self):

        primer_sets = []
        handle = open(self.input, "rU")
        for record in SeqIO.parse(handle, "fasta"):
            sequence = str(record.seq)
            p3file = record.id + "_seq.txt"

            target_start = sequence.find("[")
            target_end = sequence.find("]")
            target_length = target_end - target_start - 1

            sequence = sequence.replace("[", "")
            sequence = sequence.replace("]", "")

            exclude_start = sequence.find("<")
            exclude_end = sequence.find(">")
            exclude_length = exclude_end - exclude_start - 1

            sequence = sequence.replace("<", "")
            sequence = sequence.replace(">", "")

            input_string = ""
            input_string += "SEQUENCE_ID=" + record.id + "\n"
            input_string += "SEQUENCE_TEMPLATE=" + sequence + "\n"

            if target_start >= 0 & target_length >= 0:
                input_string += "SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length) + "\n"

            if target_start >= 0 & target_length >= 0:
                input_string += "SEQUENCE_EXCLUDED_REGION=" + str(exclude_start + 1) + "," + str(exclude_length) + "\n"

            input_string += "P3_FILE_FLAG=0\n"
            input_string += "PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + self.config.p3_thermo_path + "\n="

            cmd = self.config.p3_path + " -format_output -p3_settings_file=" + self.config.p3_config_path
            args = shlex.split(cmd)
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p3_output = p.communicate(input_string)[0].strip()

            print record.id + " " + str(p3_output) + "\n"

            p3_output = p3_output.split("\n")
            primer_set = PrimerSet(record.id)
            for p3o in p3_output:
                p3_pairs = p3o.strip().split("\t")
                primer_set.append(PrimerPair(p3_pairs[0], p3_pairs[1]))

            primer_sets.append(primer_set)
        handle.close()

        return primer_sets
