import argparse
import subprocess
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
    p3file = record.id + "_seq.txt"
    f = open(p3file, 'w')
    f.write("SEQUENCE_ID=" + record.id + "\n")
    f.write("SEQUENCE_TEMPLATE=" + str(record.seq) + "\n")
    f.write("P3_FILE_FLAG=1\n")
    f.write("PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + config.p3_thermo_path + "\n=")
    cmd = [config.p3_path, "-format_output", "-p3_settings_file=" + config.p3_config_path, "-output=" + record.id + "_p3.txt", p3file]
    print cmd
    subprocess.Popen(cmd)
handle.close()

