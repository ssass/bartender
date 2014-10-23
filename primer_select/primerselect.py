import argparse
from primer_select.blaster import Blaster
from primer_select.primer_predictor import PrimerPredictor
from primer_select.ps_configuration import PsConfigurationHandler

parser = argparse.ArgumentParser(description='Run the PrimerSelect pipeline.')

parser.add_argument("input", help="Input file containing the sequences in FASTA format", type=str)
args = parser.parse_args()

ch = PsConfigurationHandler("config.cfg")
config = ch.read_config()

primer_predictor = PrimerPredictor(config, args.input)
primer_sets = primer_predictor.predict_primer_set()

blaster = Blaster(config, args.input)
blaster.blast_primer_set(primer_sets)
