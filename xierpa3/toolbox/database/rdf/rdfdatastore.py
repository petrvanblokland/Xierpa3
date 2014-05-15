# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------

import rdflib

class RdfDatastore(object):

    def createStore(self):
        # Example.
        store = TripleStore()
        store.parse ( inputsource )
        rdf_subjects = store.subjects()
        store.predicates(subject="http://web.resource.org/cc/License")
