#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib
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
    csvDatiMIUR = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
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
namespace_ontologia = namespace_MIUR + 'ontologia#'

caratteristiche = set ()
tipiIstituzione = set ()

for rigaScuola in csvDatiMIUR:
    meccanografico = rigaScuola['PLESSO/SCUOLA'].upper ()
    grafo_MIUR.add ( (namespace_scuole + meccanografico, namespace_ontologia + 'meccanografico', rdflib.Literal (meccanografico)) )
    autonomia = rigaScuola['ISTITUTO PRINCIPALE'].upper ()
    if autonomia == meccanografico:
        if rigaScuola['DENOMINAZIONE'].upper () != rigaScuola['DENOMINAZIONE ISTITUTO PRINCIPALE'].upper ():
            print 'Anomalia sulla autonomia', meccanografico, 'denominazioni non coincidenti'
        grafo_MIUR.add ( (namespace_scuole + meccanografico, rdflib.RDF.type, namespace_ontologia + 'Autonomia') )
    else:
        grafo_MIUR.add ( (namespace_scuole + meccanografico, rdflib.RDF.type, namespace_ontologia + 'PuntoErogazioneServizio') )
        grafo_MIUR.add ( (namespace_scuole + meccanografico, namespace_ontologia + 'haIstitutoPrincipale', namespace_scuole + autonomia) )
    grafo_MIUR.add ( (namespace_scuole + meccanografico, rdflib.RDFS.label, rdflib.Literal (rigaScuola['DENOMINAZIONE'])) )
    caratteristiche |= {rigaScuola['CARATTERISTICA']}
    tipiIstituzione |= {rigaScuola['TIPO ISTITUZIONE']}

grafo_MIUR.serialize (destination=open ('MIUR.ttl', 'w'), format=formatoDati)
print 'Scritto un grafo con', len (grafo_MIUR), 'terne.'

print 'Caratteristiche trovate:', caratteristiche
print 'Valori per TIPO ISTITUZIONE:', tipiIstituzione
