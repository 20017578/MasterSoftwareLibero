#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

from rdflib import Graph
import sys

grafo_AgID = Graph()

fonteDati = 'AgID'
nomeFileDati = 'DatiAgID.nt'
formatoDati ='nt'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.nt'
try:
    grafo_AgID.parse(file = nomeFileDati , format=formatoDati)
    print 'Ho letto i dati ', fonteDati, ' dal file ', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File ', nomeFileDati, ' non trovato, provo da rete'
    import requests
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get(URL_Dati)
        print 'Ho scaricato i dati ', fonteDati, ' da ', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy'
        proxies = {
            'http' : 'http://10.102.162.8:80',
            'https' : 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get(URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati ', fonteDati, ' da ', URL_Dati, ' usando il proxy'
        except:
            print "Impossibile scaricare i dati da AgID, termino."
            sys.exit(1)
    grafo_AgID.parse(data = datiDaRete.text , format=formatoDati)
    datiDaRete='' # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

print len(grafo_AgID)

from rdflib.namespace import RDF
from rdflib import URIRef

URI_amministrazione = URIRef("http://spcdata.digitpa.gov.it/Amministrazione")
URI_pec = URIRef('http://spcdata.digitpa.gov.it/PEC')
URI_mail = URIRef('http://xmlns.com/foaf/0.1/mbox')

lista = []
conto = 0
for amm in grafo_AgID.subjects(predicate=RDF.type, object=URI_amministrazione):
    scuola = ''
    conto += 1
    if conto % 1000 == 0:
        print 'Analizzate ', conto, ' amministrazioni, trovate ', len(lista), ' possibili scuole'
    # cerca se la PEC è nel dominio istruzione.it
    for pec in grafo_AgID.objects(amm,URI_pec):
        if str(pec).upper().find('ISTRUZIONE.IT') != -1:
            scuola = str(pec).split('@')[0]
    if scuola != '': # Cerca ancora solo se non trovata prima
        for mail in grafo_AgID.objects(amm,URI_mail):
            if str(mail).upper().find('ISTRUZIONE.IT') != -1:
                scuola = str(mail).split('@')[0]
    if scuola != '':
        # print "%s presumibilmente è una scuola, con meccanografico %s"%(str(amm), scuola)
        lista.append (scuola)

grafo_AgID = ''
