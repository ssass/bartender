from __future__ import print_function
import random
import math
import copy

class OptimizationResult:
    def __init__(self, opt_arrangement, arrangements, sum_mfe):
        self.opt_arrangement = opt_arrangement
        self.arrangements = arrangements
        self.sum_mfe = sum_mfe


class Optimizer:

    def __init__(self, config, primer_sets):
        self.config = config
        self.primer_sets = primer_sets

    def f(self, selected_pairs):
        sum_mfes = 0
        for seq1, pair1 in enumerate(selected_pairs):
            for seq2, pair2 in enumerate(selected_pairs):
                sum_mfes += self.primer_sets[seq1].mfes[pair1][seq2][pair2]
        return sum_mfes / 2

    def optimize(self):

        max_ind = self.config.opt_steps
        max_temperature = min(15, self.config.opt_max_temp)

        set_lengths = []
        for pset in self.primer_sets:
            set_lengths.append(random.randint(0, len(pset)-1))

        combinations = []
        act_temperature = max_temperature

        mfe_sum = []
        v = []
        for i, pset in enumerate(self.primer_sets):
            v.append(set_lengths[i])

        temp_steps = math.floor(max_ind/(max_temperature+1))

        for i in xrange(1, max_ind):
            if i % temp_steps == 0 & act_temperature != 0:
                --act_temperature

            j = random.randint(0, len(v)-1)

            for k in random.sample(xrange(0, set_lengths[j]), set_lengths[j]):
                v_temp = copy.copy(v)
                v_temp[j] = k
                if self.f(v_temp) <= self.f(v):
                    v[j] = k
                elif math.exp((self.f(v)-self.f(v_temp))/act_temperature) > random.uniform(0, 1):
                    v[j] = k

            print(v, self.f(v))
            combinations.append(v)
            mfe_sum.append(self.f(v))

        return OptimizationResult(v, combinations, mfe_sum)