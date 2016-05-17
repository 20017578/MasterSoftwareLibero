# Legge il file di configurazione per produrre il lod


# import urllib
import sys
import csv
import string

# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def funzione(stringa_pa):

    return stringa_pulita






try:
    file_csv_config_main = open ('campi_config.csv')
except:
    print 'File non trovato, provo da rete.'

def_campi=[]
# LEGGIAMO IL FILE CON IL NOME DEI TIPI DI CAMPO
riga_csv=file_csv_config_main.readline()
while riga_csv:
    riga_csv=riga_csv.rstrip()
    def_campi.append(riga_csv)
    riga_csv = file_csv_config_main.readline()


# APRO IL FILE CONTENENTE LA CONFIGURAZIONE
campi = []
nomeFileDati = 'config_toponomastica.csv'
with open(nomeFileDati, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ',')
       n_righe=0
       for row in reader:
           n_righe=n_righe+1
           n_campi=len(row)
           i=0
           while i<n_campi:
              campi.append(row[i])
              i=i+1


print ('Il CSV da sottoporre deve avere le seguenti caratteristiche :')
print ('NUMERO CAMPI POSSIBILI = ',n_campi)
i=0
while i<n_campi:
    print
    print 'Campo nr.',i+1,' :'
    j=0
    while j<n_righe:
        print def_campi[j],' -> ',campi[(j*n_campi)+i]
        j=j+1
    i=i+1
