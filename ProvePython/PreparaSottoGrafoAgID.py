#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib
#

import rdflib
import sys
import csv

#
# Lettura dei dati di AgID
# TODO: rendere questa porzione di codice una funzione!!
#

grafo_AgID = rdflib.Graph ()

fonteDati = 'AgID'
nomeFileDati = 'DatiAgID_completi.ttl'
formatoDati = 'n3'
try:
    grafo_AgID.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, lanciare ScaricaDatiDaRete.py'
    sys.exit (1)

# print len (grafo_AgID)

nomeFileDati = 'DatiAgID.csv'
separatoreDati = '\t'
try:
    letturaRighe = csv.reader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, lanciare ScaricaDatiDaRete.py'
    sys.exit (1)

# Legge dal CSV quali sono le scuole ed aggiunge la tripla corretta al grafo
spcdata_catAmm = rdflib.Namespace('http://spcdata.digitpa.gov.it/Categoriaamministrazione/')
IRI_scuola = spcdata_catAmm.L33
IRI_orgClassif = rdflib.URIRef ('http://www.w3.org/ns/org#classification')
pref_amministrazione = 'http://spcdata.digitpa.gov.it/Amministrazione/'

contoScuole = 0
for riga in letturaRighe:
    if riga [11] == 'Istituti di Istruzione Statale di Ogni Ordine e Grado':
        if not grafo_AgID.value (rdflib.URIRef (pref_amministrazione + riga[0]),  IRI_orgClassif):
            grafo_AgID.set ( (rdflib.URIRef (pref_amministrazione + riga[0]), IRI_orgClassif, IRI_scuola) )
            contoScuole += 1
        else:
            print 'Questa scuola ha una categoria associata, non aggiungo altro'

comuni = set (grafo_AgID.subjects (predicate=rdflib.RDF.type, object=rdflib.URIRef ('http://spcdata.digitpa.gov.it/Comune')))
scuole = set (grafo_AgID.subjects (predicate=IRI_orgClassif, object=IRI_scuola))

grafo_AgID_essenziale = rdflib.Graph ()

for p, n in grafo_AgID.namespaces ():
    grafo_AgID_essenziale.bind (p, n)

daAggiungere = comuni | scuole
aggiunti = set ()
while len (daAggiungere) != 0:
    dato = daAggiungere.pop ()
    aggiunti.add (dato)
    for p, o in grafo_AgID.predicate_objects (dato):
        grafo_AgID_essenziale.add ( (dato, p, o) )
        if p not in aggiunti:
            daAggiungere.add (p)
        if type (o) == type (p) and o not in aggiunti:
            daAggiungere.add (o)

aggiunti.clear ()
del grafo_AgID

namespace_attenzione = rdflib.Namespace('http://www.example.org/MIUR/Attenzione/')
IRI_pec = rdflib.URIRef ('http://spcdata.digitpa.gov.it/PEC')
IRI_mail = rdflib.namespace.FOAF.mbox
grafo_AgID_essenziale.bind ('warn', namespace_attenzione)
nomeFileDati = 'AgID-MIUR.csv'
scritturaRighe = csv.writer (open (nomeFileDati, 'w'), delimiter = separatoreDati)

for amministrazione in scuole:
    if str(amministrazione)[-16:-10].upper () == 'ISTSC_':
        meccanograficoScuola = str(amministrazione)[-10:].upper ()
    else:
        meccanograficoScuola = ''
    for mail in grafo_AgID_essenziale.objects (amministrazione, IRI_pec):
         if (str (mail)[-18:].upper () == '@PEC.ISTRUZIONE.IT'):
             if len (meccanograficoScuola) != 10:
                 meccanograficoScuola = str (mail)[:-18].upper ()
                 if len (meccanograficoScuola) != 10:
                     grafo_AgID_essenziale.add ( (amministrazione, namespace_attenzione.PEC, mail) )
             else:
                 if str (mail)[:-18].upper () != meccanograficoScuola:
                     grafo_AgID_essenziale.add ( (amministrazione, namespace_attenzione.PEC, mail) )
    for mail in grafo_AgID_essenziale.objects (amministrazione, IRI_mail):
         if (str (mail)[-14:].upper () == '@ISTRUZIONE.IT'):
             if len (meccanograficoScuola) != 10:
                 meccanograficoScuola = str (mail)[:-14].upper ()
                 if len (meccanograficoScuola) != 10:
                     grafo_AgID_essenziale.add ( (amministrazione, namespace_attenzione.mbox, mail) )
             else:
                 if str (mail)[:-14].upper () != meccanograficoScuola:
                     grafo_AgID_essenziale.add ( (amministrazione, namespace_attenzione.mbox, mail) )
    if len (meccanograficoScuola) == 10:
         scritturaRighe.writerow([str (amministrazione), meccanograficoScuola] )

grafo_AgID_essenziale.serialize (destination=open ('AgID.ttl', 'w'), format='n3')
