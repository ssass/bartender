from __future__ import print_function
from primer_select.blaster import Blaster
from primer_select.optimizer import Optimizer
from primer_select.primer_predictor import PrimerPredictor
from primer_select.rnacofolder import Cofolder

class PrimerSelect:

    @staticmethod
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
