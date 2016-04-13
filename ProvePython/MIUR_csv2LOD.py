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
    csvDatiMIUR = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Leggo i dati', fonteDati, 'dal file', nomeFileDati
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

#
# Legge grafo AgID, per i comuni (per ora)
#

grafo_AgID = rdflib.Graph ()
nomeFileDati = 'AgID.ttl'
formatoDati = 'n3'
try:
    f = open (nomeFileDati)
    grafo_AgID.parse (file = f, format = formatoDati)
    print 'Ho inizializzato il grafo dal file', nomeFileDati
    f.close ()
except:
    print 'File', nomeFileDati, 'non trovato, eseguire PreparaSottoGrafoAgID.py'
    sys.exit (1)

geonames_In = rdflib.URIRef ('http://www.geonames.org/ontology#locatedIn')
comuniAgID = {}
for comune in grafo_AgID.subjects (predicate=rdflib.RDF.type, object=rdflib.URIRef ('http://spcdata.digitpa.gov.it/Comune')):
    nomeComune = grafo_AgID.value (comune, rdflib.RDFS.label).toPython ().upper ()
    if nomeComune in comuniAgID:
        print 'Ci sono due comuni di nome', nomeComune
        re = grafo_AgID.value (grafo_AgID.value (grafo_AgID.value (comuniAgID[nomeComune], geonames_In), geonames_In),rdflib.RDFS.label).toPython ()
        print nomeComune + ' (' + re + ')'
        comuniAgID[nomeComune + ' ('+ re +')'] = comuniAgID[nomeComune]
        del comuniAgID[nomeComune]
        re = grafo_AgID.value (grafo_AgID.value (grafo_AgID.value (comune, geonames_In), geonames_In),rdflib.RDFS.label).toPython ()
        print nomeComune + ' (' + re + ')'
        comuniAgID[nomeComune + ' ('+ re +')'] = comune
    else:
        comuniAgID[nomeComune] = comune

namespace_scuole = namespace_MIUR + 'Scuola/'
namespace_ontologia = namespace_MIUR + 'ontologia#'
prop_latitudine = rdflib.URIRef ('http://www.w3.org/2003/01/geo/wgs84_pos#lat')
prop_longitudine = rdflib.URIRef ('http://www.w3.org/2003/01/geo/wgs84_pos#long')

grafo_MIUR.bind ('scuola', namespace_scuole)

caratteristiche = set ()
tipiIstituzione = set ()
comuniNonTrovati = {}

locale.setlocale( locale.LC_ALL, 'it_IT.UTF-8')

aliasComuni = { 'AGLIANO' : 'AGLIANO TERME', 'BORGONE DI SUSA' : 'BORGONE SUSA', 'CERRINA' : 'CERRINA MONFERRATO', 'CAMPIGLIONE FENILE' : 'CAMPIGLIONE-FENILE', 'CASTELLETTO TICINO' : 'CASTELLETTO SOPRA TICINO', "LENTA'" : 'LENTA',  'MOTTA DEI CONTI' : "MOTTA DE' CONTI", "MOLINO DE' TORTI" : 'MOLINO DEI TORTI', 'LEINI' : "LEINI'", 'PONT CANAVESE' : 'PONT-CANAVESE',  "REGGIO NELL'EMILIA" : "REGGIO EMILIA", 'SAN REMO' : 'SANREMO',  'IESOLO' : 'JESOLO', 'RACCUIA':'RACCUJA', 'ORTONA A MARE' : 'ORTONA','CASSANO ALLO IONIO' :"CASSANO ALL'IONIO"}

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
    comune = None
    nomeComune = rigaScuola['COMUNE']
    nomeProvincia = rigaScuola['PROVINCIA']
    if nomeProvincia == "L' Aquila":
        nomeProvincia = "L'Aquila"
    nomeRegione = rigaScuola['REGIONE']
    if nomeComune in comuniAgID:
        comune = comuniAgID[nomeComune]
    elif (nomeComune + ' (' + nomeRegione + ')') in comuniAgID:
        comune = comuniAgID[nomeComune + ' (' + nomeRegione + ')']
    elif ('.' in nomeComune) and \
    (nomeComune[:nomeComune.find('.') - 1] in comuniAgID):
        comune = comuniAgID[nomeComune[:nomeComune.find('.') - 1]]
    elif nomeComune in aliasComuni and aliasComuni[nomeComune] in comuniAgID:
        comune = comuniAgID[aliasComuni[nomeComune]]
    if comune:
        grafo_MIUR.add ( (namespace_scuole + meccanografico, geonames_In, comune) )
        re = grafo_AgID.value (grafo_AgID.value (grafo_AgID.value (comune, geonames_In), geonames_In), rdflib.RDFS.label).toPython ()
        if re[:5] != nomeRegione[:5]:
            print 'Attenzione, per il comune', nomeComune, 'la regione non corrisponde:', re, '!=', nomeRegione
    else:
        if nomeRegione == 'Piemonte':
            print 'Comune', nomeComune, 'non trovato!!'
        nomeComune += ' (' + nomeRegione + ')'
        if nomeComune in comuniNonTrovati:
            comuniNonTrovati[nomeComune] += 1
        else:
            comuniNonTrovati[nomeComune] = 1

print 'Caratteristiche trovate:', caratteristiche
print 'Valori per TIPO ISTITUZIONE:', tipiIstituzione
print 'Comuni non trovati:', comuniNonTrovati

grafo_MIUR.serialize (destination=open ('MIUR.ttl', 'w'), format=formatoDati)
print 'Scritto un grafo con', len (grafo_MIUR), 'terne.'
