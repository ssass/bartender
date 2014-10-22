import argparse
import shlex
import subprocess
import time
from primer_select.primerpair import PrimerPair
from primer_select.ps_configuration import PsConfigurationHandler
import csv

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format", type=str)
args = parser.parse_args()

ch = PsConfigurationHandler("config.cfg")
config = ch.read_config()

from Bio import SeqIO

primer_set = []

handle = open(args.input, "rU")
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
    input_string += "PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + config.p3_thermo_path + "\n="

    cmd = config.p3_path + " -format_output -p3_settings_file=" + config.p3_config_path
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p3_output = p.communicate(input_string)[0].split("\n")

    primer_pairs = []
    for p3o in p3_output:
        p3_pairs = p3o.split("\t")
        print str(p3_pairs) + "\n"
        #primer_pairs.append(PrimerPair(p3_pairs[0], p3_pairs[1]))

    primer_set.append(primer_pairs)
handle.close()

print primer_set[0][1].rev + " " + primer_set[3][2].fwd