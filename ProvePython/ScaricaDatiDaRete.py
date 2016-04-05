# Scarica tutti i file che ci servono

import sys
import urllib
import os.path

sovrascrivi = False

if len(sys.argv) == 2 and sys.argv[1] == "-o":
        sovrascrivi = True
elif len(sys.argv) > 1:
        sys.stderr.write("Parametro non riconosciuto.\n")
        sys.exit(1)

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
        if not os.path.isfile (nome) or sovrascrivi:
	        print 'Scarico', nome, 'da', listaFile[nome]
	        accessoWeb.retrieve (listaFile[nome] , nome )
        else:
	        print nome, 'esiste, non lo sovrascrivo'
