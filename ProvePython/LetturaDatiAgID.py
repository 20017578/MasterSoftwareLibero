#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import rdflib
import requests
import sys

grafo_AgID = rdflib.Graph ()

fonteDati = 'AgID'
nomeFileDati = 'DatiAgID.nt'
formatoDati = 'nt'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.nt'
try:
    grafo_AgID.parse (file=open(nomeFileDati), format=formatoDati)
    print 'Ho letto i dati ', fonteDati, ' dal file ', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File ', nomeFileDati, ' non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati ', fonteDati, ' da ', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati ', fonteDati, ' da ', URL_Dati, ' usando il proxy'
        except:
            print "Impossibile scaricare i dati da AgID, termino."
            sys.exit (1)
    grafo_AgID.parse (data=datiDaRete.text, format=formatoDati)
    datiDaRete = ''  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

print len (grafo_AgID)

URI_amministrazione = rdflib.URIRef ("http://spcdata.digitpa.gov.it/Amministrazione")
URI_pec = rdflib.URIRef ('http://spcdata.digitpa.gov.it/PEC')
URI_mail = rdflib.URIRef ('http://xmlns.com/foaf/0.1/mbox')
URI_locatedIn = rdflib.URIRef ('http://www.geonames.org/ontology#locatedIn')
URI_label = rdflib.URIRef ('http://www.w3.org/2000/01/rdf-schema#label')

listaMeccanograficiAgID = []
listaScuolePerComune = {}
conto = 0
for amministrazione in grafo_AgID.subjects (predicate=rdflib.RDF.type, object=URI_amministrazione):
    meccanograficoScuola = ''
    conto += 1
    if conto % 1000 == 0:
        print 'Analizzate ', conto, ' amministrazioni, trovate ', len (listaMeccanograficiAgID), ' possibili scuole'
    # cerca se la PEC ha dominio istruzione.it
    for pec in grafo_AgID.objects (amministrazione, URI_pec):
        if str (pec).upper ().find ('ISTRUZIONE.IT') != -1:
            meccanograficoScuola = str (pec).split ('@')[0]
    if len(meccanograficoScuola) != 10:  # Cerca ancora solo se non trovata prima
        for mail in grafo_AgID.objects (amministrazione, URI_mail):
            if str (mail).upper ().find ('ISTRUZIONE.IT') != -1:
                meccanograficoScuola = str (mail).split ('@')[0]
    if meccanograficoScuola != '':
        if len(meccanograficoScuola) != 10:
            print "%s sembra una scuola, ma il codice %s non sembra un meccanografico"%(str(amministrazione), meccanograficoScuola)
        else:
            for Comune in grafo_AgID.objects(amministrazione,URI_locatedIn):
                codiceCatastaleComune = str(Comune).split('/')[-1];
                if codiceCatastaleComune in listaScuolePerComune:
                    listaScuolePerComune[codiceCatastaleComune].append(meccanograficoScuola.upper ())
                else:
                    listaScuolePerComune[codiceCatastaleComune] = [meccanograficoScuola.upper ()]
        listaMeccanograficiAgID.append (meccanograficoScuola.upper ())

print 'Su ', conto, ' amministrazioni, ho trovato', len (listaMeccanograficiAgID), ' presunte scuole, distribuite su ', len (listaScuolePerComune), 'comuni'

print "Stampo quello che so sull'ultima scuola trovata."

for p,o in grafo_AgID.predicate_objects(unaScuola):
    print str(p), str(o)
    for lab in grafo_AgID.objects(o,URI_label):
        print ':::: label', str(lab)

print 'Lista dei comuni', listaScuolePerComune.keys()

print 'Lista delle ', len(listaScuolePerComune['L219']), 'scuole trovate nel comune di Torino', listaScuolePerComune['L219']

grafo_AgID = ''
