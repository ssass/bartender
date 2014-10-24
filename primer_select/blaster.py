from __future__ import print_function
from multiprocessing import Process
from collections import deque
import shlex
import subprocess

class Blaster:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def run_process(self, primer_set, args):
        print("Blasting primer", primer_set.name, "...")
        blast_string = ""
        for pair in primer_set.set:
            blast_string += ">" + pair.name + "_fwd\n" + pair.fwd + "\n\n"
            blast_string += ">" + pair.name + "_rev\n" + pair.rev + "\n\n"

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        blast_output = p.communicate(blast_string)[0].strip()
        # print(blast_output)
        blast_output = blast_output.split("\n")
        blast_hits = []
        for line in blast_output:
            act_result = line.strip().split("\t")
            if float(act_result[10]) < 0.1:
                blast_hits.append(act_result[0])

        for pair in primer_set.set:
            pair.blast_hits[0] = blast_hits.count(pair.name + "_fwd")
            pair.blast_hits[1] = blast_hits.count(pair.name + "_rev")


    def blast_primer_set(self, primer_sets):

        cmd = self.config.blast_path + " -p blastn -m 8 -d " + self.config.blast_dbpath
        args = shlex.split(cmd)

        processes = deque()
        for primer_set in primer_sets:
            processes.append(Process(target=self.run_process, args=(primer_set,args, )))

        active_processes = 0
        while len(processes) > 0:
            p = processes.popleft()
            if active_processes < self.config.threads:
                p.start()
                active_processes += 1

            active_processes = 0
            for p in processes:
                if p.is_alive():
                    ++active_processes

            print (active_processes, len(processes))



        for p in processes:
            p.start()
        for p in processes:
            p.join()

        return primer_sets