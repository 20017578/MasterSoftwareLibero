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



contoMIUR = 0
valoriTrovati = []
istitutiTrovati = set ()

if voceDaConteggiare in letturaRighe.fieldnames:
    for riga in letturaRighe:
        contoMIUR += 1
        if riga[voceDaConteggiare] in catalogoMeccanograficiMIUR:
            catalogoMeccanograficiMIUR[riga[voceDaConteggiare]] += 1
        else:
            catalogoMeccanograficiMIUR[riga[voceDaConteggiare]] = 1
        if voceDaSalvare in letturaRighe.fieldnames and voceDaFiltrare in letturaRighe.fieldnames:
            if riga[voceDaFiltrare] == valoreDaCercare:
                valoriTrovati.append (riga[voceDaSalvare])
                istitutiTrovati.add (riga[voceDaConteggiare])
else:
    print 'La voce', voceDaConteggiare, 'non si trova...'

print 'Su', contoMIUR, 'scuole, ho trovato', len (catalogoMeccanograficiMIUR), 'istituzoni'
print 'Per', voceDaFiltrare, 'pari a', valoreDaCercare, 'ho trovato i seguenti', len (valoriTrovati), 'valori per', voceDaSalvare, ':', valoriTrovati

grafo_MIUR = rdflib.Graph ()

nomeFileDati = '../RDF/miur.ttl'
formatoDati = 'n3'
try:
    grafo_MIUR.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho inizializzato il grafo dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, impossibile inizializzare il grafo'
    sys.exit (1)




