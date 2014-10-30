import sys

__author__ = 'Steffen'
from Bio import SeqIO
import shlex
import subprocess
from primer_select.primerpair import *


class PrimerPredictor:

    def __init__(self, config, fasta_file, predefined):
        self.config = config
        self.input = fasta_file
        self.predefined = predefined

    def parse_predefined_pairs(self, predefined_sets):
        handle = open(self.predefined, "rU")

        for record in SeqIO.parse(handle, "fasta"):
            seq = str(record.seq)

            if seq.find("&") == -1:
                print("Please specify fwd and rev primer sequences by separating them with \'&\' for the predefined "
                      "primer " + record.id + ".")
                sys.exit(1)

            seqs = seq.split("&")
            if len(seqs) != 2:
                print("Exactly two primer sequences (fwd&rev) have to provided for the predefined "
                      "primer " + record.id + ".")
                sys.exit(1)

            pair_ind = 0
            if record.id in predefined_sets:
                act_set = predefined_sets[record.id]
                for pair in act_set.set:
                    ind = int(pair.name.split("_")[1])
                    if ind > pair_ind:
                        pair_ind = ind
                act_set.set.append(PrimerPair(seqs[0], seqs[1], record.id + "_" + str(pair_ind+1)))
            else:
                ps = PrimerSet(record.id)
                ps.set.append(PrimerPair(seqs[0], seqs[1], record.id + "_" + str(pair_ind)))
                predefined_sets[record.id] = ps



    def predict_primer_set(self):
        predefined_sets = dict()
        if self.predefined != "":
            self.parse_predefined_pairs(predefined_sets)

        primer_sets = []
        handle = open(self.input, "rU")
        for record in SeqIO.parse(handle, "fasta"):

            if record.id in predefined_sets:
                print(record.id)
                primer_sets.append(predefined_sets[record.id])
                del predefined_sets[record.id]
                continue

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

            # print record.id + " " + str(p3_output) + "\n"

            p3_output = p3_output.split("\n")
            primer_set = PrimerSet(record.id)
            for i, p3o in enumerate(p3_output):
                p3_pairs = p3o.strip().split("\t")
                primer_set.append(PrimerPair(p3_pairs[0], p3_pairs[1], record.id + "_" + str(i)))

            primer_sets.append(primer_set)
        handle.close()

        return primer_sets
