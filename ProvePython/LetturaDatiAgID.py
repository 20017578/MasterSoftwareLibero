#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import rdflib
import requests
import sys

#
# Lettura dei dati di AgID
# TODO: rendere questa porzione di codice una funzione!!
#

grafo_AgID = rdflib.Graph ()

fonteDati = 'AgID'
nomeFileDati = 'DatiAgID.ttl'
formatoDati = 'n3'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.ttl'
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

# print len (grafo_AgID)

#
# Qualche manipolazione sul grafo AgID
# TODO: Oltre a visualizzare qualche statistica, forse converrebbe creare un sotto-grafo con le sole scuole, per gli usi successivi
#

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
        if meccanograficoScuola != '':
            print "%s sembra una scuola, ma la pec %s non sembra indicare un meccanografico, cerco la e-mail"%(str(amministrazione), meccanograficoScuola)
        for mail in grafo_AgID.objects (amministrazione, URI_mail):
            if str (mail).upper ().find ('ISTRUZIONE.IT') != -1:
                meccanograficoScuola = str (mail).split ('@')[0]
    if meccanograficoScuola != '':
        if len(meccanograficoScuola) != 10:
            print "%s sembra una scuola, ma il codice %s non sembra un meccanografico"%(str(amministrazione), meccanograficoScuola)
        else:
            codiceCatastaleComune = '';
            for Comune in grafo_AgID.objects(amministrazione,URI_locatedIn):
                codiceCatastaleComune = str(Comune).split('/')[-1];
                if codiceCatastaleComune in listaScuolePerComune:
                    listaScuolePerComune[codiceCatastaleComune].append(meccanograficoScuola.upper ())
                else:
                    listaScuolePerComune[codiceCatastaleComune] = [meccanograficoScuola.upper ()]
            if codiceCatastaleComune == '':
                print "Non trovato il comune, stampo quel che so su questa amministrazione"
                for p,o in grafo_AgID.predicate_objects(amministrazione):
                    print str(p), str(o)
                    for lab in grafo_AgID.objects(o,URI_label):
                        print ':::: label', str(lab)

        listaMeccanograficiAgID.append (meccanograficoScuola.upper ())
        unaScuola = amministrazione

print 'Su ', conto, ' amministrazioni, ho trovato', len (listaMeccanograficiAgID), ' presunte scuole, distribuite su ', len (listaScuolePerComune), 'comuni'

sommaScuoleConComune = 0
numeroScuolePerComune = {}
for i in listaScuolePerComune:
    numeroScuolePerComune[i] = len(listaScuolePerComune[i])
    sommaScuoleConComune += numeroScuolePerComune[i]

print 'Trovate in tutto', sommaScuoleConComune, ' distribuit nei seguenti comuni:', listaScuolePerComune.keys()

print 'Lista delle ', numeroScuolePerComune['L219'], 'scuole trovate nel comune di Torino', listaScuolePerComune['L219']

grafo_AgID = ''
