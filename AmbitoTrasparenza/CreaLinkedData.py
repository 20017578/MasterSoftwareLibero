#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import sys
import csv
import string
import hashlib
import operator

def crea_tripla_tipo (soggetto,tipo):
    tripla=''
    if tipo <> 'null':
        tripla = soggetto+'  a  ' + tipo+" ."
    return tripla

def crea_tripla_uri_interno (soggetto,predicato,listaOggetti):
    triple=[]
    j = 0
    for oggetto in listaOggetti:
        if j == 0:
            tripla=soggetto+'  '+predicato+'  _:'+oggetto+' ,'
            nSpazi=len(soggetto)+2+len(predicato)+2
        else:
            tripla='_:'+oggetto
            tripla = aggiungi_spazi(nSpazi) + tripla+' ,'
        triple.append(tripla)
        j = j + 1
    j = len(triple)
    if j > 0:
        ultimaTripla = triple[j - 1]
        triple[j - 1] = ultimaTripla[:-1] + '.'
    return triple

def crea_triple(prefSoggetto,soggetto,listaProprieta,corrispondenzeProprieta,listaOggetti,fileTabella,separatore,intestazione):
    triple=[]
    with open(fileTabella, 'rb') as f_dati:
        reader = csv.reader(f_dati, delimiter=separatore)
        riga = 0
        for row in reader:
            riga = riga + 1
            if riga > 1 or intestazione == 'n':
                i = 0
                prima_riga = 1
                while i < len(row):
                    j = int(corrispondenzeProprieta[i+1])   # perché in corrispondenzeProprietà[0] c'è l'indice del soggetto
                    if j <> 0 and row[i] <> "" and row[int(corrispondenzeProprieta[0])]==soggetto:
                        object = listaOggetti[j - 1]
                        # print lod_object
                        # print object
                        if object[-5:] == '<uri>':
                            # object=' '+object[:-5]+'"'+cerca_istanza(row[i],campi[n_campi_config*9+(j-1)])+'"'   # Se nel csv il tipo di oggetto è una URI occorre andare a cercare la corrispondenza
                            object = ' ' + object[:-5] + '"' + row[i] + '"'
                        else:
                            object = ' "' + row[i] + '"' + listaOggetti[j - 1]
                        tripla = listaProprieta[j - 1] + object+ ' ;'
                        if prima_riga == 1:
                            tripla = prefSoggetto+soggetto + '  ' + tripla
                            nSpazi = len(prefSoggetto+soggetto)+2
                            prima_riga = 0
                        else :
                            tripla = aggiungi_spazi(nSpazi)+tripla
                        triple.append(tripla)
                    i = i + 1
                #if soggPred <> "null":
                    #f_lod.write(soggPred + "  " + prefSoggetto + nodo + " .\n")
    i=len(triple)
    if i>0:
        ultimaTripla=triple[i-1]
        triple[i - 1]=ultimaTripla[:-1]+'.'
    f_dati.close()
    return triple

def aggiungi_spazi(ns):
    s=''
    i=0
    while i<ns:
        s=s+' '
        i=i+1
    return s

def ordina_csv(f_name,separatore,intestazione,colonna):    #DELETE
    file_csv=open(f_name,'rb')
    data=csv.reader(file_csv,delimiter=separatore)
    print data
    sortedlist=sorted(data,key=operator.itemgetter(int(colonna)))
    f_name='sorted_'+f_name
    with open(f_name,'wb') as f:
        f_write=csv.writer(f,delimiter=separatore)
        for row in sortedlist:
            f_write.writerow(row)
    return

def occorrenzeFiglia(id,tabFigliaName,separatore,colonnaFiglia):
    file_csv = open(tabFigliaName, 'rb')
    reader = csv.reader(file_csv, delimiter=separatore)
    n_occ=0
    for row in reader:
        v=row[int(colonnaFiglia)]
        if v==id:
            n_occ=n_occ+1
    file_csv.close()

    return n_occ

def occorrenzeMe(nomeFileCSV,separatore,colonnaSoggetto,colonnaOggetto,soggetto):
    lista=[]
    with open(nomeFileCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=separatore)
        n_occ=0
        for row in reader:
            s=row[int(colonnaSoggetto)]
            # print 's =',s,'  soggetto =',soggetto
            if s==soggetto:
                n_occ=n_occ+1
                lista.append(row[int(colonnaOggetto)])

    return lista


def cerca_corrispondenze(nomeFileCSV,separatore,fileConfig):
    leggi_configurazione(fileConfig)
    lista=[]
    with open(nomeFileCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=separatore)
        n_record = 0  # n_record conterrà il numero di record da elaborare
        for row in reader:
            n_record = n_record + 1
            n_campi = len(row)  # n_campi conterrà il numero di tipi di dati nel CSV da elaborare
            if n_record == 1:
                i = 0
                print 'Il record e composto da ', len(row), 'campi :'
                while i < n_campi:
                    print i,': ',row[i]
                    i = i + 1
                soggetto=raw_input('Il soggetto è presente nel campo nr? ')
                lista.append(soggetto)
                i = 0
                while i < n_campi:
                    stringa_input = row[i] + ' corrisponde al campo nr? '
                    v = raw_input(stringa_input)          # da scommentare
                    lista.append(v)              # da scommentare
                    i = i + 1
    csvfile.close()
    print 'Il file contiene ', n_record, ' record'
    return lista


# FUNZIONE CHE LEGGE I FILE DI CONFIGURAZIONE UTILI ALLA GENERAZIONE DELLE TRIPLE
def leggi_configurazione(nomeFileConfig):

    # LEGGO IL FILE campi_config CHE CONTIENE IL NOME DEI DIVERSI RECORD PRESENTI NEI FILE
    #  DI CONFIGURAZIONE, le prime 10 righe servono a descrivere il nodo e non proprietà ed oggetti
    try:
        f_nomiConfig = open ('campi_config.txt')
    except:
        print 'File non trovato.'
        sys.exit(1)
    def_campi=[]                             # def_campi contiene i nomi
    riga=f_nomiConfig.readline().rstrip()    # rstrip elimina il carattere /n a fine riga
    while riga:
        def_campi.append(riga)
        riga = f_nomiConfig.readline()
    f_nomiConfig.close()

    # LEGGO IL FILE CONTENENTE LA CONFIGURAZIONE SPECIFICA PER IL TIPO DI DATO CHE STO ELABORANDO, QUESTO SARA' MODELLATO
    #  SEMPRE NELLO STESSO MODO ED OGNI RIGA (RECORD) SARA' RIFERITO AL TITOLO ESTRATTO COL FILE campi_config PRECEDENTE
    campi = []                                     # campi i valori utili alla produzione delle triple
    with open(nomeFileConfig, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ';')   # funzione per leggere un csv splittandolo a seconda del carattere delimitatore, funziona meglio della funzione split limitata alle stringhe in quanto riconosce i campi di testo racchiusi tra virgolette
       for row in reader:
           n_campi=len(row)
           i = 0
           while i<n_campi:
                campi.append(row[i])          # campi conterrà tutti i dati in sequenza, prima la quelli della riga 11, poi la 12 e così via
                i = i + 1
    csvfile.close()

    # SCRIVO I DATI UTILI CIRCA I POSSIBILI CAMPI (OVVERO LE PROPRIETA') DELLE TRIPLE
    print 'Il LOD da produrre potrà avere i seguenti campi :'
    # print 'NUMERO CAMPI POSSIBILI = ',n_campi
    # print campi                   # solo in test, poi eliminare
    # print def_campi               # solo in test, poi eliminare
    i=0
    while i<n_campi:
        print 'Campo [',i+1,'] -> ',campi[i]
        i=i+1

    return


# FUNZIONE PER LA RICERCA DEGLI OGGETTI SU OPENDATA ESTERNI A SECONDA DEL PARAMETRO PASSATO
# in lavorazione ............................ da togliere ???????
def cerca_istanza(stringa_da_cercare,ind_corrispondenza):    #DELETE
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

myspace='my_ld'
# INPUT: quale Linked Data voglio creare ?
print "Software per la generazione di Linked Data (in linguaggio turtle) partendo da file CSV per le seguenti tipologie :"
print "1) Numeri civici"
print "2) Indice di tempestività dei pagamenti (dlgs. 33/2013 art. xx)"
print "3) Immobili posseduti e affittati da una PA (dlgs. 33/2013 art. xx)"
print "-------------------------------------------------------------------------------------------"
tipoLOD=0
while tipoLOD<'1' or tipoLOD>'3':
    tipoLOD = raw_input("Quale linked-data vuoi creare (1/3) ? ")
    if tipoLOD<'1' or tipoLOD>'3':
        print "!ATTENZIONE! Valore inserito non corretto"
if tipoLOD=='1':
    suffisso_file='civici'
    prefissoSoggetto=''
    profondita = 0     # rimettere a 1
if tipoLOD=='2':
    suffisso_file='indice_pag'
    prefissoSoggetto='spcdata:'
    profondita = 2
if tipoLOD=='3':
    suffisso_file='immobili'
    prefissoSoggetto='spcdata:'
    profondita = 0     # rimettere a 3

nomeFileConfig = 'configurazione_'+suffisso_file+'.csv'
nomeFileStruct = 'struttura_'+suffisso_file+'.txt'
nomeFilePrefissi = 'prefissi_'+suffisso_file+'.txt'
nomeFileDef = 'definizioni_'+suffisso_file+'.txt'

tupla_cardinali='zero','prima','seconda','terza','quarta','quinta','sesta','settima','ottava','nona','decima'
lista_tabelle=[]
i=0

try:
    f_struct = open (nomeFileStruct,'r')
except:
    print 'File contenente la struttura del linked data (',nomeFileStruct,') non trovato.'
    sys.exit(1)

corrispondenza=[['null']]
while i<profondita:
    lista=[]
    nomeFile = raw_input("Inserire il nome del file CSV contenente i dati della "+tupla_cardinali[i+1]+" tabella (file CSV): ")
    if i>0:
        lista_tabelle[i-1][7]=nomeFile
    separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabulazione) : ")
    separatore = ';'                      #TOGLIERE
    if separatore == "TAB":
        separatore = '\t'
    stringa = "La prima riga del file " + nomeFile + " e' una riga di intestazione dei campi (s/n) ? "
    intestazione = raw_input(stringa)
    intestazione = 's'                      #TOGLIERE
    with open(nomeFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=separatore)
        n_record = 0                                    # n_record conterrà il numero di record da elaborare
        for row in reader:
            n_record = n_record + 1
            n_campi = len(row)                      # n_campi conterrà il numero di tipi di dati nel CSV da elaborare
            if n_record == 1:
                j = 0
                print 'Il record e composto da ', len(row), 'campi :'
                while j < n_campi:
                    print "Campo n.",j," : ",row[j]
                    j = j + 1
    csvfile.close()
    idTabella=''
    idTabella2=''
    if profondita>i+1:
        idTabella = raw_input("Qual è il campo con gli identificativi (tipo chiave primaria) di questa tabella che riferiscono alla tabella figlia, se esistente ? ")
    if i>0:
        idTabella2 = raw_input("Qual è il campo con gli identificativi che riferiscono alla tabella padre ? ")

    tipo = f_struct.readline().rstrip()
    predicato = f_struct.readline().rstrip()

    lista.append(nomeFile)
    lista.append(separatore)
    lista.append(intestazione)
    lista.append(tipo)
    lista.append(idTabella)
    lista.append(idTabella2)
    lista.append(predicato)
    lista.append('')           # non conosco ancora il nome della tabella 'figlia'
    lista.append(i+1)
    lista_tabelle.append(lista)

    print
    print 'Per ogni tipo di dato presente nel proprio CSV indicare il numero corrispondente al campo tra quelli proposti.'
    print '     Il numero è indicato tra parentesi quadre [].'
    print "Il campo da indicare è l'oggetto della tripla (NON il soggetto)"
    print 'Se il dato nel proprio CSV non esiste, o se esso è un identificativo usato come soggetto, inserire il valore 0 (zero).'
    c=cerca_corrispondenze(nomeFile,separatore,nomeFileConfig)             #SCOMMENTARE
    corrispondenza.append(c)                                            #SCOMMENTARE
    i=i+1

f_struct.close()

#print"Lista tabelle :"
#print lista_tabelle

#print"corrispondenza :"
#print corrispondenza

if tipoLOD=='1':
    corrispondenza=[['null'],['1', '0', '0', '0', '0', '5', '4', '1', '2', '6', '7', '8', '9', '10', '11', '3']]
    lista_tabelle=[['civici_torino_ridotto_n.csv', ';', 's', 'locn:Address', '', '', 'null', '', 1]]
    profondita=1
if tipoLOD=='x':
    lista_tabelle=[['indice_temp_1_n.csv', ';', 's', 'http://spcdata.digitpa.gov.it/Amministrazione/', '1', '', 'my_ld:ha_indice_di_tempestivita_dei_pagamenti', 'indice_temp_2.csv', 1], ['indice_temp_2.csv', ';', 's', 'null', '', '0', 'null', '', 2]]
    corrispondenza =[['null'], ['2', '0', '0', '0'], ['0', '0', '1', '2', '3', '4']]
    profondita=2
if tipoLOD=='3':
    corrispondenza=[['null'],['2', '0', '0', '0'],['0', '0', '0', '0', '0', '2', '9', '10', '5', '6', '7', '8', '13', '0', '11', '14'],['1', '0', '0', '22', '23', '17', '18', '19']]
    lista_tabelle=[['reg1_n.csv', ';', 's', 'http://spcdata.digitpa.gov.it/Amministrazione/', '1', '', 'my_ld:possiede_affitta', 'reg2.csv', 1], ['reg2.csv', ';', 's', 'null', '1', '0', 'my_ld:affitta', 'reg3.csv', 2], ['reg3.csv', ';', 's', 'null', '', '0', 'null', '', 3]]
    profondita=3
#print "La lista è formata così: "
#print "0- nome della tabella (CSV)"
#print "1- separatore del CSV"
#print "2- il CSV ha una intestazione (s/n) ?"
#print "3- tipo del soggetto: id a ......"
#print "4- Numero del campo contenente gli id che linkano alla tabella figlia"
#print "5- Numero del campo contenente gli id che linkano alla tabella padre"
#print "6- Predicato col quale si legano le due tabelle: id1 predicato id2"
#print "7- Nome della tabella figlia"
#print "8- Livello di profondità"


#LEGGE IL FILE DI CONFIGURAZIONE E POPOLA LA LISTA campi, PEZZO DI CODICE GIA' PRESENTE NELLA FUNZIONE leggi_configurazione. VALUTARE SE PASSARE LA LISTA campi per riferimento
campi = []
with open(nomeFileConfig, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ';')
       n_righe=0
       for row in reader:
            n_righe=n_righe+1
            n_campi_config=len(row)
            i = 0
            while i < n_campi_config:
                campi.append(row[i])
                i = i + 1
csvfile.close()
i=0
lod_property=[]     # Lista contenente le proprietà del LOD
lod_object=[]
while i<n_campi_config:
    property=campi[i + (n_campi_config * 5)]
    if property[:1] == '_':
        property=property.replace('_',myspace)
    lod_property.append(property)

    object=campi[i + (n_campi_config * 6)]
    if object[-5:] <> '<uri>':
        object = '^^xsd:' + object
    lod_object.append(object)
    i=i+1
#print campi
#print lod_property
#print lod_object

#####################################################################################################################################
#                                                                                                                                   #
#            RICHIESTA DELLA URL DELLO SPAZIO DATI E DEL NOME DEL FILE FINALE PER IL LINKED DATA                                    #
#                                                                                                                                   #
#####################################################################################################################################

print "Inserisci l'url del tuo spazio dati (p.e.: http://spcdata.digitpa.gov.it/)"
spazioDati = raw_input("    se non lo conosci premi Enter e prosegui :")
if spazioDati=='':
    spazioDati='none'
spazioDati='@prefix '+myspace+': <'+spazioDati+'>  .\n'

nomeFileLOD = raw_input("Inserisci il nome del file per il Linked Data (senza estensione) :")
nomeFileLOD=nomeFileLOD+'.ttl'
try:
    f_lod = open(nomeFileLOD, 'wb')
except:
    print 'Non è possibile aprire in scrittura il file ',nomeFileLOD
    sys.exit(1)

#####################################################################################################################################
#                                                                                                                                   #
#            SCRITTURA SUL FILE DEL LINKED DATA DI PREFISSI E DEFINIZIONI                                                           #
#                                                                                                                                   #
#####################################################################################################################################

try:
    f_pref = open (nomeFilePrefissi,'r')
except:
    print 'File contenente i prefissi (',nomeFilePrefissi,') non trovato.'
    sys.exit(1)

print 'Sto scrivendo i prefissi ...'
riga=f_pref.readline()
i=0
while riga:
    riga=riga.rstrip()+'\n'
    f_lod.write(riga)
    riga = f_pref.readline()
f_lod.write(spazioDati)
f_pref.close()

print 'Termine scrittura dei prefissi.'
print 'Sto scrivendo le definizioni ...'

try:
    f_def = open (nomeFileDef,'r')
except:
    print 'File contenente le definizioni (',nomeFileDef,') non trovato.'
    sys.exit(1)

f_lod.write('\n')
riga=f_def.readline()
while riga:
    riga=riga.rstrip()+'\n'
    # print riga
    f_lod.write(riga)
    riga = f_def.readline()
f_def.close()

print 'Termine scrittura delle definizioni.'
f_lod.write('\n')


#####################################################################################################################################
#                                                                                                                                   #
#            INIZIO CALCOLO DELLE TRIPLE                                                                                            #
#                                                                                                                                   #
#####################################################################################################################################

f_lod.write('\n')
f_lod.write('# DATI')
f_lod.write('\n')

print
print "Inizio l'elaborazione delle triple ..."
i=1
while i<=profondita:
    if i>1:
        prefissoSoggetto='_:'
    print'----------------------------------------------------------------'
    print "ELABORAZIONE TABELLA nr.",i,' :',lista_tabelle [i-1][0]
    print'----------------------------------------------------------------'
    with open(lista_tabelle [i-1][0], 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=lista_tabelle [i-1][1])
        r = 0
        listaSoggetti=[]
        for row in reader:
            #print row
            if lista_tabelle[i - 1][2] <> 's' or r > 0:
                soggetto = prefissoSoggetto + row[int(corrispondenza[i][0])]
                #print "Analizzo il soggetto: ",soggetto
                if soggetto not in listaSoggetti:
                    #print 'Elaboro il soggetto: ',soggetto
                    f_lod.write('\n')
                    listaSoggetti.append(soggetto)

                    t=crea_tripla_tipo(soggetto,lista_tabelle[i-1][3])    # crea tripla del tipo
                    if t<>'':
                        t=t+'\n'
                        f_lod.write(t)
                    #print 'TRIPLA TIPO : ',t

                    if profondita>i:
                        meOggetti = []
                        meOggetti = occorrenzeMe(lista_tabelle[i-1][0],lista_tabelle[i-1][1], corrispondenza[i][0],int(lista_tabelle[i - 1][4]), row[int(corrispondenza[i][0])])
                        #print soggetto, " ha i seguenti oggetti =", len(occMeOggetti), occMeOggetti
                        occFiglia = occorrenzeFiglia(row[int(lista_tabelle[i - 1][4])], lista_tabelle[i][0],lista_tabelle[i][1], lista_tabelle[i][5])  # cerca nella tabella figlia quante occorrenze esistono dell'oggetto
                        #print row[int(lista_tabelle[i - 1][4])], " - occorrenze =", occFiglia
                        listaTripleUri=[]
                        if occFiglia>0:
                            listaTripleUri=crea_tripla_uri_interno(soggetto,lista_tabelle[i-1][6],meOggetti)   # crea triple che riportano legami con tabella figlia
                            for tripla in listaTripleUri:
                                tripla=tripla+'\n'
                                f_lod.write(tripla)

                    listaTripleInterne = []
                    listaTripleInterne = crea_triple(prefissoSoggetto , row[int(corrispondenza[i][0])],lod_property,corrispondenza[i],lod_object,lista_tabelle[i-1][0],lista_tabelle[i-1][1],lista_tabelle[i-1][2])
                    for tripla in listaTripleInterne:
                        tripla = tripla + '\n'
                        f_lod.write(tripla)
            r=r+1
    csvfile.close()
    i=i+1

print 'Termine scrittura delle triple.'
f_lod.close()
