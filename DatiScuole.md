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

 * mancanza di uniformità tra i dati riguardanti le scuole statali e quelle non statali, che hanno oblighi ed interessi diversi nell'alimentare il sistema informativo del MIUR
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

Tipo di informazioni che possono essere reperiti da questo insieme di dati:

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
$ curl "http://aperto.comune.torino.it/sites/default/files/scuole.csv"| tee aperto_comune_scuole.csv |wc -l
614
```

 * Nota, il file csv **contiene** una riga di intestazioni.
