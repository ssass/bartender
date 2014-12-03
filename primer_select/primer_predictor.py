import sys
import shlex
import subprocess

from Bio import SeqIO
from helpers.p3_parser import P3Parser
from helpers.primerpair import *
from helpers.primer import *


class PrimerPredictor:

    def __init__(self, config, input_handle, predefined_handle):
        self.config = config
        self.input_handle = input_handle
        self.predefined_handle = predefined_handle

    def parse_predefined_pairs(self, predefined_sets):

        for record in SeqIO.parse(self.predefined_handle, "fasta"):
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

                act_set.set.append(PrimerPair(Primer(seqs[0], None), Primer(seqs[1], None), record.id + "_" + str(pair_ind+1)))
            else:
                ps = PrimerPairSet(record.id)
                ps.set.append(PrimerPair(Primer(seqs[0], None),  Primer(seqs[1], None), record.id + "_" + str(pair_ind)))
                predefined_sets[record.id] = ps


    def predict_primer_set(self):

        predefined_sets = dict()
        if self.predefined_handle is not None:
            self.parse_predefined_pairs(predefined_sets)

        primer_sets = []
        for record in SeqIO.parse(self.input_handle, "fasta"):

            if record.id in predefined_sets:
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

            if target_start >= 0 and target_length >= 0:
                input_string += "SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length) + "\n"

            if exclude_start >= 0 and exclude_length >= 0:
                input_string += "SEQUENCE_EXCLUDED_REGION=" + str(exclude_start + 1) + "," + str(exclude_length) + "\n"

            input_string += "P3_FILE_FLAG=0\n"
            input_string += "PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + self.config.p3_thermo_path + "\n="

            cmd = self.config.p3_path + " -p3_settings_file=" + self.config.p3_config_path
            args = shlex.split(cmd)
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p3_output = p.communicate(input_string)[0].strip()

            m = re.search('(?<=PRIMER_ERROR=)\w+', p3_output)
            if m is not None:
                raise Exception("Error for sequence " + record.id + ": " + m.group(0))

            primer_set = PrimerPairSet(record.id)
            P3Parser.parse_p3_information(primer_set, p3_output)

            primer_sets.append(primer_set)

        for key in predefined_sets:
            print("WARNING: No input sequence could be found for the predefined primer " + key)

        return primer_sets
