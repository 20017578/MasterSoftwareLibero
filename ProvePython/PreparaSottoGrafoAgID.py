#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import rdflib
import requests
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
URL_Dati = 'http://spcdata.digitpa.gov.it/data/ipa.ttl'
try:
    grafo_AgID.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da', fonteDati, ', termino.'
            sys.exit (1)
    grafo_AgID.parse (data=datiDaRete.text, format=formatoDati)
    grafo_AgID.serialize (destination=open (nomeFileDati, 'w'), format=formatoDati)
    print 'Dati salvati su', nomeFileDati, 'per usi futuri'
    datiDaRete = None  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

# print len (grafo_AgID)

nomeFileDati = 'DatiAgID.csv'
separatoreDati = '\t'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.csv'
try:
    letturaRighe = csv.reader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da AgID, termino.'
            sys.exit (1)
    f = open (nomeFileDati, 'w')
    f.write (datiDaRete.text)
    print 'Ho scritto i dati sul file', nomeFileDati
    f.close ()
    letturaRighe = csv.reader (open (nomeFileDati), delimiter = separatoreDati)
    datiDaRete = None  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

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

grafo_AgID_essenziale.serialize (destination=open ('AgID.ttl', 'w'), format='n3')
