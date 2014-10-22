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
    # print str(target_start) + "\n"
    # print target_length
    #
    print "SEQUENCE_TARGET=" + str(target_start) + "," + str(target_length)

  # exclude.start=regexpr("<",act.seq.ann,fixed=T)[1]
  # exclude.length=regexpr(">",act.seq.ann,fixed=T)[1]-exclude.start-1
  # if (exclude.start >(-1) & exclude.length > (-1))write(paste("SEQUENCE_EXCLUDED_REGION=",exclude.start,",",exclude.length,sep=""),file=paste("../p3_input/seq",i,".txt",sep=""),append=T)
  #


    f.write("P3_FILE_FLAG=1\n")
    f.write("PRIMER_THERMODYNAMIC_PARAMETERS_PATH=" + config.p3_thermo_path + "\n=")

    #print cmd
    cmd = config.p3_path + " -format_output -p3_settings_file=" + config.p3_config_path + " -output=" + record.id + "_p3.txt "+ p3file
    #print cmd
    args = shlex.split(cmd)
    print args
    p = subprocess.Popen(args)
    #time.sleep(10)
handle.close()

