import rdflib

grafo_DatiPiemonte = rdflib.Graph ()

grafo_DatiPiemonte.parse (file=open('scuole-piemonte.rdf'))

meccanografici = set()
for meccan in grafo_DatiPiemonte.objects(predicate=rdflib.URIRef('http://id-dati.piemonte.it/ontology/v1/rponto.owl#codMIURscuola')):
    meccanografici.add (str (meccan).upper ())

print len(meccanografici)
