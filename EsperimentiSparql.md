Esperimenti SPARQL
==================
Definizioni
-----------
[SPARQL Protocol and RDF Query Language](https://it.wikipedia.org/wiki/SPARQL)

Richieste alla AgID
-------------------
l'AgID espone un endpoint: http://spcdata.digitpa.gov.it:8899/sparql

Su quel sevizio, per avere la lista dei comuni del Piemonte (limitata a 100 risultati)

```SPARQL
select distinct ?c ?n where {
?c <http://www.geonames.org/ontology#locatedIn> ?p.
?p <http://www.geonames.org/ontology#locatedIn> <http://spcdata.digitpa.gov.it/Regione/1>.
?c <http://www.w3.org/2000/01/rdf-schema#label> ?n.
} LIMIT 100
```

La lista delle categorie di amministrazione

```SPARQL
select distinct ?x ?o where {?x a
<http://spcdata.digitpa.gov.it/CategoriaAmministrazione>. ?x
<http://www.w3.org/2000/01/rdf-schema#label> ?o.}
```

La categoria delle scuole sembrerebbe essere: http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L33 ma non sembra usata...
