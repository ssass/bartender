from __future__ import print_function
import argparse
from primer_select.blaster import Blaster
from primer_select.optimizer import Optimizer
from primer_select.primer_predictor import PrimerPredictor
from primer_select.ps_configuration import PsConfigurationHandler
from primer_select.rnacofolder import Cofolder

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format", type=str)
args = parser.parse_args()

ch = PsConfigurationHandler("config.cfg")
config = ch.read_config()

primer_predictor = PrimerPredictor(config, args.input)
primer_sets = primer_predictor.predict_primer_set()

blaster = Blaster(config, args.input)
blaster.blast_primer_set(primer_sets)

# for primer_set in primer_sets:
#     print(primer_set.name, "\n")
#     for pair in primer_set.set:
#         print (pair.name, "\t", pair.blast_hits[0], "/", pair.blast_hits[1])
#     print("\n")

cofolder = Cofolder(config, args.input)
cofolder.cofold(primer_sets)

optimizer = Optimizer(config, primer_sets)
opt_result = optimizer.optimize()
