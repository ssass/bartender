from __future__ import print_function
from multiprocessing import Process, Queue
from collections import deque
import shlex
import subprocess
import sys


class Blaster:

    def __init__(self, config, fasta_file):
        self.config = config
        self.input = fasta_file

    def run_process(self, primer_set, args, q):
        print("Blasting primer", primer_set.name, "...")
        blast_string = ""
        for pair in primer_set.set:
            blast_string += ">" + pair.name + "_fwd\n" + pair.fwd + "\n\n"
            blast_string += ">" + pair.name + "_rev\n" + pair.rev + "\n\n"

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        blast_output = p.communicate(blast_string)[0].strip()
        blast_output = blast_output.split("\n")
        blast_hits = []
        for line in blast_output:
            act_result = line.strip().split("\t")
            if float(act_result[10]) < 0.1:
                blast_hits.append(act_result[0])

        for pair in primer_set.set:
            pair.blast_hits[0] = blast_hits.count(pair.name + "_fwd")
            pair.blast_hits[1] = blast_hits.count(pair.name + "_rev")

        q.put(primer_set)

    def blast_primer_set(self, primer_sets):

        cmd = self.config.blast_path + " -p blastn -m 8 -d " + self.config.blast_dbpath
        args = shlex.split(cmd)

        # start parallel BLAST processes and ensure that the number of threads does not exceed the maximum
        q = Queue()
        processes = deque()
        for i, primer_set in enumerate(primer_sets):
            primer_set.index = i
            processes.append(Process(target=self.run_process, args=(primer_set, args, q, )))

        active_processes = []
        while len(processes) > 0:

            if len(active_processes) < self.config.max_threads:
                p = processes.popleft()
                p.start()
                active_processes.append(p)

            for ap in active_processes:
                if not ap.is_alive():
                    active_processes.remove(ap)

        # wait until all processes have finished
        for p in active_processes:
            p.join()

        while not q.empty():
            primer_set_q = q.get()
            new_set = []
            for i, pair in enumerate(primer_set_q.set):
                print(i, len(primer_set_q))
                print(self.config.blast_max_hits, pair.blast_hits)
                if pair.blast_hits[0] <= self.config.blast_max_hits and pair.blast_hits[1] <= self.config.blast_max_hits:
                    new_set.append(pair)

            if len(new_set) == 0:
                print("No primer pair left for " + primer_set_q.name + ". Consider less restrictive BLAST settings.")
                sys.exit(1)

            print("\n")

            primer_sets[primer_set_q.index].set = new_set