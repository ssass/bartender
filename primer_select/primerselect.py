import argparse
import shlex
import subprocess
import time
from primer_select.ps_configuration import PsConfigurationHandler
import csv

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format", type=str)
args = parser.parse_args()

ch = PsConfigurationHandler("config.cfg")
config = ch.read_config()

from Bio import SeqIO

handle = open(args.input, "rU")
for record in SeqIO.parse(handle, "fasta"):
    sequence = str(record.seq)
    p3file = record.id + "_seq.txt"

    input_String = ""
    #f = open(p3file, 'w')
    input_String += "SEQUENCE_ID=" + record.id + "\n"
    input_String += "SEQUENCE_TEMPLATE=" + sequence + "\n"

    target_start = sequence.find("\[")
    target_end = sequence.find("\]")
    target_length = target_end - target_start - 1

    if target_start >= 0 & target_length >= 0:
        input_String += "SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length) + "\n"

    exclude_start = sequence.find("<")
    exclude_end = sequence.find(">")
    exclude_length = exclude_end - exclude_start - 1

    if target_start >= 0 & target_length >= 0:
        input_String += "SEQUENCE_EXCLUDED_REGION=" + str(exclude_start) + "," + str(exclude_length) + "\n"

    input_String += "P3_FILE_FLAG=1\n"
    input_String += "PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + config.p3_thermo_path + "\n="

    # print cmd
    cmd = config.p3_path + " -format_output -p3_settings_file=" + config.p3_config_path + " -output=" + record.id + "_p3.txt"
    print cmd
    args = shlex.split(cmd)
    # print args
    p = subprocess.call(args, stdin=subprocess.PIPE)
    p.communicate(input_String)
handle.close()
#time.sleep(5)
