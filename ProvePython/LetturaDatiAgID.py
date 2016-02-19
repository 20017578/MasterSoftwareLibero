#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import requests
from rdflib import Graph

# Imposta il proxy, da mettere a 0 se si lavora da fuori dai computer della Regione
da_regione = 1

if da_regione == 1:
    proxies = {
        'http' : 'http://10.102.162.8:80',
        'https' : 'http://10.102.162.8:80',
    }
else:
    proxies = {}

dati_da_AgID = requests.get('http://spcdata.digitpa.gov.it/data/amm.nt', proxies=proxies)

grafo_AgID = Graph()
grafo_AgID.parse(data = dati_da_AgID.text , format="nt")

print len(grafo_AgID)

from rdflib.namespace import RDF
from rdflib import URIRef
URI_amministrazione = URIRef("http://spcdata.digitpa.gov.it/Amministrazione")
URI_pec = URIRef('http://spcdata.digitpa.gov.it/PEC')
URI_mail = URIRef('http://xmlns.com/foaf/0.1/mbox')

conto = 0
for amm in grafo_AgID.subjects(predicate=RDF.type, object=URI_amministrazione):
    scuola = ''
    conto += 1
    if conto % 1000 == 0:
        print conto
    # cerca se la PEC è nel dominio istruzione.it
    for pec in grafo_AgID.objects(amm,URI_pec):
        if str(pec).upper().find('ISTRUZIONE.IT') != -1:
            scuola = str(pec).split('@')[0]
    if scuola != '': # Cerca ancora solo se non trovata prima
        for mail in grafo_AgID.objects(amm,URI_mail):
            if str(mail).upper().find('ISTRUZIONE.IT') != -1:
                scuola = str(mail).split('@')[0]
    if scuola != '':
        print "%s presumibilmente è una scuola, con meccanografico %s"%(str(amm), scuola)

dati_da_AgID = ''
grafo_AgID = ''
