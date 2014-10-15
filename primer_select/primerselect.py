import argparse

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the primer sequences in FASTA format", type=str)
args = parser.parse_args()

from Bio import SeqIO
handle = open(args.input, "rU")
for record in SeqIO.parse(handle, "fasta"):
    print record.seq
handle.close()