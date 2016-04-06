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

oppure

```SPARQL
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?iriComune ?labelComune where {
 ?iriComune gn:locatedIn [ gn:locatedIn [ a <http://spcdata.digitpa.gov.it/Regione>; rdfs:label 'Piemonte']] ;
    rdfs:label ?labelComune.
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
SELECT *
WHERE
{
 ?c rdf:type ter:COM ;
    ter:haNome ?Comune ;
    ter:haIndicatoreCensimento [
    cen:haClassiEta16Categorie cen:ClasseEtaTotale16Cat ;
    cen:haStatoCivile cen:StatoCivile5CatTotale ;
    cen:haSesso <http://purl.org/linked-data/sdmx/2009/code#sex-T> ;
    cen:haPopolazioneResidente ?Popolazione ].
 FILTER (?Popolazione > 700000)
} ORDER BY (?Popolazione)
```

Lista dei comuni, con codici ISTAT, catastale ed altro, se disponibile (non si vede ragione per cui ter:haNome e rdfs:label non debbano coincidere, ma tanto vale prelevarli entrambi).

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ter: <http://datiopen.istat.it/odi/ontologia/territorio/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT  *
WHERE {
?iri rdf:type ter:COM.
  OPTIONAL {
  ?iri ter:haCodCatastale ?catastale;
     ter:haCodIstat ?istat;
     rdfs:label ?nome;
     ter:haNome ?Toponimo ;
     ter:provincia_di_COM ?Prov;
     ter:regione_di_COM ?Reg ;
     owl:sameAs ?altriLOD .
  }
}
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
PREFIX geov:<http://geovocab.org/geometry#>
PREFIX lgdo:<http://linkedgeodata.org/ontology/>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT distinct ?nodo ?nome ?WKT {
 ?nodo a lgdo:School; rdfs:label ?nome;
   geov:geometry [
     <http://www.opengis.net/ont/geosparql#asWKT> ?WKT;
     lgdo:posSeq [ [] [ ^geov:geometry [
       geo:lat ?lat;
       geo:long ?lon
     ]]]
   ].
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
