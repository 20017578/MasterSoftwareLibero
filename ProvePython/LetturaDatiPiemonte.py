
import rdflib

grafo_DatiPiemonte = rdflib.Graph ()

fonteDati = 'dati.piemonte'
nomeFileDati = 'DatiPiemonte.ttl'
formatoDati = 'n3'
URL_Dati = 'http://id-dati.piemonte.it/resource/scuole/scuole-piemonte.rdf'
try:
    grafo_DatiPiemonte.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho letto i dati ', fonteDati, ' dal file ', nomeFileDati
except:
    print 'File ', nomeFileDati, ' non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        grafo_DatiPiemonte.parse (URL_Dati)
        print 'Ho scaricato i dati ', fonteDati, ' da ', URL_Dati
    except:
        print 'Impossibile scaricare i dati da', fonteDati, ', termino.'
        sys.exit (1)
    grafo_DatiPiemonte.serialize (destination=open (nomeFileDati, 'w'), format=formatoDati)
    print 'Dati salvati su', nomeFileDati, 'per usi futuri'

meccanografici = set()
for meccan in grafo_DatiPiemonte.objects(predicate=rdflib.URIRef('http://id-dati.piemonte.it/ontology/v1/rponto.owl#codMIURscuola')):
    meccanografici.add (str (meccan).upper ())

print len(meccanografici)
