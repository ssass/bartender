from __future__ import print_function
import ConfigParser
import StringIO
import re
from helpers.primer import Primer
from helpers.primerpair import PrimerPair


class P3Parser:

    @staticmethod
    def parse_p3_information(primer_pair_set, p3output):

        ini_str = '[root]\n' + p3output[:len(p3output) - 1]
        ini_fp = StringIO.StringIO(ini_str)
        content = ConfigParser.RawConfigParser()
        content.readfp(ini_fp)

        num_primers = content.getint('root', 'PRIMER_PAIR_NUM_RETURNED')
        if num_primers == 0:
            raise Exception("No primer found for " + primer_pair_set.name + ". Consider less restrictive Primer3 settings.")
        for i in range(num_primers):
            fwd = Primer(content.get('root', 'PRIMER_LEFT_' + str(i) + '_SEQUENCE'),
                         map(int, content.get('root', 'PRIMER_LEFT_' + str(i)).split(",")))
            fwd.gc_content = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_GC_PERCENT')
            fwd.tm = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_TM')
            fwd.any = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_SELF_ANY_TH')
            fwd.self = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_SELF_END_TH')

            rev = Primer(content.get('root', 'PRIMER_RIGHT_' + str(i) + '_SEQUENCE'),
                         map(int, content.get('root', 'PRIMER_RIGHT_' + str(i)).split(",")), True)
            rev.gc_content = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_GC_PERCENT')
            rev.tm = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_TM')
            rev.any = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_SELF_ANY_TH')
            rev.self = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_SELF_END_TH')

            pair = PrimerPair(fwd, rev, primer_pair_set.name + "_" + str(i))
            pair.product_size = content.getint('root', 'PRIMER_PAIR_' + str(i) + '_PRODUCT_SIZE')
            primer_pair_set.append(pair)

    @staticmethod
    def parse_p3seq_information(fwd_primer_set, rev_primer_set, p3output):

        ini_str = '[root]\n' + p3output[:len(p3output) - 1]
        ini_fp = StringIO.StringIO(ini_str)
        content = ConfigParser.RawConfigParser()
        content.readfp(ini_fp)

        warning = content.get('root', 'PRIMER_WARNING')

        for i in range(content.getint('root', 'PRIMER_LEFT_NUM_RETURNED')):

            fwd = Primer(content.get('root', 'PRIMER_LEFT_' + str(i) + '_SEQUENCE'),
                         map(int, content.get('root', 'PRIMER_LEFT_' + str(i)).split(",")))
            fwd.gc_content = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_GC_PERCENT')
            fwd.tm = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_TM')
            fwd.any = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_SELF_ANY_TH')
            fwd.self = content.getfloat('root', 'PRIMER_LEFT_' + str(i) + '_SELF_END_TH')
            fwd_primer_set.append(fwd)

        for i in range(content.getint('root', 'PRIMER_RIGHT_NUM_RETURNED')):

            rev = Primer(content.get('root', 'PRIMER_RIGHT_' + str(i) + '_SEQUENCE'),
                         map(int, content.get('root', 'PRIMER_RIGHT_' + str(i)).split(",")), True)
            rev.gc_content = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_GC_PERCENT')
            rev.tm = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_TM')
            rev.any = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_SELF_ANY_TH')
            rev.self = content.getfloat('root', 'PRIMER_RIGHT_' + str(i) + '_SELF_END_TH')
            rev_primer_set.append(rev)

        return warning