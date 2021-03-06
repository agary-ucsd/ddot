from __future__ import absolute_import

import os, inspect, io
import json

from ndex.networkn import NdexGraph

import ddot

###########################################
# Default NDEx server, username, password #
###########################################

ndex_server = 'http://test.ndexbio.org'
ndex_user, ndex_pass = 'scratch', 'scratch'

#########################
# Read CX Visual styles #
#########################

passthrough_style = None

def get_passthrough_style():
    global passthrough_style
    if passthrough_style is None:
        top_level = os.path.dirname(os.path.abspath(inspect.getfile(ddot)))
        with io.open(os.path.join(top_level, 'passthrough_style.cx')) as f:
            passthrough_style = NdexGraph(json.load(f))
    return passthrough_style        

##################################
# NDEx URLs for example networks #
##################################

HUMAN_GENE_SIMILARITIES_URL = 'http://dev2.ndexbio.org/v2/d2dfa5cc-56de-11e7-a2e2-0660b7976219'
GO_HUMAN_URL = 'http://dev2.ndexbio.org/v2/network/328639dc-6044-11e8-9d1c-0660b7976219'
PHAROS_URL = 'http://dev2.ndexbio.org/v2/network/a94f1c0f-789a-11e7-a1d1-0660b7976219'
MONARCH_DISEASE_GENE_URL = 'http://dev2.ndexbio.org/v2/network/3772cf51-5c75-11e8-9d1c-0660b7976219'
MONARCH_DISEASE_GENE_SLIM_URL = 'http://dev2.ndexbio.org/v2/network/9a890eed-5c81-11e8-9d1c-0660b7976219'
