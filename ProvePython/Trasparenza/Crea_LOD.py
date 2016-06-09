#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import sys
import csv
import string
import hashlib


# FUNZIONE CHE LEGGE I FILE DI CONFIGURAZIONE UTILI ALLA GENERAZIONE DELLE TRIPLE
def leggi_configurazione(nomeFileConfig):

    # LEGGO IL FILE campi_config CHE CONTIENE IL NOME DEI DIVERSI RECORD PRESENTI NEI FILE
    #  DI CONFIGURAZIONE, le prime 10 righe servono a descrivere il nodo e non proprietà ed oggetti
    try:
        file_csv_config_main = open ('campi_config.csv')
    except:
        print 'File non trovato.'
    def_campi=[]                             # def_campi contiene i nomi
    riga_csv=file_csv_config_main.readline()
    while riga_csv:
        riga_csv=riga_csv.rstrip()           # rstrip elimina il carattere /n a fine riga
        def_campi.append(riga_csv)
        riga_csv = file_csv_config_main.readline()
    file_csv_config_main.close()

    # LEGGO IL FILE CONTENENTE LA CONFIGURAZIONE SPECIFICA PER IL TIPO DI DATO CHE STO ELABORANDO, QUESTO SARA' MODELLATO
    #  SEMPRE NELLO STESSO MODO ED OGNI RIGA (RECORD) SARA' RIFERITO AL TITOLO ESTRATTO COL FILE campi_config PRECEDENTE
    campi = []                                     # campi i valori utili alla produzione delle triple
    with open(nomeFileConfig, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ',')   # funzione per leggere un csv splittandolo a seconda del carattere delimitatore, funziona meglio della funzione split limitata alle stringhe in quanto riconosce i campi di testo racchiusi tra virgolette
       for row in reader:
           n_campi=len(row)
           i = 0
           while i<n_campi:
                campi.append(row[i])          # campi conterrà tutti i dati in sequenza, prima la quelli della riga 11, poi la 12 e così via
                i = i + 1
    csvfile.close()

    # SCRIVO I DATI UTILI CIRCA I POSSIBILI CAMPI (OVVERO LE PROPRIETA') DELLE TRIPLE
    print 'Il LOD da produrre potrà avere i seguenti campi :'
    print 'NUMERO CAMPI POSSIBILI = ',n_campi
    print campi                   # solo in test, poi eliminare
    print def_campi               # solo in test, poi eliminare
    i=0
    while i<n_campi:
        print
        print 'Campo [',i+1,']'
        j=0
        while j<5:                # perché i campi successivi al quinto servono al sw per creare le triple e non sono utili all'utente
            print def_campi[j],' -> ',campi[(j*n_campi)+i]
            j=j+1
        i=i+1

    return


# FUNZIONE PER LA RICERCA DEGLI OGGETTI SU OPENDATA ESTERNI A SECONDA DEL PARAMETRO PASSATO
# in lavorazione ............................ da togliere ???????
def cerca_istanza(stringa_da_cercare,ind_corrispondenza):
    print'---------------------------'
    print 'funzione: cerca_istanza'
    print stringa_da_cercare
    print ind_corrispondenza
    print'---------------------------'
    stringa_opendata=stringa_da_cercare
    return stringa_opendata

def calcola_hash(stringa):
    c_hash=hashlib.sha224(stringa).hexdigest()
    return c_hash





###################################################################################################################################
#                           FINE FUNZIONI , INIZIO PROGRAMMA PRINCIPALE                                                           #
###################################################################################################################################

## 1 ## INPUT DEI NOMI DEI FILE : ## 1 ##

#   nomeFileDati E' IL FILE CON IL CSV DA TRASFORMARE IN TRIPLE
#   separatore E' IL CARATTERE SEPARATORE USATO NEL CSV
#   intestazione CI DICE SE IL CSV HA LA PRIMA RIGA CON I NOMI DEI CAMPI ('s') OPPURE NO ('n')
#   nomeFileConfig E' IL FILE CSV CONTENENTE LE INFORMAZIONI STANDARDIZZATE PER LA GENERAZIONE DELLE TRIPLE
#   nomeFileDef E' IL FILE DI TESTO CONTENENTE LE DEFINIZIONI DA INSERIRE TRA I PREFIX E LE TRIPLE

nomeFileDati = raw_input("Inserire il nome del file CSV contenente i dati : ")
nomeFileDati='civici_torino_ridotto_n.csv'
nomeFileDati='immobili_torino_part_n.csv'
separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabilazione) : ")
separatore=';'
if separatore=="TAB":
    separatore='\t'
stringa="La prima riga del file "+nomeFileDati+" e' una riga di intestazione dei campi (s/n) ? "
intestazione=raw_input(stringa)
intestazione='s'

nomeFileConfig = raw_input("Inserire il nome del file di configurazione da aprire : ")
nomeFileConfig='configurazione_civici.csv'
nomeFileConfig='configurazione_immobili.csv'
leggi_configurazione(nomeFileConfig)


## 2 ## ABBINAMENTO CAMPI FILE CSV CON FILE DI CONFIGURAZIONE ## 2 ##
print
print 'Per ogni tipo di dato presente nel proprio CSV indicare il numero corrispondente al campo tra quelli proposti. Il numero è indicato tra parentesi quadre [].'
print 'Se il dato nel proprio CSV non esiste inserire 0.'
corrispondenza=[]
corrispondenza=['0', '12', '0', '0', '5', '4', '1', '2', '6', '7', '8', '9', '10', '11', '3']    # poi da togliere e da scommentare la riga successiva
corrispondenza=['0', '0', '4', '0', '0', '0', '13', '19', '17', '18', '21', '22', '23', '24', '5', '6', '7', '11', '14', '3', '2']
with open(nomeFileDati, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = separatore)
       n_record=0                          # n_record conterrà il numero di record da elaborare
       for row in reader:
           n_record=n_record+1
           n_campi=len(row)                # n_campi conterrà il numero di tipi di dati nel CSV da elaborare
           i=0
           if n_record==1:
               i=0
               print 'Il record e composto da ', len(row), 'campi :'
               while i<n_campi:
                   stringa_input=row[i]+' corrisponde al campo nr? '
                   #v = raw_input(stringa_input)          # da scommentare
                   #corrispondenza.append(v)              # da scommentare
                   i=i+1
csvfile.close()
print 'Il file contiene ', n_record, ' record'
print corrispondenza    # solo in test, poi eliminare

#LEGGE IL FILE DI CONFIGURAZIONE E POPOLA LA LISTA campi, PEZZO DI CODICE GIA' PRESENTE NELLA FUNZIONE leggi_configurazione. VALUTARE SE PASSARE LA LISTA campi per riferimento
campi = []
with open(nomeFileConfig, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ',')
       n_righe=0
       for row in reader:
            n_righe=n_righe+1
            n_campi_config=len(row)
            i = 0
            while i < n_campi_config:
                campi.append(row[i])
                i = i + 1
csvfile.close()


print '-------------------------------------------------------------------------------------------'

# CREO IL LOD

#nome_lod=raw_input('Quale nome vuoi per il tuo LOD: ')    # da scommentare
#nome_lod=nome_lod+'.ttl'                                  # da scommentare
nomeFileLod=raw_input('Quale nome vuoi per il tuo LOD: ')
nomeFileLod=nomeFileLod+'.ttl'
try:
    f_lod = open(nomeFileLod, 'wb')
except:
    print 'Non è possibile aprire in scrittura il file ',nomeFileLod


#LEGGE IL FILE IN CUI E' DESCRITTA LA STRUTTURA DEL LOD
nomeFileStruct = raw_input("Inserire il nome del filecontenente la struttura del Linked Data : ")
nomeFileStruct='struttura_civici.txt'
nomeFileStruct='struttura_immobili.txt'
try:
    f_struct = open (nomeFileStruct,'r')
except:
    print 'File contenente la struttura del linked data non trovato.'

riga=f_struct.readline()
i=1
while riga:
    riga=riga.rstrip()
    if i==1:        # prima riga contenente il tipo di dato principale
        tipoOggetto = riga
        print "tipoOggetto =(",tipoOggetto,")"
        print "-------------------------------"
    if i == 2:  # seconda riga contenente il prefisso del soggetto
        prefSoggetto = riga
        if prefSoggetto<>"null":
            prefSoggetto=prefSoggetto+":"
    if i==3:        # terza riga contenente soggetto e predicato ove l'oggetto è il tipo di dato principale
        soggPred = riga
    riga = f_struct.readline()
    i=i+1

f_struct.close()

#spazio_dati=raw_input('Inserisci il link relativo al tuo spazio dati (es. http://miospazio.org/:) , se non lo siconosce inserire la voce -none- ')   # da scommentare
spazio_dati='none'


print 'Sto copiando i prefissi ...'


f_lod.write("###################################################\n")
f_lod.write("############          PREFISSI         ############\n")
f_lod.write("###################################################\n")
spazio_dati='@prefix myspace: <'+spazio_dati+'>\n'

f_lod.write(spazio_dati)   # da scommentare

# legge tutti i prefix nel file con i prefissi
nomeFilePrefissi = raw_input("Inserire il nome del file di testo contenente i prefissi : ")
nomeFilePrefissi='prefissi_civici.txt'
nomeFilePrefissi='prefissi_immobili.txt'
try:
    f_pref = open (nomeFilePrefissi,'r')
except:
    print 'File contenente i prefissi non trovato.'

def_campi=[]
# LEGGIAMO IL FILE CON IL NOME DEI TIPI DI CAMPO CERCANDO DOVE E' PRESENTE prefix ALL'INIZIO
riga=f_pref.readline()
i=0

while riga:
    riga=riga.rstrip()+'\n'
    # print riga
    f_lod.write(riga)
    riga = f_pref.readline()
f_pref.close()

print 'Sto copiando le definizioni ...'
f_lod.write('\n')
f_lod.write("###################################################\n")
f_lod.write("############        DEFINIZIONI        ############\n")
f_lod.write("###################################################\n")

#f.write(spazio_dati)   # da scommentare

# legge tutte le definizioni nel file con le definizioni
nomeFileDef = raw_input("Inserire il nome del file di testo contenente le definizioni : ")
nomeFileDef='definizioni_civici.txt'
nomeFileDef='definizioni_immobili.txt'
try:
    f_def = open (nomeFileDef,'r')
except:
    print 'File contenente le definizioni non trovato.'

# LEGGIAMO IL FILE CON IL NOME DEI TIPI DI CAMPO CERCANDO DOVE E' PRESENTE prefix ALL'INIZIO
riga=f_def.readline()

while riga:
    riga=riga.rstrip()+'\n'
    # print riga
    f_lod.write(riga)
    riga = f_def.readline()
f_def.close()

print 'Sto creando le triple ...'
f_lod.write('\n')
f_lod.write("###################################################\n")
f_lod.write("############           TRIPLE          ############\n")
f_lod.write("###################################################\n")


### Parte di programma che carica in due liste lod_property e lod_object i valori utili alla creazione delle triple

#print corrispondenza, 'numero campi nel file di configurazione =', n_campi_config
#print 'numero campi nel file dati =', n_campi

i=0
lod_property=[]     # Lista contenente le proprietà del LOD
lod_object=[]
while i<n_campi_config:
    property=campi[i + (n_campi_config * 5)]
    if property[:1] == '_':
        property=property.replace('_','myspace')
    lod_property.append(property)

    object=campi[i + (n_campi_config * 6)]
    if object[-5:] <> '<uri>':
        object = '^^xsd:' + object
    lod_object.append(object)
    i=i+1

# Parte di programma che genera le triple

# print lod_property
# print lod_object
# sys.exit(0)

with open(nomeFileDati, 'rb') as f_dati:
    reader = csv.reader(f_dati, delimiter=separatore)
    riga = 0
    for row in reader:
        f_lod.write('\n')
        stringa_x_hash =''
        i=0
        while i < n_campi:
            stringa_x_hash=stringa_x_hash+row[i]
            i = i + 1
        nodo = calcola_hash(stringa_x_hash)
        if prefSoggetto == "null":
            stringaWrite = nodo + '  a ' + tipoOggetto + ' ;\n'
        else:
            stringaWrite=prefSoggetto+nodo+'  a '+tipoOggetto+' ;\n'
        # print nodo

        riga = riga + 1
        if riga > 1 or intestazione=='n':
            if tipoOggetto <> "null":
                f_lod.write(stringaWrite)  # scrive il tipo del nodo
            i = 0
            #print
            #print 'elaborazione riga dati numero :',riga,'/',n_record
            prima_riga=1
            while i < n_campi:
                j=int(corrispondenza[i])
                if j<>0 and row[i]<>"":
                    object=lod_object[j-1]
                    #print lod_object
                    #print object
                    if object[-5:] == '<uri>':
                        #object=' '+object[:-5]+'"'+cerca_istanza(row[i],campi[n_campi_config*9+(j-1)])+'"'   # Se nel csv il tipo di oggetto è una URI occorre andare a cercare la corrispondenza
                        object=' '+object[:-5]+'"'+row[i]+'"'
                    else:
                        object=' "'+row[i]+'"'+lod_object[j-1]
                    stringa_lod = lod_property[j - 1] + object + " ;\n"
                    # print stringa_lod
                    print "prima_riga=",prima_riga,"   tipoOggetto=(",tipoOggetto,")"
                    if tipoOggetto == "null" and prima_riga==1:
                        print "prefSoggetto=",prefSoggetto
                        if prefSoggetto=="null":
                            stringa_lod = nodo + "  " + stringa_lod
                        else:
                            stringa_lod=prefSoggetto + nodo+"  "+stringa_lod
                    else:
                        stringa_lod='                                                          ' +stringa_lod
                    if prima_riga==1:
                        prima_riga=0
                    f_lod.write(stringa_lod)
                i = i + 1
            if soggPred <> "null":
                f_lod.write(soggPred + "  " + prefSoggetto + nodo+" .\n")
f_dati.close()
f_lod.close()