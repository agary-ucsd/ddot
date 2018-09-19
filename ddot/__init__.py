from __future__ import absolute_import

from ddot.config import *
from ddot.Ontology import *
from ddot.utils import *
import subprocess

def generate_clixo_file(graph, alpha, beta):
    clixo_cmd = '/Users/aarongary/Development/Projects/ddot/ddot/mhk7-clixo_0.3-cec3674/clixo'

    path_this = os.path.dirname(os.path.abspath(__file__))
    #graph = os.path.join(path_this, '3col_interactions260.csv')
    output_file = os.path.join(path_this, 'stdout.txt')

    if not isinstance(alpha, str):
        alpha = str(alpha)

    if not isinstance(beta, str):
        beta = str(beta)

    #cmd = ("""{0} {1} {2} {3} """.format(clixo_cmd, graph, alpha, beta) +
    #       """ | tee {}""".format(output_log))

    #print('CLIXO command:', cmd)

    # os.system(cmd)

    #with open(output_file, 'w') as outfile:
    with tempfile.NamedTemporaryFile('w', delete=False) as outfile:

        subprocess.call([clixo_cmd, graph, alpha, beta], stdout=outfile)

        return outfile.name

    return None
