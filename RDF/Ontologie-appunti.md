Da: https://www.w3.org/TR/owl2-primer/

(4.1) Le **classi** sono utilizzate per descrivere un gruppo che hanno qualcosa in comune, così da poterci riferire ad essi. 
Quindi se una classe è "Dpcm-22-09-2014" allora un'**istanza** di essa potrebbe essere l'Indice di tempestività dei pagamenti

 :Dpcm-22-09-2014  rdf:type owl:Class .
 :IndiceDiTempestivitaDeiPagamenti rdf:type :Dpcm-22-09-2014

E' poi ovvio che l'appartenenza ad una classe non è esclusiva: quindi per esempio l'indice di tempestività dei pagamenti 
oltre che appartenere alla classe "Dpcm 22/09/2014" potrà per esempio appartenere 
anche ad una ipotetica classe "Finanza pubblica" oppure alla classe "Dlgs 33/2013" o altro ancora.

(4.2) Ora, risulta chiaro che per alcune classi definite, per esempio: ObblighiDiPubblicazione e IndiceDiTempestivitaDeiPagamenti 
esiste tra di loro una qualche relazione. Per consentire ad un sistema (parlante per le macchine) di comprendere la relazione 
a noi umani evidente, occorre istruirlo di questa corrispondenza. In OWL 2, questa conoscenza è data dal un cosiddetto assioma **sottoclasse**.

 :ObblighiDiPubblicazione  rdf:type owl:Class .
 :Dpcm-22-09-2014 rdfs:subClassOf :ObblighiDiPubblicazione .
