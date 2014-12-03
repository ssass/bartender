from __future__ import print_function
from primer_select.blaster import Blaster
from primer_select.optimizer import Optimizer
from primer_select.primer_predictor import PrimerPredictor
from primer_select.rnacofolder import Cofolder
from operator import itemgetter

class PrimerSelect:

    @staticmethod
    def output(arrangements, primer_sets):
        output_string = ""

        for i, run in enumerate(arrangements[0:5]):
            output_string += "Rank " + str(i + 1) + ": Sum MFE=" + str(run[0]) + "\n"

            v = run[1]
            for j, pset in enumerate(primer_sets):
                pair = pset.set[v[j]]
                output_string += pset.name + "\tfwd: " + pair.fwd.sequence.upper() + "\trev: " \
                                 + pair.rev.sequence.upper() + "\tBLAST hits: " \
                                 + str(pair.fwd.blast_hits) + " / " + str(pair.rev.blast_hits) + "\n"
            output_string += "------------------\n"
        return output_string


    @staticmethod
    def optimize(config, primer_sets):
        cofolder = Cofolder(config)
        cofolder.cofold(primer_sets)

        optimizer = Optimizer(config, primer_sets)
        opt_result = optimizer.optimize()
        return opt_result


    @staticmethod
    def predict_primerset(config, input_handle, predefined_handle):
        primer_predictor = PrimerPredictor(config, input_handle, predefined_handle)
        primer_sets = primer_predictor.predict_primer_set()

        blaster = Blaster(config)
        blaster.blast_primer_set(primer_sets)
        return primer_sets
