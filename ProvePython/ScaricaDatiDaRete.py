# Scarica tutti i file che ci servono

import urllib

proxy = None
# proxy = {'http': 'http://proxy.regione.piemonte.it:80'}

accessoWeb = urllib.URLopener(proxies=proxy)

listaFile = {
        'DatiMIUR.csv' : 'http://www.istruzione.it/scuolainchiaro_dati/7-Anagrafe_Scuole_Statali_201516.csv' ,
        'DatiAgID.ttl' : 'http://spcdata.digitpa.gov.it/data/amm.ttl' ,
        'DatiMIUR_paritarie.csv' : 'http://www.istruzione.it/scuolainchiaro_dati/8-Anagrafe_Scuole_Paritarie_201516.csv' ,
        'DatiTorino.csv' : 'http://aperto.comune.torino.it/sites/default/files/scuole_0.csv' ,
        'DatiMIUR_alunniClassi.csv' : 'http://www.istruzione.it/scuolainchiaro_dati/1-Anagrafe_Nazionale_ALUNNI_CLASSI.csv' ,
        'DatiAgID.csv' : 'http://spcdata.digitpa.gov.it/data/amm.csv' ,
        'DatiMIUR_personale.csv' : 'http://www.istruzione.it/scuolainchiaro_dati/6-Personale_scuola.csv' ,
}

for nome in listaFile:
	print 'Scarico', nome, 'da', listaFile[nome]
	accessoWeb.retrieve (listaFile[nome] , nome )

