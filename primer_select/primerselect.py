import argparse

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the primer sequences in FASTA format", type=str)
args = parser.parse_args()

from Bio import SeqIO
handle = open(args.input, "rU")
for record in SeqIO.parse(handle, "fasta"):
    f = open(record.id, 'w')
    f.write("SEQUENCE_ID=" + record.id+ "\n")
    f.write("SEQUENCE_TEMPLATE=" + record.seq + "\n")
    f.write("P3_FILE_FLAG=1\n=")
handle.close()