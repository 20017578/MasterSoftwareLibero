#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import sys
import csv
import string


# FUNZIONE CHE LEGGE I FILE DI CONFIGURAZIONE UTILI ALLA GENERAZIONE DELLE TRIPLE
def leggi_configurazione(nomeFileConfig):
    
    # LEGGO IL FILE campi_config CHE CONTIENE IL NOME DEI DIVERSI RECORD PRESENTI NEI FILE
    #  DI CONFIGURAZIONE, le prime 10 righe servono a descrivere il nodo e non proprietà ed oggetti
    try:
        file_csv_config_main = open ('campi_config.csv')
    except:
        print 'File non trovato, provo da rete.'
    def_campi=[]                             # def_campi contiene i nomi
    riga_csv=file_csv_config_main.readline()
    i=0
    while riga_csv:
        riga_csv=riga_csv.rstrip()           # rstrip elimina il carattere /n a fine riga
        if i>=10:
            def_campi.append(riga_csv)
        i=i+1
        riga_csv = file_csv_config_main.readline()
    file_csv_config_main.close()

    # LEGGO IL FILE CONTENENTE LA CONFIGURAZIONE SPECIFICA PER IL TIPO DI DATO CHE STO ELABORANDO, QUESTO SARA' MODELLATO
    #  SEMPRE NELLO STESSO MODO ED OGNI RIGA (RECORD) SARA' RIFERITO AL TITOLO ESTRATTO COL FILE campi_config PRECEDENTE
    campi = []                                     # campi i valori utili alla produzione delle triple
    with open(nomeFileConfig, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ',')   # funzione per leggere un csv splittandolo a seconda del carattere delimitatore, funziona meglio della funzione split limitata alle stringhe in quanto riconosce i campi di testo racchiusi tra virgolette
       n=0
       for row in reader:
           n=n+1
           n_campi=len(row)
           if n>9:                                # perché dopo la riga 10 ci sono i campi con le informazioni di proprietà e oggetti
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
# in lavorazione ............................
def cerca_istanza(stringa_da_cercare,ind_corrispondenza):
    print'---------------------------'
    print 'funzione: cerca_istanza'
    print stringa_da_cercare
    print ind_corrispondenza
    print'---------------------------'
    stringa_opendata=stringa_da_cercare
    return stringa_opendata

################################################################################################################
#        FINE FUNZIONI , INIZIO PROGRAMMA PRINCIPALE                                                           #
################################################################################################################


# INPUT DEI NOMI DEI FILE :
#   nomeFileDati E' IL FILE CON IL CSV DA TRASFORMARE IN TRIPLE
#   separatore E' IL CARATTERE SEPARATORE USATO NEL CSV
#   intestazione CI DICE SE IL CSV HA LA PRIMA RIGA CON I NOMI DEI CAMPI ('s') OPPURE NO ('n')
#   nomeFileConfig E' IL FILE CSV CONTENENTE LE INFORMAZIONI STANDARDIZZATE PER LA GENERAZIONE DELLE TRIPLE

# nomeFileDati = raw_input("Inserire il nome del file da aprire : ")
nomeFileDati='civici_torino.csv'
# separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabilazione) : ")
separatore=';'
if separatore=="TAB":
    separatore='\t'
# intestazione=raw_input("La prima riga del file ",nomeFileDati," e' una riga di intestazione dei campi (s/n) ? ")
intestazione='s'
# nomeFileConfig = raw_input("Inserire il nome del file di configurazione da aprire : ")
nomeFileConfig='config_toponomastica.csv'

leggi_configurazione(nomeFileConfig)

# ABBINAMENTO CAMPI FILE CSV CON FILE DI CONFIGURAZIONE
print
print 'Per ogni tipo di dato presente nel proprio CSV indicare il numero corrispondente al campo tra quelli proposti. Il numero è indicato tra parentesi quadre [].'
print 'Se il dato nel proprio CSV non esiste inserire 0.'
corrispondenza=['12', '3', '5', '0', '4', '1', '2']    # poi da togliere e da scommentare la riga successiva
#corrispondenza=[]                                     
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
           if n_righe > 9:
                i = 0
                while i < n_campi_config:
                    campi.append(row[i])
                    i = i + 1
csvfile.close()


print '-------------------------------------------------------------------------------------------'

# CREO IL LOD

#nome_lod=raw_input('Quale nome vuoi per il tuo LOD: ')    # da scommentare
#nome_lod=nome_lod+'.ttl'                                  # da scommentare
#spazio_dati=raw_input('Inserisci il link relativo al tuo spazio dati (es. http://miospazio.org/: ')   # da scommentare
spazio_dati="http://miospazio.it"            # solo in test, poi eliminare

print
print '############################'
print '###         LOD          ###'
print '############################'
spazio_dati='@prefix myspace:<'+spazio_dati+'>'
#f=open(nome_lod,'w')   # da scommentare
#f.write(spazio_dati)   # da scommentare
print spazio_dati
# legge tutti i prefix possibili presenti nel file di configurazione
try:
    file_config_main = open ('campi_config.csv')
except:
    print 'File non trovato, provo da rete.'

def_campi=[]
# LEGGIAMO IL FILE CON IL NOME DEI TIPI DI CAMPO CERCANDO DOVE E' PRESENTE prefix ALL'INIZIO
riga_csv=file_config_main.readline()
i=0
prefisso=[]
while riga_csv:
    riga_csv=riga_csv.rstrip()
    if riga_csv[:6]=='prefix':
        j=0
        while j<n_campi_config:
            #print i,'.',campi[n_campi_config*i+j]
            #print campi[n_campi_config*(i-1)+j]
            p = campi[n_campi_config*(i-11)+j].split(':')
            if campi[n_campi_config*(i-10)+j]<>"":
                prefisso.append('@prefix '+p[0]+': <'+campi[n_campi_config*(i-10)+j]+'>')
            j=j+1
    i=i+1
    riga_csv = file_config_main.readline()
prefisso.sort()
p_precedente=""
for p in prefisso:
    if p<>p_precedente:
        print p
        #f.write(p)
    p_precedente=p
file_config_main.close()

print corrispondenza, 'numero campi nel file di configurazione =', n_campi_config
print 'numero campi nel file dati =', n_campi
print"####################"
i=0
lod_property=[]
lod_object=[]
while i<n_campi_config:
    property=campi[i + (n_campi_config * 5)]
    if property[:1] == '_':
        property=property.replace('_','myspace')
    lod_property.append(property)
    object=campi[i + (n_campi_config * 7)]
    #if object[-5:] == '<uri>':
       #object=object[:-5]
    #else:
        #object='^^xsd:'+object
    lod_object.append(object)
    i=i+1

# Se il csv dati contiene un campo intestazione lo elimino dai dati

print lod_property
print lod_object

with open(nomeFileDati, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=separatore)
    riga = 0
    for row in reader:
        print row
        riga = riga + 1
        if n_righe <> 1 or intestazione=='n':
            i = 0
            print
            print 'elaborazione riga dati numero :',riga,'/',n_record
            while i < n_campi:
                j=int(corrispondenza[i])
                if j<>0:
                    object=lod_object[j-1]
                    if object[-5:] == '<uri>':
                        object=' '+object[:-5]+'"'+cerca_istanza(row[i],campi[n_campi_config*9+(j-1)])+'"'   # Se nel csv il tipo di oggetto è una URI occorre andare a cercare la corrispondenza
                    else:
                        object=' "'+row[i]+'"^^'+lod_object[j-1]
                    stringa_lod=lod_property[j-1]+object
                    print stringa_lod
                i = i + 1
        if riga==10:
            break
csvfile.close()










#f.close()
