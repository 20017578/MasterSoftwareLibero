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
select distinct ?iriComune ?labelComune where {
 ?iriComune <http://www.geonames.org/ontology#locatedIn> ?provincia.
 ?provincia <http://www.geonames.org/ontology#locatedIn> ?regione.
 ?regione a <http://spcdata.digitpa.gov.it/Regione>;
    <http://www.w3.org/2000/01/rdf-schema#label> 'Piemonte'.
 ?iriComune <http://www.w3.org/2000/01/rdf-schema#label> ?labelComune.
} LIMIT 100
```

La lista delle categorie di amministrazione

```SPARQL
select distinct ?x ?o
where {
  ?x a <http://spcdata.digitpa.gov.it/CategoriaAmministrazione>;
    <http://www.w3.org/2000/01/rdf-schema#label> ?o.
}
```

La categoria delle scuole sembrerebbe essere: http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L33 ma non sembra usata, probabilmente per la problematica (evidenziata nell'analisi)[DatiScuole.md#identificazione-scuole-su-dati-agid].

Richieste all'ISTAT
-------------------

La richiesta seguente all'[*end-point* SPARQL dell'ISTAT](http://datiopen.istat.it/sparql), permette di richiedere i comuni la cui popolazione supera le 700mila unità:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ter: <http://datiopen.istat.it/odi/ontologia/territorio/>
PREFIX cen: <http://datiopen.istat.it/odi/ontologia/censimento/>
SELECT ?c ?Comune ?Popolazione
WHERE
{
 ?c rdf:type ter:COM .
 ?c ter:haNome ?Comune .
 ?c ter:haIndicatoreCensimento ?o .
 ?o cen:haClassiEta16Categorie cen:ClasseEtaTotale16Cat .
 ?o cen:haStatoCivile cen:StatoCivile5CatTotale .
 ?o cen:haSesso <http://purl.org/linked-data/sdmx/2009/code#sex-T> .
 ?o cen:haPopolazioneResidente ?Popolazione .
 FILTER (?Popolazione > 700000)
} ORDER BY (?Popolazione)
```
