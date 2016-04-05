Da: https://www.w3.org/TR/owl2-primer/

(4.1) Le **classi** sono utilizzate per descrivere un gruppo che hanno qualcosa in comune, così da poterci riferire ad essi. 
Quindi se una classe è "Dpcm-22-09-2014" allora un'**istanza** di essa potrebbe essere l'Indice di tempestività dei pagamenti

 :Dpcm-22-09-2014  rdf:type owl:Class .
 :IndiceDiTempestivitaDeiPagamenti rdf:type :Dpcm-22-09-2014

 ,dove "owl:" sta ad indicare l'ontologia al link :http://www.w3.org/2002/07/owl#. Per definire questo nell'ontologia
 dobbiamo anzitutto definire dei prefissi: @prefix owl: <http://www.w3.org/2002/07/owl#>

E' poi ovvio che l'appartenenza ad una classe non è esclusiva: quindi per esempio l'indice di tempestività dei pagamenti 
oltre che appartenere alla classe "Dpcm 22/09/2014" potrà per esempio appartenere 
anche ad una ipotetica classe "Finanza pubblica" oppure alla classe "Dlgs 33/2013" o altro ancora.

:Dpcm-22-09-2014  rdf:type owl:Class .
:Dpcm-22-09-2014  rdfs:comment "Definizione degli schemi e delle modalita' per la pubblicazione su internet dei dati relativi alle entrate e alla spesa dei bilanci preventivi e consuntivi e dell'indicatore annuale di tempestivita' dei pagamenti delle pubbliche amministrazioni."^^xsd:string .

(4.2) Ora, risulta chiaro che per alcune classi definite, per esempio: ObblighiDiPubblicazione e IndiceDiTempestivitaDeiPagamenti esiste tra di loro una qualche **relazione**. Per consentire ad un sistema (parlante per le macchine) di comprendere la relazione a noi umani evidente, occorre istruirlo di questa corrispondenza. In OWL 2, questa conoscenza è data dal un cosiddetto assioma sottoclasse.

  :ObblighiDiPubblicazione  rdf:type owl:Class .
 :Dpcm-22-09-2014 rdfs:subClassOf :ObblighiDiPubblicazione .

 Due classi sono considerate equivalenti se contengono esattamente gli stessi individui. 
 Il seguente esempio indica che la classe "DecretoTrasparenza" è equivalente alla classe "Dlgs-33-2013".
 
 :DecretoTrasparenza owl:equivalentClass :Dlgs-33-2013 .

(4.3) In alcuni casi, l'appartenenza di un'istanza ad una classe esclude l'appartenenza ad un'altra.
Ad esempio, se consideriamo le classi Uomo e Donna possiamo affermare che nessun individuo può essere un'istanza di entrambe
(per il bene di questo esempio, si prescinde casi limite biologici). Questo rapporto di incompatibilità tra le classi è indicato come
 **classe disgiunta**. Per indicare esplicitamente la disgiunzione delle classi:
 
 []  rdf:type     owl:AllDisjointClasses ;
     owl:members  ( :Woman  :Man ) .
     
 , dove [] indica "qualunque istanza"
 
Il fatto di dichiarare classi disgiunte può aiutare a comprendere che se un'istanza appartiene ad una classe allora questa non appartiene all'altra: se definisco una tripla in cui "Gianbruno" appartiene alla classe "Uomo", allora si potrà dedurre che esso non è "Donna".

(4.4) Si è visto come le classi possano relazionarsi tra di loro in base alle loro istanze, ma non solo queste relazioni esistono in un'ontologia, molte volte infatti, è necessario specificare come istanze diverse siano in **relazione** tra di loro.
Ad esempio se prendiamo in considerazione le informazioni richieste dalla la Legge 190/2012 relativamente alle gare d’appalto degli Enti Pubblici, si può dire che una certa Ditta A è capofila in un raggruppamento d’impresa con altre Ditte. Le istanze sono pertanto in relazione tra loro, in questo caso andremmo a definire nell’ontologia:

:èCapofila rdf:type owl:ObjectProperty .
:èCapofila rdfs:domain      :Ditta ;
           rdfs:range       :Raggruppamenti d’impresa .
:èConsociata  rdf:type  owl:ReflexiveProperty .

, dove owl:ReflexiveProperty sta ad indicare che se :DittaA :èConsociata :DittaB, allora vale anche il contrario
(4.6) In questo caso rdfs:domain sta ad indicare che l’istanza “soggetto” dovrà essere di tipo “Ditta” mentre l’istanza “oggetto” dovrà essere di tipo “Raggruppamento d’impresa”.

(4.7) E’ bene ricordare che l’oggetto potendo essere anche un valore (o **Datatype**), tipo stringa, intero, booleano etc.. una di proprietà nell’ontologia potrebbe anche avere il seguente aspetto, per esempio per indicare che il numero di giorni di pagamento non può essere inferiore a Zero :

:Periodo  rdfs:domain  :ValoreIndice ;
          rdfs:range   xsd:nonNegativeInteger .

, in questo caso usando “Domain” e “Range” stiamo dicendo che l’oggetto è un Datatype, nell’esempio qui sopra indichiamo che in un dato periodo il valore dell’Indice di Tempestività dei Pagamenti sarà un intero non negativo.
Senza definire che ValoreIndice è nel dominio, cioé che è “soggetto”, della proprietà “Periodo”, ma pur definendone il valore non-negativo avremmo anche potuto scrivere:

 :ValoreIndice  owl:onDatatype  xsd:nonNegativeInteger .


(5) Definite le Classi per individuare gruppi di istanze dello stesso tipo, queste, così come le istanze possono essere usate come blocchi per definire nuove classi.
(5.1) Il linguaggio OWL fornisce gli elementi classici della logica and, or, not che corrispondono ai termini (class) intersection, (class) union e (class) complement.
Ad esempio: l'intersezione di due classi consiste esattamente di quegli elementi che sono istanze appartenenti ad entrambe le classi; l'unione di due classi contiene ogni individuo che è contenuto in almeno una di queste e il complemento di una classe corrisponde alla negazione logica: è cioé composto da esattamente quegli oggetti che non sono membri della classe stessa.
