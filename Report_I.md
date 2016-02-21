![UPO](https://www.uniupo.it/sites/all/themes/bootstrap/unipm/img/std/logo.png)

MASTER IN MANAGEMENT DEL SOFTWARE LIBERO - PROJECT WORK
=======================================================

* Titolo: **Open Data**
* Componenti gruppo di lavoro ed enti di provenienza
  1. Marco BODRATO, [MIUR - Ufficio Scolastico Regionale per il Piemonte](http://www.istruzionepiemonte.it/);
  2. Claudia CONFORTI, Regione Piemonte;
  3. Anna Alessandra MASSA, [MIUR - Ufficio Scolastico Regionale per il Piemonte](http://www.istruzionepiemonte.it/);
  4. Gianbruno VERDA, Regione Piemonte;
  5. Guido VERNERO, Comune di Torino.
* Responsabile di ambito: 
* Docente responsabile del PW: 
* Tutor responsabili: 

# Aspetti Organizzativi

## CONSIDERAZIONI INTRODUTTIVE

## DESCRIZIONE ANALITICA

# ASPETTI TECNICI

## Dati trasparenza

### Problema

### Situazione attuale

### Proposte

## Dati già pubblicati sulle scuole

### Problema

Molti dati provenienti da diverse fonti, ma difficili da mettere in relazione per avere una visione a tutto tondo del mondo dell'istruzione.

### Situazione attuale

Analizzata brevemente in (altro documento)[DatiScuole.md].

### Percorso di lavoro

1. Verificare coerenza tra i dati pubblicati dai diversi enti.
2. Sperimentare e proporre percorsi di interoperabilità, anche evidenziando le incoerenze riscontrate per proporre le verifiche del caso sui dati pubblicati.
3. Per gli enti coinvolti (MIUR, Regione, Comune di Torino), provare a strutturare i dati già pubblicati usando *ontologie* comuni.
4. Collegare anche i [dati che seguono](#dati-della-regione-piemonte-sugli-edifici-scolastici)...

## Dati della Regione Piemonte sugli edifici scolastici

### Problema

La regione raccoglie da anni dati molto dettagliati sulle aree scolastiche e sugli edifici. Esiste una pubblicazione degli stessi tramite il geoportale regionale, ma tecnicamente il riuso risulta molto difficoltoso.

### Situazione attuale

I dati sono immagazzinati sotto forma di Shapefile o di Geo-DataBase?

### Proposte

A parte gli aspetti *politici*/organizzativi, tecnicamente possono essere analizzati i seguenti punti:

1. Verificare l'esistenza di formati liberi che permettano di esportare tutti gli aspetti di questa raccolta dati.
2. Analizzare quali di questi dati possono essere resi facilmente interoperabili con quelli analizzati nei [punti precedenti](#dati-gia-pubblicati-sulle-scuole).
3. Costruire con almeno un sottoinsieme di questi dati una struttura di tipo Linked Open Data.

# ASPETTI GIURIDICI 

## Privacy

### Identificazione problemi

### Modelli ed esempi

### Proposta di soluzione

## Licenze per dati aperti
Per massimizzare le possibilità di riuso (e quindi il valore) dei dati aperti, oltre alla qualità dei dati stessi, è necessario garantire diverse condizioni: i dati devono essere accessibili (pubblicati e reperibili), tecnicamente lavorabili (ben strutturati e _machine-readable_) e legalmente riutilizzabili.
Quest'ultimo punto dipende dalla licenza d'uso scelta (o mancante) per i dati.

### Identificazione problema
La presenza di diverse licenze e svariati orientamenti non facilita il riuso dei dati pubblicati dalle diverse PA, né da parte di imprese e cittadini, né da parte delle PA stesse che potrebbero trovarsi in difficoltà ad mescolare dati provenienti da diverse amministrazioni.

### Modelli di soluzione ed esempi
Le [Linee guida dell'AgID](http://www.agid.gov.it/sites/default/files/linee_guida/patrimoniopubblicolg2014_v0.7finale.pdf) approfondiscono il tema nel capitolo 8.

#### IODL
Una delle soluzioni che sembrerebbe più naturale sarebbe quella di affidarsi alle licenze scritte **appositamente** per la pubblicazione di dati aperti da parte delle pubbliche amministrazioni italiane, le IODL ([Italian Open Data Licence](https://it.wikipedia.org/wiki/Italian_Open_Data_License)), in una delle versioni pubblicate: v1.0 e v2.0.
Tanto che, secondo il [sito dati.gov.it dell'AgID](http://www.dati.gov.it/content/italian-open-data-license-domande-e-risposte) _rappresentano le licenze più utilizzate, per numero di amministrazioni, in Italia_.

**Problema**: tali licenze sono perlopiù sconosciute all'estero, pertanto non facilitano il riuso da parte di attori che agiscono a livello internazionale. Quindi **incertezza**.

#### _Open by default_
Altra possibile soluzione, non apporre alcuna licenza. Secondo il comma 2 del[l'articolo 52 del CAD](http://www.agid.gov.it/cad/accesso-telematico-riutilizzo-dati-pubbliche-amministrazioni) i dati così pubblicati **da una PA** _si intendono rilasciati come dati di tipo aperto_, si applica il principio dell'_Open Data by default_.

**Problema**: il potenziale interessato che non vede nessuna licenza potrebbe pensare semplicemente di non essere stato capace di trovarla. Le già citate _Linee guida dell'AgID_ si spingono ad affermare che _la mancata indicazione della licenza implica che i dati siano pubblicati secondo i termini stabiliti dalla licenza CC-BY (attribuzione)_, ma ciò non è del tutto convincente ed è comunque impreciso, quale versione delle CC? Viene richiesta l'attribuzione, ma in che modo? Anche in questo caso **incertezza**.

#### Creative Commons
Alcuni insiemi di dati sui portali della Regione Piemonte (e non solo), usano la licenza [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Questa licenza non richiede nemmeno l'attribuzione ed in generale rinuncia ai diritti morali, che però in Italia sono indipsonibili, pertanto potrebbe non essere la licenza più consigliabile.  

Sempre le _Linee guida dell'AgID_ concludono consigliando _l’uso della CC-BY nella sua versione 4.0_; questa licenza è un'aggiornamento delle versioni precedenti mirato in particolare ad avere una solida validità internazionale ed a considerare anche il diritto _sui generis_ per le basi di dati. Lo stesso documento però è concorde con [i documenti in rete di OpenStreetMap](http://wiki.openstreetmap.org/wiki/Import/ODbL_Compatibility) nel rilevare che tale licenza **non è compatibile** con la licenza [ODbL](http://opendatacommons.org/licenses/odbl/summary/). Considerando che quest'ultima è proprio la licenza usata da [OpenStreetMap](http://www.openstreetmap.org/), probabilmente il più rilevante portale collaborativo di raccolta e rappresentazione di dati geografici, l'uso di questa licenza non sembra una buona soluzione, in particolare per dati geografici.

#### ODbL
Al converso, la scelta di usare la licenza ODbL per rilasciare le proprie basi dati ci costringerebbe all'uso di una licenza poco usata se non per dati geografici e comunque **non compatibile** con le licenze CC che sono molto più diffuse.

### Sintesi proposta
Ci proporremmo pertanto di indicare sempre esplicitamente una licenza d'uso, che preveda almeno l'attribuzione, per evitare le incertezze giuridiche.

Al fine di evitare l'incompatibilità tra le modalità di attribuzione richieste dalle licenze CC-BY e quelle della licenza ODbL, si propone di proporle entrambe, in parallelo, a scelta del riutilizzatore. La pratica di usare [licenze multiple per evitare incompatibilità tra licenze libere](https://en.wikipedia.org/wiki/Multi-licensing#License_compatibility) è una prassi già sperimentata nell'ambito del software libero, forse un po' meno nell'ambito dei dati aperti, ma non c'è che da iniziare.

# GESTIONE DEL CAMBIAMENTO

# Appendice A

## Tabella vecchio software (???)

## Tabella vecchi formati

Num|Nome|Pro|Contro|Licenza|Note
---|----|---|------|-------|----
1|ESRI-Shapefile|diffuso, gestibile anche con software liberi|informazioni suddivise su diversi file|da verificare|Si veda anche paragrafo 6.2.2 del [documento AgID](http://www.agid.gov.it/sites/default/files/linee_guida/patrimoniopubblicolg2014_v0.7finale.pdf)
2|xls|diffuso,molte librerie libere lo leggono|vecchio e con alcune limitazioni|chiusa|*superato* da xlsx
2|xlsx|abbastanza diffuso, meglio documentato di xls||da verificare|successore di xls

## Tabella possibili formati analizzati

Num|Nome|Pro|Contro|Licenza|Note
---|----|---|------|-------|----
1|GeoJSON|Facilmente importabile anche da web-app||standard aperto|
2|CSV|essenziale|non auto-descrittivo: quale separatore? quale codifica?|nessuna (libera)|il più *portabile* per tabelle semplici
2|ODS|standard ISO, oggi leggibile anche da Suite Office non libere||standard aperto|
