import urllib
import sys
import csv
import string


# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def leggi_configurazione():

    # LEGGIAMO IL FILE CON IL NOME DEI TIPI DI CAMPO (Attenzione le prime 10 righe descrivono il nodo e non il campo
    try:
        file_csv_config_main = open ('campi_config.csv')
    except:
        print 'File non trovato, provo da rete.'
    def_campi=[]
    riga_csv=file_csv_config_main.readline()
    i=0
    while riga_csv:
        riga_csv=riga_csv.rstrip()
        if i>=10:
            def_campi.append(riga_csv)
        i=i+1
        riga_csv = file_csv_config_main.readline()
    file_csv_config_main.close()

    # APRO IL FILE CONTENENTE LA CONFIGURAZIONE
    campi = []
    nomeFileDati = 'config_toponomastica.csv'
    with open(nomeFileDati, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = ',')
       n_righe=0
       for row in reader:
           n_righe=n_righe+1
           n_campi=len(row)
           if n_righe>9:
                i = 0
                while i<n_campi:
                    campi.append(row[i])
                    i=i+1
    csvfile.close()
    print ('Il CSV da sottoporre deve avere le seguenti caratteristiche :')
    print 'NUMERO CAMPI POSSIBILI = ',n_campi
    print campi
    print def_campi
    i=0
    while i<n_campi:
        print
        print 'Campo nr.',i+1
        j=0
        while j<5:
            print def_campi[j],' -> ',campi[(j*n_campi)+i]
            j=j+1
        i=i+1

    return


# FUNZIONE PER LA RICERCA DEGLI OGGETTI SU OPENDATA ESTERNI A SECONDA DEL PARAMETRO PASSATO
def cerca_istanza(stringa_da_cercare,ind_corrispondenza):
    print'---------------------------'
    print 'funzione: cerca_istanza'
    print stringa_da_cercare
    print ind_corrispondenza
    print'---------------------------'
    stringa_opendata=stringa_da_cercare
    return stringa_opendata

################################################################################################################

leggi_configurazione()

# INPUT DEI NOMI DEI FILE
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

# ABBINAMENTO CAMPI FILE CSV CON FILE DI CONFIGURAZIONE
print
print 'Per ogni tipologia di dato possibile indicare a quale campo corrisponde nel proprio CSV.'
print 'Se nel proprio CSV non esiste quel tipo di dato inserire 0.'
corrispondenza=['12', '3', '5', '0', '4', '1', '2']
#corrispondenza=[]
with open(nomeFileDati, 'rb') as csvfile:
       reader = csv.reader(csvfile, delimiter = separatore)
       n_record=0
       for row in reader:
           n_record=n_record+1
           n_campi=len(row)
           i=0
           if n_record==1:
               i=0
               print 'Il record e composto da ', len(row), 'campi :'
               while i<n_campi:
                   stringa_input=row[i]+' corrisponde al campo nr? '
                   #v = raw_input(stringa_input)
                   #corrispondenza.append(v)
                   i=i+1
csvfile.close()
print 'Il file contiene ', n_record, ' record'
print corrispondenza    #togliere

#LEGGE IL FILE DI CONFIGURAZIONE E POPOLA LA LISTA campi
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

#nome_lod=raw_input('Quale nome vuoi per il tuo LOD: ')
#nome_lod=nome_lod+'.ttl'
#spazio_dati=raw_input('Inserisci il link relativo al tuo spazio dati (es. http://miospazio.org/: ')
spazio_dati="http://miospazio.it"
print
print '############################'
print '###         LOD          ###'
print '############################'
spazio_dati='@prefix myspace:<'+spazio_dati+'>'
#f=open(nome_lod,'w')
#f.write(spazio_dati)
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

                        object=' '+object[:-5]+'"'+cerca_istanza(row[i],campi[n_campi_config*9+(j-1)])+'"'
                    else:
                        object=' "'+row[i]+'"^^'+lod_object[j-1]
                    stringa_lod=lod_property[j-1]+object
                    print stringa_lod
                i = i + 1
        if riga==10:
            break
csvfile.close()










#f.close()
