from __future__ import print_function
import re
import shlex
from Bio import SeqIO
import subprocess
from helpers.p3_parser import P3Parser
from helpers.primer import PrimerSet
from helpers.primerpair import PrimerPairSet

class P3SeqResult:

    def __init__(self, spacing, interval):
        self.spacing = spacing
        self.interval = interval
        self.warning = ""
        self.error = ""

class P3Seq:

    def __init__(self, config, input_handle):
        self.config = config
        self.input_handle = input_handle


    def run(self, spacing_range, interval_range):
        output = dict()
        for record in SeqIO.parse(self.input_handle, "fasta"):
            act_list = []
            for i, spacing in enumerate(spacing_range):
                for j, interval in enumerate(interval_range):
                    sequence = str(record.seq)
                    target_start = sequence.find("[")
                    target_end = sequence.find("]")
                    target_length = target_end - target_start - 1
                    print(target_start, target_end, target_length)
                    sequence = sequence.replace("[", "")
                    sequence = sequence.replace("]", "")

                    exclude_start = sequence.find("<")
                    exclude_end = sequence.find(">")
                    exclude_length = exclude_end - exclude_start - 1

                    sequence = sequence.replace("<", "")
                    sequence = sequence.replace(">", "")

                    input_string = ""
                    input_string += "SEQUENCE_ID=" + record.id + "_" + spacing + "_" + interval + "\n"
                    input_string += "SEQUENCE_TEMPLATE=" + sequence + "\n"
                    input_string += "PRIMER_TASK=pick_sequencing_primers\n"
                    input_string += "PRIMER_SEQUENCING_SPACING=" + spacing + "\n"
                    input_string += "PRIMER_SEQUENCING_INTERVAL=" + interval + "\n"

                    if target_start >= 0 and target_length >= 0:
                        input_string += "SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length) + "\n"

                    if exclude_start >= 0 and exclude_end >= 0:
                        input_string += "SEQUENCE_EXCLUDED_REGION=" + str(exclude_start + 1) + "," + str(exclude_length) + "\n"

                    input_string += "P3_FILE_FLAG=0\n"
                    input_string += "PRIMER_EXPLAIN_FLAG=1\n"
                    input_string += "PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + self.config.p3_thermo_path + "\n="

                    cmd = self.config.p3_path + " -p3_settings_file=" + self.config.p3_config_path
                    args = shlex.split(cmd)
                    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    p3_output = p.communicate(input_string)[0].strip()

                    primer_set_fwd = PrimerSet(record.id + "_" + spacing + "_" + interval + "_left")
                    primer_set_rev = PrimerSet(record.id + "_" + spacing + "_" + interval + "_right")

                    m = re.search('(?<=PRIMER_ERROR=)\w+', p3_output)

                    result = P3SeqResult(spacing, interval)
                    if m is not None:
                        result.error = m.group(0)
                    elif p3_output != "":
                        result.warning = P3Parser.parse_p3seq_information(primer_set_fwd, primer_set_rev, p3_output)

                    result.primer_set_fwd = primer_set_fwd
                    result.primer_set_rev = primer_set_rev

            output[record.id] = act_list
            print(output.keys())
        return output

