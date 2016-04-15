PW5-Stato di avanzamento in merito alla parte applicativa "Scuole"
==================================================================

Al fine di consentire di descrivere nella maniera più dettagliata possibile le tipologie di dati riferite
alla parte più applicativa del nostro Project Work 5 il cui processo di rielaborazione, tramite i
linguaggi appresi durante il Master, possa contribuire all'avanzamento della parte di esempi
operativi e che nel nostro caso riguarda i dati sulle scuole ed i dati sulla trasparenza, si è redatto
questo documento che, a breve, rappresenterà il documento di metadatazione dei dati "scuole"
scaricabili dal DBgeografico pubblicati sul Geoportale della Regione Piemonte.

Gli shape file scaricabili dalla pubblicazione sul Geoportale Regionale si riferiscono a due livelli
informativi geografici specifici individuati come: Aree Scolastiche e Punti.

La possibilità di creare dei Linked Open Data che, oltre che avvalersi delle fonti già sperimentate (AgID, Miur, Istat, dati.gov.it, etc) dovrebbe consentire di rendere sempre più realistico e esaustivo
l'esempio applicativo scelto all'interno del PW.

Genesi della produzione di dati georiferiti
-------------------------------------------

Nell'arco degli ultimi anni, è stato attivato un progetto di impianto di un Dbgeografico su questo
aspetto specifico attraverso il quale sono state recuperate tutte le informazioni analogiche
(cartografie, allegate ai progetti, estratti di Mappe Catastali e/o di Piani Regolatori che nel tempo
erano in deposito presso il Settore in quanto oggetto di trasmissione di elaborati progettuali utili alla
richiesta di contributi da parte degli enti proprietari per la manutenzione straordinaria degli edifici,
utilizzo di elenchi di dati derivanti da collaborazioni con i Comuni piemontesi e le Province
piemontesi che in modo non omogeneo avevano comunque informazioni utili a tale riguardo, etc).
Attraverso un lungo lavoro minuzioso di controllo e di georeferenziazione sono state caricate le
geometrie in termini di coppie di coordinate nel sistema di riferimento regionale (**UTM-WGS84 ­ sistema di proiezione 32632**- sistema adottato nelle linee guida D.G.R. 22-4687 del 8-10-2012
art.5) tentando di associare codici univoci depositati dall'applicativo EDISCO (Anagrafe
dell'Edilizia Scolastica)..

Analisi Dati
------------

A. I **punti** rappresentano la geolocalizzazione sul baricentro dell'edificio scolastico ed una serie di attributi di seguito riportati. (vedi Tab. 1)

Si è preferito utilizzare il baricentro dell'edificio rispetto ad altre eventuali localizzazioni puntuali
(ad esempio il numero civico di accesso all'edificio) in quanto, in questa fase di primo impianto del
progetto, il controllo delle attività in itinere era di livello "*macro*" e quindi i controlli dovevano
avvenire sulla coerenza topologica tra il punto e le aree; pertanto il punto dell'accesso stradale pur
essendo molto utile in una successiva rielaborazione delle geometrie a livello "*micro*" ad oggi non è
stato preso in considerazione e potrà essere presente in versioni successive.

B. Le **aree scolastiche** che rappresentano una serie di poligoni che definiscono l'area di pertinenza dell'edificio scolastico intesa come area che accorpa eventuali altri edifici puntuali afferenti allo stesso plesso scolastico. (vedi Tab. 2).

Occorre a questo riguardo ricordare come il concetto di area scolastica considerata nella
realizzazione di questo livello informativo possa assumere indifferentemente il contorno di un
poligono relativo al solo edificio (nel caso di un edificio inserito in un tessuto urbano densamente
edificato) o, in caso di aree urbanisticamente destinate a servizi, il contorno di aree in cui sono
contenuti più edifici scolastici. Nessuna relazione è per ora da attribuirsi alla definizione di "*area
scolastica di pertinenza*" in analogia all'area di pertinenza dell'edificio secondo una terminologia
legata al catasto terreni (fogli di mappa, o dividenti di frazionamento).

Di seguito vengono descritti i tracciati record e le sintesi descrittive.

###Tab. 1 : Descrizione Shape file "PUNTI.shp"

num ord|nome campo|tipo|nome tipo|lungh|prec|desc campo|Poss. valorizz|note
-------|----------|----|---------|-----|----|----------|--------------|----
0|id_progr_scuole_pt|int|Int4|-1|0|id univoco identificativo del punto assegnato manualmente|id crescente
1|fk_uuid_edifc|Qstring|varchar|500|-1|id univoco identificativo del punto assegnato automaticamente|id automatico
2|fonte|Qstring|varchar|500|-1|data assegnazione attributi sorgente|21-10-2014
3|tipo_edi|Qstring|varchar|500|-1|tipo edificio|E-S E-P
4|agg|Qstring|varchar|500|-1|null|data
5|pro|Qstring|varchar|500|-1|sigla targa provincia|AL, AT, BI, CN, NO, TO, VB, VC|ridurre a 2 chr
6|comune|Qstring|varchar|500|-1|nome comune||normalizzati in base all'assenza di apostrofi e lettere accentate '=ascii 096
7|ristat|Qstring|varchar|500|-1|codice istat comune anteponendo prefisso"R"
8|istat|Qstring|varchar|500|-1|codice istat comune
9|tipo_scu|Qstring|varchar|500|-1|grado scolastico edificio scolastico
10|deno_scu|Qstring|varchar|500|-1|eventuali denominazione dei P.E.S
11|ind_scu|Qstring|varchar|500|-1|eventuale indirizzo dei P.E.S.|
12|c_sede_i|Qstring|varchar|500|-1|eliminare
13|ind_stu|Qstring|varchar|500|-1|eventuale indirizzo distudio dei P.E.S.
14|rcerp|Qstring|varchar|500|-1|Codice Edificio Regione Piemonte anteponendo prefisso"R"||ridurre a 20 chr
15|cerp|Qstring|varchar|500|-1|Codice Edificio Regione Piemonte||ridurre a 20 chr
16|cem|Qstring|varchar|500|-1|Codice Edificio Miur||ridurre a 20 chr
17|coord_x|double|numeric|15|5|coordinata X nel sistema di proiezione utm-wgs84 32632||Aumentare a 6 cifre decimali
18|coord_y|num|double reale|15|5|coordinata Y nel sistema di proiezione utm-wgs8432632||Aumentare a 6 cifre decimali
19|fi|num|double reale|15|5|coordinata LAT nel sistema di proiezione geographic 4326||Aumentare a 6 cifre decimali
20|lambda|num|double reale|15|5|coordinata LON nel sistema di proiezione geographic 4326||Aumentare a 6 cifre decimali
21|note_gg|Qstring|varchar|500|-1|punto rappresentato dalle coppia di coordinate nel sistema geographic 4326
22|flg_statal|Qstring|varchar|500|-1|flag statale||ridurre a 2 chr
23|flg_parita|Qstring|varchar|500|-1|flag paritaria||ridurre a 2 chr
24|flg_comuna|Qstring|varchar|500|-1|flag comunale||ridurre a 2 chr
25|flg_privat|Qstring|varchar|500|-1|flag privata||attualmente rappresenta punti
26|note|Qstring|varchar|500|-1|eventuale campo note|x|non coincidenti con edifici della BDTRE
27|data_edit|Qstring|timestamp|254|0|eventuale data di aggiornamento
28|user_edit|Qstring|varchar|50|-1|codice identificativo del soggetto che ha effettuato la modifica

Obiettivi e risultati
---------------------

1. La strutturazione del Dbtopografico così come realizzato consente di non trattare ogni singolo punto "fine a se", infatti pur contenendo tutte le informazioni legate alle informazioni sull'edificio scolastico esse possono venire elaborate mediante tecniche G.I.S. di "overlay", al fine di estrarre tutti i punti (edifici) che insistono all'interno di una stessa area di pertinenza a carattere "scolastico" Se a questo punto le elaborazioni consentono di sommare valori che prima erano solo dell'entità "Punto". (ad esempio popolazione scolastica che afferisce ad ogni punto) potrebbero venire valorizzati per ogni area e quindi partendo da un dato granulometricamente di livello base ad una generalizzazione che tenga conto degli attributi esistenti complessivamente nell'area.
2. Altro interessante obiettivo è rappresentato dalla possibilità di "ereditare" informazioni che sono depositate su altri livelli informativi presenti bnei dataset geografici e riferita ad altre tematiche. La immediata conoscenza della localizzazione di un edificio in area ad esondazione, in aree con vincoli sismici, la stessa informazione sui dati catastali (frutto non più di un caricamento alfanumerico) ma attraverso una semplice operazione di overmapping e, non ultima, la popolazione di attributi che implementano il complesso dataset relativo alla **BDTRE** può essere il giusto obiettivo di interoperabilità sancita sia a livello normativo nazionale che regionale.
3. Il risultato già conseguito è consistito nella possibilità di utilizzare le funzioni del Geoportale per una consultazione personalizzata che consente di vedere il progetto dinamicamente in pubblicazione. A tale fine si allega una sintetica tematizzazione che consente di comprendere immediatamente le tipologie di edifici rappresentati.

Oltre a tenere conto che la possibilità di scaricare in formato shape file (che rappresentano secondo
le diretive INSPIRE un formato di interoperabilità) i due layer oggetto di queste note di
metadatazione è un risultato che conclude una fase di impianto ponendo le basi per eventuali
possibili miglioramenti.

Applicata all'attività del PW5 questa "ufficiale" metadatazione consente di rendere più semplice
l'esercitazione applicativa permettendo di ottenere del L.O.D. che possano avere una pratica
utilizzazione.
