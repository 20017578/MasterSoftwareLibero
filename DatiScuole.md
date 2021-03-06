Analisi sui dati esistenti che riguardano le scuole
===================================================
Obiettivi dell'analisi
----------------------
 * Consistenza dei dati esistenti, per capire quali dati sono già pubblici e quali potrebbero essere aggiunti
 * Riconoscere i tipi di informazioni ed eventualmente arricchirle con migliori classificazioni
 * Verificare incoerenze tra i dati pubblicati, eventualmente per segnalare gli errori rilevati

Verifiche sui dati esistenti
----------------------------

### I dati RDF del [Sistema Pubblico di Connettività](http://spcdata.digitpa.gov.it/data.html)
L'*Indice della Pubblica Amministrazione* Contiene dati su tutte le amministrazioni, quindi anche sulle scuole.

Tipo di informazioni che possono essere reperite da questo insieme di dati:

 * denominazione;
 * Nome e Cognome di chi dirige l'istituzione;
 * indirizzo postale;
 * sito web istituzionale;
 * indirizzi elettronici istituzionali (in particolare PEC, ma anche e-mail e *social network*).

Licenza, secondo la pagina [note legali](http://spcdata.digitpa.gov.it/notelegali.html): CC BY-SA 3.0

Punti di forza:

 * Tutte le amministrazioni devono registrarsi sull'IPA, quindi qui si dovrebbero trovare tutte le scuole *statali*.

Punti di debolezza:

 * Al momento della consultazione, **15 marzo 2016**, risulta come data di ultimo aggiornamento il **25 maggio 2015**, quindi i dati sono vecchi di più di nove mesi; con l'aggravante, per il mondo scolastico, che all'inizio di settembre ha effetto il *dimensionamento* delle scuole, che può sopprimere/fondere/creare istituzioni scolastiche; anche le scuole non *dimensionate* possono comunque cambiare dirigente.
 * Non contiene dati sulle scuole non statali.
 * Contiene dati sulle *istituzioni*, quindi sulle sedi amministrative, collegati alle quali possiamo avere molti diversi *punti di erogazione* del servizio scolastico, distribuito su diversi edifici (anche diversi comuni) e diverse tipologie (anche ordine) di insegnamento.

Comandi per scaricare la base dati in formato csv e prime verifiche. Da shell:

```shell
$ curl "http://spcdata.digitpa.gov.it/data/amm.csv" | tee amm.csv |
  grep $'\tIstituti di Istruzione Statale di Ogni Ordine e Grado\t' |
  tee spcdata_digitpa_amm.csv | wc -l
9017
$ grep $'\tPiemonte\t' spcdata_digitpa_amm.csv| wc -l
602
```

Oltre a scaricare i dati (nel file spcdata_digitpa_amm.csv), i comandi suggeriti filtrano a priori gli istituti di *Istruzione Statale* e li contano. I valori di 9017 in tutta Italia e di 602 nel solo Piemonte, sembrano in realtà leggermente eccessivi.

 * Nota, il file csv **non contiene** una riga di intestazioni.

#### Identificazione scuole su dati AgID

Ci sono alcune una incongruenze tra i dati pubblicati dall'AgID in formato CSV ([http://spcdata.digitpa.gov.it/data/amm.csv](http://spcdata.digitpa.gov.it/data/amm.csv)) e quelli pubblicati nei formati per LinkedOpenData come ad esempio Turtle ([http://spcdata.digitpa.gov.it/data/amm.ttl](http://spcdata.digitpa.gov.it/data/amm.ttl)).

Tali incongruenze sembrano dovute a piccoli errori di riconoscimento, dovuti a errate digitazioni o troncamenti, con l'*aggravante*, per i dati sulle scuole, di presentare anche un errore sistematico per troncamento.

Nei file CSV, per tutte le scuole risulta presente, nella dodicesima colonna, (descritta nei [metadati](http://spcdata.digitpa.gov.it/data/Metadati_Open_Data.pdf) come `tipologia_istat`) la dicitura filtrata nell'esempio precedente: `Istituti di Istruzione Statale di Ogni Ordine e Grado`; tuttavia nei file Turtle tale dato non compare.

Vediamo come esempio il comune di Torino:

```shell
$ grep c_l219 amm.csv
c_l219	Comune di Torino	Torino	Piero Franco Rodolfo	Fassino	10122	TO	Piemonte	www.comune.torino.it	Piazza Palazzo Di Citta' 1	Sindaco	Comuni e loro Consorzi e Associazioni	Pubbliche Amministrazioni		S	00514490010	protocollogenerale@cert.comune.torino.it	pec	null	null	null	null	null	null	null	null	https://www.facebook.com/cittaditorino	https://twitter.com/twitorino		http://www.youtube.com/youtorino0
$ grep c_l219 amm.csv|cut -f12
Comuni e loro Consorzi e Associazioni
```

La dodicesima colonna contiene `Comuni e loro Consorzi e Associazioni`, nel file Turtle, tra le triple con *soggetto* il comune, troviamo `org:classification <http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L6>`. Ci aspetteremo dunque, per le scuole, di trovare `org:classification <http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L33>`.

Il problema probabilmente deriva da un banale troncamento. La categoria [L33](http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L33) ha come `label` la dicitura `Istituti di Istruzione Statale di Ogni Ordine e Grad`, senza la **`o`** finale!

Problema probabilmente analogo si presenta per alcune scuole con l'indicazione del comune di appartenenza. Per la maggioranza assoluta delle scuole trovate nei dati dell'AgID, è presente la tripla `<...scuola...> geonames:locatedIn <http://spcdata.digitpa.gov.it/Comune/...>`. Laddove manca, il nome del comune è comunque indicato nel file CSV, ma potrebbe esservi stata qualche incongruenza nella scrittura esatta&hellip;

### Il portale [Scuola in Chiaro](http://cercalatuascuola.istruzione.it/cercalatuascuola/opendata/)
Contiene dati specifici sulle scuole, pubblicati direttamente dal MIUR.

Tipo di informazioni che possono essere reperite da questo insieme di dati:

 * denominazione;
 * indirizzo postale;
 * collegamento tra istituti;
 * coordinate geografiche;
 * dati su alunni, classi, esiti, personale...

Licenza, non specificata esplicitamente sulla pagina, che riporta semplicemente: "I dati scaricabili da questo sito possono essere utilizzati per ogni scopo".

Punti di forza:

 * I dati sono estratti direttamente dal sistema informativo del MIUR, alimentato ed utilizzato dal ministero e dalle stesse istituzioni scolastiche
 * Contiene anche alcuni dati sulle scuole non statali

Punti di debolezza:

 * mancanza di uniformità tra i dati riguardanti le scuole statali e quelle non statali, che hanno obblighi ed interessi diversi nell'alimentare il sistema informativo del MIUR
 * l'informazione riguardante la "provincia", oltre a non tener conto delle nuove "città metropolitane" risulta spesso errato
 * dati geografici piuttosto approssimativi

Comandi per scaricare la base dati in formato csv e prime verifiche. Da shell:

```shell
$ curl "http://www.istruzione.it/scuolainchiaro_dati/7-Anagrafe_Scuole_Statali_201516.csv" | tee cercalatuascuola_istruzione_ASS_201516.csv | wc -l
51554
$ grep -E "^Piemonte" cercalatuascuola_istruzione_ASS_201516.csv | wc -l
3850
$ curl "http://www.istruzione.it/scuolainchiaro_dati/8-Anagrafe_Scuole_Paritarie_201516.csv" | tee tee cercalatuascuola_istruzione_ASP_201516.csv | wc -l
13669
$ grep -E "^Piemonte" -a cercalatuascuola_istruzione_ASP_201516.csv | wc -l
793
```

Oltre a scaricare i dati (nel file cercalatuascuola_istruzione_ASS_201516.csv), i comandi suggeriti li contano. I valori sono superiori a quelli visti per l'IPA, ma si riferiscono a tutte le scuole, non solo alle sedi amministrative.

 * Nota, il file csv **contiene** una riga di intestazioni.

Il file CSV coi [dati principali sulle scuole statali del MIUR](http://www.istruzione.it/scuolainchiaro_dati/7-Anagrafe_Scuole_Statali_201516.csv) contiene le seguenti colonne, che possono essere riferite a diverse ontologie:

Intestazione colonna|possibile predicato
--------------------|-------------------
REGIONE|<http://www.geonames.org/ontology#locatedIn> come AgID?
PROVINCIA|**Spesso questo valore risulta errato, meglio saltarlo?**
PLESSO/SCUOLA|<http://id-dati.piemonte.it/ontology/v1/rponto.html#codMIURscuola> ??? meglio crearne una nuova
DENOMINAZIONE|<http://www.w3.org/2000/01/rdf-schema#label>
ISTITUTO PRINCIPALE|<http://www.w3.org/ns/org#unitOf> ?
DENOMINAZIONE ISTITUTO PRINCIPALE|*Ridondante, va indicato nell'istituto principale*
INDIRIZZO|<http://www.w3.org/ns/locn#address>, ma l'indirizzo va in altro nodo come <http://www.w3.org/ns/locn#fullAddress>
CAP|nel nodo dell'indirizzo, come <http://www.w3.org/ns/locn#postCode> (Vedi anche http://www.dmi.unict.it/~longo/comunect/#luoghi )
COMUNE|<http://www.geonames.org/ontology#locatedIn> come AgID!
CARATTERISTICA|da creare nuova (circa 20 valori diversi rilevati)
TIPO ISTITUZIONE|da creare nuova (circa 35 valori diversi rilevati)
LATITUDINE|<http://www.w3.org/2003/01/geo/wgs84_pos#lat>
LONGITUDINE|<http://www.w3.org/2003/01/geo/wgs84_pos#long>

A parte i nodi per descrivere caratteristiche e tipi istruzione e ai nodi di tipo <http://www.w3.org/ns/locn#Address> si userebbero nodi di due classi:

 - Una per le istituzioni principali, sedi di segreteria: il tipo di amministrazione definito dall'AgID? <http://spcdata.digitpa.gov.it/CategoriaAmministrazione/L33> ... forse non va bene, perché non è concepito come una classe di oggetti...
 - Una per le sedi/plessi. Per la quale temporaneamente si potrebbe usare l'ontologia definita dalla Regione Piemonte: <http://id-dati.piemonte.it/ontology/v1/rponto.html#scuola>

Lo stesso sito riporta anche un file CSV coi [dati principali sulle scuole paritarie](http://www.istruzione.it/scuolainchiaro_dati/9-Anagrafe_Centri_Formazione_Professionale_201516.csv), che contiene le seguenti colonne, che possono essere riferite a ontologie simili alle precedenti:

Intestazione colonna|possibile predicato
--------------------|-------------------
REGIONE|<http://www.geonames.org/ontology#locatedIn> come AgID?
PROVINCIA|<http://www.geonames.org/ontology#locatedIn> come AgID?
PLESSO/SCUOLA|<http://id-dati.piemonte.it/ontology/v1/rponto.html#codMIURscuola> ??? meglio crearne una nuova
DENOMINAZIONE|<http://www.w3.org/2000/01/rdf-schema#label>
INDIRIZZO|<http://www.w3.org/ns/locn#address>, ma l'indirizzo va in altro nodo come <http://www.w3.org/ns/locn#fullAddress>
CAP|nel nodo dell'indirizzo, come <http://www.w3.org/ns/locn#postCode> (Vedi anche http://www.dmi.unict.it/~longo/comunect/#luoghi )
COMUNE|<http://www.geonames.org/ontology#locatedIn> come AgID!
TIPO ISTITUZIONE|da creare nuova (usando la stessa delle statali, ma meno valori)
LATITUDINE|<http://www.w3.org/2003/01/geo/wgs84_pos#lat>
LONGITUDINE|<http://www.w3.org/2003/01/geo/wgs84_pos#long>

Su tutte le scuole c'è un CSV coi [dati su alunni e classi](http://www.istruzione.it/scuolainchiaro_dati/1-Anagrafe_Nazionale_ALUNNI_CLASSI.csv). Questi sono dati *multidimensionali*, vedere se può servire l'ontologia per dati statistici https://github.com/UKGovLD/publishing-statistical-data/blob/master/specs/src/main/vocab/cube.ttl e gli intervalli di tempo come http://reference.data.gov.uk/doc/gregorian-interval/2015-09-01T00:00:00/P1Y .

### I dati di [geolocalizzazione](http://osgis2.csi.it/webgisAtlante/qgiswebclient.html?map=Scuole/BDTRE_SCUOLE_pubblicazione/) della Regione Piemonte
Contiene dati geografici dettagliati sugli edifici scolastici.

Licenza, secondo i [metadati presenti sul geoportale](http://www.geoportale.piemonte.it/geonetworkrp/srv/ita/pdf?id=2751) della Regione: CC-BY 2.5 .

Punti di forza:

* Presenta dati geografici abbastanza precisi e più specificatamente secondi i seguenti items:
  * PUNTI-localizzazione baricentrica sull'edificio scolastico definito "Principale"
  * PUNTI-localizzazione baricentrica sull'edificio scolastico definito "Subordinato"
  * POLYGON-localizzazione areale sulla superficie interessata dagli edifici scolastici afferenti; concetto di area di pertinenza diverso dal concetto catastale di area ad uso pertinenziale.!

[se serve posso caricare un documento che tratta l'approccio metodologico utilizzato per recuperare le informazioni, i rapporti intercorsi con gli enti locali proprietari e/o gestori di edifici scolastici, l'acquisizione effettuata mediante la localizzazione di tutti i contributi richiesti per le opere di manutenzione straordinaria in funzione di tutti bandi regionali attivi.]

* specificare meglio e dettagliare le geometrie sopradescritte ponendo l'accento sul vantaggio di un approccio areale che conteggi oltre ai punti di erogazione specifici anche la vicinanza tra essi al fine di riassumere dati non di un'unica sede ma di più punti di erogazione insieme - proporre e suggerire il concetto di "Analisi territoriale", di interrogazione spaziale, tematizzazione e non solo, come fino ad ora è accaduto, di un elenco di punti di erogazione del servizio isolati anche se vicini e confinanti.
[ampliare questo concetto fino ai temi legati alla "programmazione", al piano del dimensionameto scolastico inteso non solo come numero di studenti per autonomia ma come strumento di analisi territoriale per definire autonomie e sedi scolastiche, etc etc ]

Ad oggi si sta cercando di far scaricare direttamente questi 3 layer direttamente dal geoportale, ma, a breve, la pubblicazione tra i "data set" dell'Open Data regionale dovrebbe essere un'operazione già programmata.

???Oppure potrebbe essere utile capire se viene fornito anche un servizio WMS pubblico. -> ci si sta attrezzando per farlo!

Punti di debolezza:

* Attualmente il codice edificio (sia regionale che MIUR) non è riportato dagli open data ministeriali, solo un riferimento è al codice regionale nella procedura di consultazione "scuole in chiaro" nella sezione edilizia. [difficoltà di avere un campo per fare un join]
* Attualmente non permette di scaricare i dati, né di interrogare la base dati in maniera automatizzata
* Attualmente joinare il codice meccanografico del punto di erogazione del servizio con l'edificio è in via di definizione.

Verificare chi è titolare di questi dati e cercare un percorso che porti alla pubblicazione.
[se il titolare è il sottoscritto dovremmo riuscire in tempi brevi ad ottenere una base dati sufficientemente affidabile.]

Punti ancora da chiarire:

* Assenza totale del "codice edificio MIUR" CEM da tutti i dataset esistenti.
* Assenza di un codice MIUR che differenzi un punto di erogazione del servizio e la sua eventuale succursale (in Regione si è dovuto procedere ad una nuova codifica che tenesse conto di tale assenza).

### Portale aperTO, dati sulle [scuole](http://aperto.comune.torino.it/?q=node/129)

Tipo di informazioni che possono essere reperite da questo insieme di dati:

 * denominazione;
 * indirizzo postale;
 * coordinate geografiche;
 * contatti (telefono, e-mail, sito web)

Licenza: IODL v2.0 .

Punti di forza:

 * Presenta dati geografici molto precisi;
 * Informazioni su tutte le scuole presenti nel comune di Torino, statali e non, paritarie e non.

Punti di debolezza:

 * Non è chiaro se e ogni quanto verrà aggiornato, al momento della consultazione, riporta la data **18 Settembre 2014**
 * Limitato al solo territorio del comune di Torino.
 * Non dichiara la proiezione usata per le coordinate geografiche.

Comandi per scaricare la base dati in formato csv. Da shell:

```shell
$ curl "http://aperto.comune.torino.it/sites/default/files/scuole_0.csv"| tee aperto_comune_scuole.csv |wc -l
614
```

 * Nota, il file csv **contiene** una riga di intestazioni.

### Dati RDF da [dati.piemonte](http://www.dati.piemonte.it/rdf.html)

Analisi in particolare dei dati su http://id-dati.piemonte.it/resource/scuole/scuole-piemonte.html

Tipo di informazioni che possono essere reperite da questo insieme di dati:

* Quasi nulla, non molto oltre ad una struttura per le scuole
* Un grafo contenente comuni e province della regione

Licenza: non trovata, "open by default"?

Punti di forza:

* Il formato RDF si presta ad essere riutilizzato e riferito in altri LOD
* L'ontologia include [rponto:codMIURscuola](http://id-dati.piemonte.it/ontology/v1/rponto.html#codMIURscuola) che indica il codice meccanografico usato dal MIUR per riferirsi alle scuole

Punti di debolezza:

* Non contiene alcuna data di aggiornamento, quindi non si capisce se e quando i dati sono aggiornati
* In considerazione di ciò probabilmente non ha senso neppure usare l'elenco di comuni/province, meglio ISTAT o AgID&hellip;
* gli URI sono fasulli e non indicano effettive pagine web visitabili
* la struttura regge ma sostanzialmente vuota, il contenuto è quasi inesistente

Comandi per scaricare la base dati. Da shell:

```shell
$ curl "http://id-dati.piemonte.it/resource/scuole/scuole-piemonte.rdf"| tee dati_piemonte_scuole.rdf|grep rponto.codMIURscuola|wc -l
4466
```

Il numero pari a 4466 sembra elevato rispetto alle 3850 conteggiate nei dati MIUR, le scuole per le quali il codice meccanografico risulta mancante o errato sono comunque poche. Possiamo comunque verificare quali codici si ripetono il maggior numero di volte:

```shell
$ grep rponto.codMIURscuola dati_piemonte_scuole.rdf|sort|uniq -c|sort -n|tail -4
      6 	<rponto:codMIURscuola>topc020003</rponto:codMIURscuola>
      6 	<rponto:codMIURscuola>torc060005</rponto:codMIURscuola>
      8 	<rponto:codMIURscuola>-</rponto:codMIURscuola>
      8 	<rponto:codMIURscuola>torc05000e</rponto:codMIURscuola>
```

da cui si vede che oltre al meccanografico vuoto `-`, risulta ripetuto parecchie volte il codice `torc05000e`.

### Dati da ISTAT?

L'[*end-point* SPARQL dell'ISTAT](http://datiopen.istat.it/sparql) prevede la classe <http://datiopen.istat.it/odi/ontologia/territorio/SCH>, potremmo controllare se e quanto è usata&hellip;

```SPARQL
PREFIX ter: <http://datiopen.istat.it/odi/ontologia/territorio/>
SELECT ?s ?p
WHERE {
?s ?p ter:SCH
} LIMIT 100
```

restituisce [poche cose](http://datiopen.istat.it/sparql/oracle?query=PREFIX+ORACLE_SEM_FS_NS%3A+%3Chttp%3A%2F%2Foracle.com%2Fsemtech%23timeout%3D600%2Callow_dup%3Dt%2Cstrict_default%3Df%3EPREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX+ter%3A+%3Chttp%3A%2F%2Fdatiopen.istat.it%2Fodi%2Fontologia%2Fterritorio%2F%3E%0APREFIX+cen%3A+%3Chttp%3A%2F%2Fdatiopen.istat.it%2Fodi%2Fontologia%2Fcensimento%2F%3E%0APREFIX+qb%3A+%3Chttp%3A%2F%2Fpurl.org%2Flinked-data%2Fcube%23%3E%0ASELECT+%3Fs+%3Fp%0AWHERE+{%0A%3Fs+%3Fp+ter%3ASCH%0A}+LIMIT+100%0A&stylesheet=/sparql/xml-to-html.xsl)

### Altri dati in giro&hellip;

Forse vale la pena guardare cose pubblicate da altre amministrazioni grandi o piccole e raccolte da [dati.gov.it](http://www.dati.gov.it/dataset?f[0]=field_themes%3A2&f[1]=field_resources%253Afield_format%3A56)

Proposta per un'ontologia dei dati sulle scuole
===============================================

Partendo dalle proposte indicate per i dati MIUR di anagrafe delle scuole statali, si è provato a scrivere una prima bozza di ontologia per tali dati, [in formato Turtle](RDF/miur.ttl).

Innanzitutto le istituzioni scolastiche sono state definite come sottoclasse delle organizzazioni, ispirandosi all'ontologia standardizzata dal W3C per le organizzazioni <http://www.w3.org/ns/org>, di cui ci siamo estratti [una copia ridotta](RDF/org.ttl).

Le scuole
---------

Per definire una scuola non ci possiamo limitare al concetto di istituzione, perché la scuola potrebbe non essere una pubblica amministrazione... inoltre ha probabilmente senso creare una classe ampia, che contempli anche la fase pre-scolastica.

Così è stata creata una sottoclasse di `org:Organizazion`, con una precisa chiave distintiva, il codice meccanografico stabilito dal MIUR.

```turtle
miurO:Scuola a owl:Class, rdfs:Class;
  rdfs:subClassOf org:Organization;
  owl:equivalentClass rponto:scuola;
  rdfs:label "Scuola"@it;
  owl:hasKey (miurO:meccanografico) ;
  rdfs:comment "Rappresenta una scuola in senso generale di organizzazione che fornisce servizi di istruzione scolastica o pre-scolastica, ma non universitaria, catalogata dal MIUR."@it;
  rdfs:isDefinedBy miur:ontologia ;
  rdfs:seeAlso <http://www.geonames.org/ontology#S.SCH> ;
.
```

In questa definizione probabilmente è un po' azzardato considerare classe equivalente quella (maldestramente) definita dalla Regione Piemonte, perché essa non è molto chiara neppure nell'intenzione. Certamente non si può stabilire una equivalenza con la definizione di `geonames`, che si riferisce esplicitamente agli edifici scolastici.

