from __future__ import print_function
import argparse
import os
from Bio import SeqIO
from primer_select.blaster import Blaster
from primer_select.optimizer import Optimizer
from primer_select.primer_predictor import PrimerPredictor
from primer_select.ps_configuration import PsConfigurationHandler
from primer_select.rnacofolder import Cofolder


def output(opt_result, primer_sets):
    unique_indices = [0]
    last_mfe = opt_result.sum_mfe[0]

    for i, act_mfe in enumerate(opt_result.sum_mfe):
        if act_mfe != last_mfe:
            unique_indices.append(i)
            last_mfe = act_mfe

    for rank, i in enumerate(unique_indices[0:10]):
        print("Rank " + str(rank + 1) + ": Sum MFE=" + str(opt_result.sum_mfe[i]))

        v = opt_result.arrangements[i]
        for j, pset in enumerate(primer_sets):
            pair = pset.set[v[j]]
            print(pset.name + "\tfwd: " + pair.fwd + "\trev: " + pair.rev + "\tBLAST hits: " +
                  str(pair.blast_hits[0]) + " / " + str(pair.blast_hits[1]))
        print("------------------\n")


def optimize(config, primer_sets):
    cofolder = Cofolder(config, args.input)
    cofolder.cofold(primer_sets)

    optimizer = Optimizer(config, primer_sets)
    opt_result = optimizer.optimize()
    return opt_result


def start_process(config, input_handle, predefined_handle):
    primer_predictor = PrimerPredictor(config, input_handle, predef_handle)
    primer_sets = primer_predictor.predict_primer_set()

    blaster = Blaster(config, args.input)
    blaster.blast_primer_set(primer_sets)
    return primer_sets


parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format. "
                                  "The FASTA headers indicate the sequence ID and have to be unique.", type=str)
parser.add_argument("-predefined", dest="predefined",
                    help="Input file containing sequences in FASTA format for predefined primer pairs. "
                         "The primer pair sequences have to provided as \'fwdseq&revseq\'. "
                         "The FASTA header of a given primer has to be specified according to the "
                         "corresponding input sequence ID. "
                         "If you want to specify more than one primer pair per input "
                         "sequence, please add \'_0\', \'_1\' ... to the sequence ID.", type=str, default="")

args = parser.parse_args()

if not os.path.isfile("config.cfg"):
    PsConfigurationHandler.write_standard_config("config.cfg")

config_handle = open("config.cfg", 'rU')
config = PsConfigurationHandler.read_config(config_handle)
config_handle.close()

if args.predefined != "":
    predef_handle = open(args.predefined, 'rU')
else:
    predef_handle = None

input_handle = open(args.input, 'rU')

if args.predefined != "":
    predef_handle.close()


primer_sets = start_process(config, input_handle, predef_handle)
opt_result = optimize(config, primer_sets)
output(opt_result, primer_sets)




