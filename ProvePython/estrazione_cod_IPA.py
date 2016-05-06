# Da un input il programma legge il CSV con i dati delle amministrazioni per estrarre il codice IPA
#   da usare come codice dell'amministrazione nel LOD.
#   Al momento la ricerca viene fatta per nome dell'ente o per CF


import urllib
import sys
import csv
import string

# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def pulisci_input(stringa_pa):
    stringa_pulita = stringa_pa
# Eliminazioni di eventuali spazi multipli
    while '  ' in stringa_pulita:
        stringa_pulita = stringa_pulita.replace('  ', ' ')
# Eliminazioni di eventuali spazi iniziali
    if stringa_pulita[0]==' ':
        stringa_pulita = stringa_pulita[1:]
# Eliminazioni di eventuali spazi finali
    if stringa_pulita[-1] == ' ':
        stringa_pulita = stringa_pulita[:-1]
    return stringa_pulita




if len (sys.argv) > 1:
    pa_input = sys.argv[1]
else:
    pa_input = 'provincia di firenze   '
#pa_input = '00449420348'
pa_input=pa_input.upper()            # trasfoma l'input in maiuscole cosi' da evitare problema di case sensitive
pa_input=pa_input.replace('DI','')   # non consideriamo la preposizione 'di' troppo ricorrente e non significativa

pa_input=pulisci_input(pa_input)
print ':input pulito:(',pa_input,') len=',len(pa_input)

pa_input_split=pa_input.split(' ')             #splitta l'input in parole singole
parole_stringa_pa_input=len(pa_input_split)    #numero di vocaboli contenuti nella stringa inserita
print 'Codice Ascii del primo carattere =',ord(pa_input[0])
for i in range(0, parole_stringa_pa_input):
    print ':',pa_input_split[i]

# APRO IL FILE ONLINE CONTENENTE LE INFORMAZIONI DELLE PA
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.csv'
try:
    file_csv_amministrazioni =urllib.urlopen(URL_Dati)
    print 'File', URL_Dati, 'aperto in lettura'
except:
    print 'ERRORE: File', URL_Dati, 'non trovato !'

# LEGGIAMO IL NOME DELLA PA E VEDIAMO SE ESISTONO SIMILITUDINI COL VALORE INSERITO
riga_csv=file_csv_amministrazioni.readline()

while riga_csv:
    riga_split = riga_csv.split('\t')
    codice_ente = riga_split[0]           # legge la prima colonna contenente i codici identificativi delle PA all'interno dell'IPA
    nome_ente=riga_split[1]               # legge la seconda colonna contenente i nomi delle PA
    cf_ente=riga_split[15]                 # legge la colonna 15 contenente i CF delle PA
    nome_ente_split=nome_ente.split(' ')  # splitta il nome della PA letta dal CSV in singole parole
    parole_nome_ente = len(nome_ente_split)
    # per ogni parola del nome della PA letto dal CSV verifica se e' uguale ad ognuna delle parole dell'ente inserito in input

    if ord(pa_input[0])<48 or ord(pa_input[0])>56:      # la stringa in input inizia con una lettera
        n_parole = 0
        for i in range(0, parole_stringa_pa_input):
            for j in range (0, parole_nome_ente):
                if nome_ente_split[j].upper()==pa_input_split[i]:
                    n_parole= n_parole+1
        if n_parole == parole_stringa_pa_input:
            print '(*) n=', n_parole, ' -> ', nome_ente , ' codice IPA=', codice_ente  # tutte le parole inserite in input hanno avuto riscontro

    if ord(pa_input[0]) >47 and ord(pa_input[0]) <57:  # la stringa in input inizia con una cifra (cf ?)
        n_cf = 0
        if cf_ente == pa_input_split[0]:
            n_cf=1
        if n_cf==1:
            print '(*) cf (csv)=', cf_ente , ' nome ente=', nome_ente , ' (cf input)-> ', pa_input_split[0] , ' codice IPA=', codice_ente  # tutte le parole inserite in input hanno avuto riscontro

    riga_csv = file_csv_amministrazioni.readline()
