from __future__ import print_function
import argparse
from primer_select.blaster import Blaster
from primer_select.optimizer import Optimizer
from primer_select.primer_predictor import PrimerPredictor
from primer_select.ps_configuration import PsConfigurationHandler
from primer_select.rnacofolder import Cofolder

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format. "
                                  "The FASTA headers indicate the sequence ID and have to be unique.", type=str)
parser.add_argument("--predefined", dest="predefined", help="Input file containing sequences in FASTA format for predefined primer pairs. "
                                         "The primer pair sequences have to provided as \'fwdseq&revseq\'. "
                                   "The FASTA header of a given primer has to be specified according to the "
                                   "corresponding input sequence ID. "
                                   "If you want to specify more than one primer pair per input "
                                   "sequence, please add \'_0\', \'_1\' ... to the sequence ID.", type=str, default="")

args = parser.parse_args()

ch = PsConfigurationHandler("config.cfg")
config = ch.read_config()

primer_predictor = PrimerPredictor(config, args.input, args.predefined)
primer_sets = primer_predictor.predict_primer_set()

for primer_set in primer_sets:
    print(primer_set.name, "\n")
    for pair in primer_set.set:
        print (pair.name, "\t", pair.fwd, "/", pair.rev)
    print("\n")

blaster = Blaster(config, args.input)
blaster.blast_primer_set(primer_sets)

for primer_set in primer_sets:
    print(primer_set.name, "\n")
    for pair in primer_set.set:
        print (pair.name, "\t", pair.blast_hits[0], "/", pair.blast_hits[1])
    print("\n")

cofolder = Cofolder(config, args.input)
cofolder.cofold(primer_sets)

optimizer = Optimizer(config, primer_sets)
opt_result = optimizer.optimize()

print(opt_result.sum_mfe)
print(opt_result.opt_arrangement)

unique_indices = [len(opt_result.arrangements)-1]
last_mfe = opt_result.sum_mfe[len(opt_result.arrangements)-1]
for act_mfe in reversed(opt_result.sum_mfe):
        if act_mfe != last_mfe:
            unique_indices.append(act_mfe)

for i in unique_indices:
    print(i)
