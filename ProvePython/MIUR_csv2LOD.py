#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import rdflib
import sys
import csv

#
# Lettura dei dati da MIUR
# TODO: Rendere anche questa porzione una funzione!
#

fonteDati = 'MIUR'
nomeFileDati = 'DatiMIUR.csv'
separatoreDati = ';'
try:
    letturaRighe = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, lanciare ScaricaDatiDaRete.py'
    sys.exit (1)


# Prepara grafo MIUR

autonomie = {}
grafo_MIUR = rdflib.Graph ()

nomeFileDati = '../RDF/miur.ttl'
formatoDati = 'n3'
try:
    grafo_MIUR.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho inizializzato il grafo dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, impossibile inizializzare il grafo'
    sys.exit (1)

namespace_MIUR = None
for p, n in grafo_MIUR.namespaces ():
    if p == '':
        namespace_MIUR = n

if namespace_MIUR == None:
    print 'Non trovato un `namespace` di riferimento in', nomeFileDati, ', esco'
    raise ValueError('namespace non trovato')

namespace_scuole = namespace_MIUR + 'Scuola/'


