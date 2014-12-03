__author__ = 'Steffen'

class PrimerSetFormatter:

    @staticmethod
    def format_primer_set(arrangements, primer_sets):
        s = '<h4>Rank 1: Sum MFE=-' + str(arrangements[0][0]) + '</h4>'\
            + '<br>\n<div class="panel-group" id="p3selectResults" role="tablist" aria-multiselectable="true">\n'

        v = arrangements[0][1]
        for j, pset in enumerate(primer_sets):
                pair = pset.set[v[j]]
                s += PrimerSetFormatter.format_primer_pair(pair, pset.name)

        s += '</div>\n'
        return s

    @staticmethod
    def format_primer_pair(primer_pair, name):
        s = '<div class="panel panel-default">\n'\
            + '<div class="panel-heading" role="tab" id="heading' + name + '">\n'\
            + '<h4 class="panel-title">\n'\
            + '<a class="collapsed" data-toggle="collapse" data-parent="#tablist" href="#collapse' + name + '" aria-expanded="false" aria-controls="collapse' + name +'">\n'\
            + name + ": " + primer_pair.fwd.sequence.upper() + " - " + primer_pair.rev.sequence.upper() + '&emsp;Product Size: ' + str(primer_pair.product_size)\
            + '\n</a>\n'\
            + '</h4>\n'\
            + '</div>\n'\
            + '<div id="collapse' + name +'" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading' + name +'">\n'\
            + '<div class="panel-body">\n'\
            + 'Forward: ' + primer_pair.fwd.sequence.upper() + '<br>\n' \
            + '<table style="width:100%"><tr>' \
            + '<td>Position: ' + str(primer_pair.fwd.position[0]) + " - " + str(primer_pair.fwd.position[0] + primer_pair.fwd.position[1]) +'</td>'\
            + '<td>BLAST hits: ' + str(primer_pair.fwd.blast_hits) + '</td>\n'\
            + '<td>Length: ' + str(len(primer_pair.fwd)) + '</td>\n'\
            + '<td>Tm: ' + str(primer_pair.fwd.tm) + '</td>\n'\
            + '<td>GC%: ' + str(primer_pair.fwd.gc_content) + '</td>' \
            + '<td>Any: ' + str(primer_pair.fwd.any) + '</td>' \
            + '<td>Self: ' + str(primer_pair.fwd.self) + '</td></tr></table><br>\n'\
            + 'Reverse: ' + primer_pair.rev.sequence.upper() +'<br>\n'\
            + '<table style="width:100%"><tr>' \
            + '<td>Position: ' + str(primer_pair.rev.position[0]) + " - " + str(primer_pair.rev.position[0] + primer_pair.rev.position[1]) +'</td>'\
            + '<td>BLAST hits: ' + str(primer_pair.rev.blast_hits) + '</td>\n'\
            + '<td>Length: ' + str(len(primer_pair.rev)) + '</td>\n'\
            + '<td>Tm: ' + str(primer_pair.rev.tm) + '</td>\n'\
            + '<td>GC%: ' + str(primer_pair.rev.gc_content) + '</td>' \
            + '<td>Any: ' + str(primer_pair.rev.any) + '</td>' \
            + '<td>Self: ' + str(primer_pair.rev.self) + '</td></tr></table><br>\n'\
            + '\n</div>\n'\
            + '</div>\n'\
            + '</div>\n'
        return s