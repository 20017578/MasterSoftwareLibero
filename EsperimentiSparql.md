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

La richiesta seguente all'[*end-point* SPARQL dell'ISTAT](http://datiopen.istat.it/sparql), permette di richiedere i comuni la cui popolazione supera le 700mila unitÃ :

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

LinkedGeoData
-------------

Un esperimento, tanto per gioco, anche su http://linkedgeodata.org/sparql :

```SPARQL
PREFIX lgdr:<http://linkedgeodata.org/triplify/>
PREFIX lgdo:<http://linkedgeodata.org/ontology/>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nome ?lat ?lon {
 ?s a lgdo:School;
  geo:lat ?lat;
  geo:long ?lon;
  rdfs:label ?nome.
 FILTER (?lat > 44 AND ?lat < 46.5 AND ?lon > 6.6 AND ?lon < 9.3)
}
```

Un tentativo di estrarre "aree":

```SPARQL
PREFIX lgdr:<http://linkedgeodata.org/triplify/>
PREFIX lgdo:<http://linkedgeodata.org/ontology/>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT distinct ?nodo ?nome ?WKT {
 ?nodo a lgdo:School;
    <http://geovocab.org/geometry#geometry> ?o;
  rdfs:label ?nome.
 ?o <http://www.opengis.net/ont/geosparql#asWKT> ?WKT;
    <http://linkedgeodata.org/ontology/posSeq> ?s.
 ?s [] ?n.
 ?p <http://geovocab.org/geometry#geometry> ?n;
    geo:lat ?lat;
    geo:long ?lon.
 FILTER (?lat > 44 AND ?lat < 46.5 AND ?lon > 6.6 AND ?lon < 9.3)
}
```

Si tenga conto che http://www.opengis.net/ont/geosparql#asWKT è in stato **deprecated**, inoltre la richiesta qui sopra trova la geometria solo se uno dei suoi punti è anche geometria *a sé*, con latitudine e longitudine esplicitati e non *nascosti* nel WKT&hellip; Questo certamente non è il modo più efficiente di estrarre geometrie da [OSM](http://www.openstreetmap.org/)&hellip;

La lista dei comuni(?) della città metropolitana di Torino

```SPARQL
Prefix lgdr:<http://linkedgeodata.org/triplify/>
Prefix lgdo:<http://linkedgeodata.org/ontology/>
Prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>
Select * {
 ?s lgdo:isIn "Torino, Piemonte, Italy";
    rdfs:label ?l .
} Limit 1000
```
