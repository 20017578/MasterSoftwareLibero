Estrae tutte le amministrazioni presenti sul grafo SPCData, nell'esempio filtra per le amministrazioni che contengono la stringa "Albero"

```SPARQL
SELECT ?nome, ?x, ?h, ?add where {
  ?c a <http://spcdata.digitpa.gov.it/Amministrazione>.
  ?c <http://www.w3.org/2000/01/rdf-schema#label> ?nome. 
  ?c <http://www.w3.org/ns/org#identifier> ?x.
  ?c <http://xmlns.com/foaf/0.1/homepage> ?h.
  ?c <http://www.w3.org/ns/locn#address> ?add.
  FILTER ( regex(?nome, "Albero") ) 
}
```

Informazioni da inserire nei LOD:
vedere [dati.camera](http://dati.camera.it/it/download/atti-e-votazioni.html) per uniformare la descrizione dei riferimenti normativi
<dc:publisher>G.U. n. 145 del 25 Giugno 2003</dc:publisher>
<ocd:lex rdf:resource="http://www.normattiva.it..."/>
