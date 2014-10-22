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
    f = open(p3file, 'w')
    f.write("SEQUENCE_ID=" + record.id + "\n")
    f.write("SEQUENCE_TEMPLATE=" + sequence + "\n")

    target_start = sequence.find("\[")
    target_end = sequence.find("\]")
    target_length = target_end - target_start - 1

    if target_start >= 0 & target_length >= 0:
        f.write("SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length) + "\n")

    exclude_start = sequence.find("<")
    exclude_end = sequence.find(">")
    exclude_length = exclude_end - exclude_start - 1

    if target_start >= 0 & target_length >= 0:
        f.write("SEQUENCE_EXCLUDED_REGION=" + str(exclude_start) + "," + str(exclude_length) + "\n")

    f.write("P3_FILE_FLAG=1\n")
    f.write("PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + config.p3_thermo_path + "\n=")

    # print cmd
    cmd = config.p3_path + " -format_output -p3_settings_file=" + config.p3_config_path + " -output=" + record.id + "_p3.txt < " + p3file
    #print cmd
    args = shlex.split(cmd)
    # print args
    p = subprocess.Popen(args)
    #time.sleep(10)
handle.close()
time.sleep(5)
