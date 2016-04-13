#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib
#

import rdflib
import sys
import csv
import locale

#
# Lettura dei dati da MIUR
#

fonteDati = 'MIUR'
nomeFileDati = 'DatiMIUR.csv'
separatoreDati = ';'
try:
    f = open (nomeFileDati)
    csvDatiMIUR = csv.DictReader (f, delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
    f.close ()
except:
    print 'File', nomeFileDati, 'non trovato, lanciare ScaricaDatiDaRete.py'
    sys.exit (1)

#
# Prepara grafo MIUR
#

autonomie = {}
grafo_MIUR = rdflib.Graph ()

nomeFileDati = '../RDF/miur.ttl'
formatoDati = 'n3'
try:
    f = open (nomeFileDati)
    grafo_MIUR.parse (file = f, format = formatoDati)
    print 'Ho inizializzato il grafo dal file', nomeFileDati
    f.close ()
except:
    print 'File', nomeFileDati, 'non trovato, impossibile inizializzare il grafo'
    sys.exit (1)

namespace_MIUR = None
for abbrev, ns in grafo_MIUR.namespaces ():
    if abbrev == '':
        namespace_MIUR = ns

if namespace_MIUR == None:
    print 'Non trovato un `namespace` di riferimento in', nomeFileDati, ', esco'
    raise ValueError('namespace non trovato')

namespace_scuole = namespace_MIUR + 'Scuola/'
namespace_ontologia = namespace_MIUR + 'ontologia#'
prop_latitudine = rdflib.URIRef ('http://www.w3.org/2003/01/geo/wgs84_pos#lat')
prop_longitudine = rdflib.URIRef ('http://www.w3.org/2003/01/geo/wgs84_pos#long')

grafo_MIUR.bind ('scuola', namespace_scuole)

caratteristiche = set ()
tipiIstituzione = set ()

locale.setlocale( locale.LC_ALL, 'it_IT.UTF-8')

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
    try:
        lat = locale.atof (rigaScuola['LATITUDINE'])
        lon = locale.atof (rigaScuola['LONGITUDINE'])
        if lat*lon != 0:
            grafo_MIUR.add ( (namespace_scuole + meccanografico, prop_latitudine, rdflib.Literal (lat)) )
            grafo_MIUR.add ( (namespace_scuole + meccanografico, prop_longitudine, rdflib.Literal (lon)) )
    except:
        lat = 0

grafo_MIUR.serialize (destination=open ('MIUR.ttl', 'w'), format=formatoDati)
print 'Scritto un grafo con', len (grafo_MIUR), 'terne.'

print 'Caratteristiche trovate:', caratteristiche
print 'Valori per TIPO ISTITUZIONE:', tipiIstituzione
