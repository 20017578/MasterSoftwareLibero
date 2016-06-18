#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
import csv
import string
import rdflib


# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def pulisci_input(v):
    #v = v.upper()  # trasfoma l'input in maiuscole cosi' da evitare problema di case sensitive
    #v = v.replace(' DI ', ' ')  # non consideriamo la preposizione 'di' troppo ricorrente e non significativa
    #if v[:3] == 'DI ':
        #v = v[3:]
    #if v[-3:] == ' DI':
        #v = v[:-3]

    # Eliminazioni di eventuali spazi multipli
    while '  ' in v:
        v = v.replace('  ', ' ')
    # Eliminazioni di eventuali spazi iniziali
    if v[0] == ' ':
        v = v[1:]
    # Eliminazioni di eventuali spazi finali
    if v[-1] == ' ':
        v = v[:-1]

    print "Stringa pulita =",v
    return v

# FUNZIONE CHE LEGGE LA PRIMA RIGA DI UN CSV E NE STAMPA I VALORI
def stampaRigaCsv(nf, sep):
    try:
        csvfile = open(nf, 'rb')
        print 'File', nf, 'aperto in lettura'
    except:
        try:
            csvfile = urllib.urlopen(nf, 'rb')
            print 'File online ', nf, 'aperto in lettura'
        except:
            print 'ERRORE: File', nf, 'non trovato !'

    reader = csv.reader(csvfile, delimiter=sep)
    row = next(reader)
    n_c = len(row)  # n_c contiene il numero di campi
    i = 0
    print 'Il record e composto da ', len(row), 'campi :'
    while i < n_c:
        print 'Campo n.', i + 1, ' :', row[i]
        i = i + 1
    csvfile.close()
    return


# FUNZIONE CHE LEGGE IN INPUT :
#     s = stringa che dovrà essere cercata
#     fa = file in cui cercare la stringa 's'
#     sep = caratere separato del file fa che dovrà essere un CSV
#     intest = dice se il primo record del file contiene le intestazioni di riga
#     campoRic = è il numero del campo nel file CSV in cui potrebbe essere presente la stringa da cercare
#     campoRis = è il numero del campo nel file CSV corrispondente al valore che dovrà essere restituito

def cerca_uri(s, fa, sep, intest, campoRic, campoRis):

    print 'RICERCO :', s
    s_split = s.split(' ')  # splitta l'input in parole singole
    parole_s_input = len(s_split)  # numero di vocaboli contenuti nella stringa inserita
    for i in range(0, parole_s_input):
        print ' :', s_split[i]

    # LEGGIAMO IL NOME DELLA PA E VEDIAMO SE ESISTONO SIMILITUDINI COL VALORE INSERITO
    id_ric = 0
    ris_ricerca = []  # Definisco una lista vuota dove vado a mettere le voci trovate
    with open(fa, 'rb') as f2:
        reader = csv.reader(f2, delimiter=sep)
        riga=0
        for row in reader:
            val = row[campoRic]
            codice=row[campoRis]
            if riga > 0 or intest == 'n':
                val_split = val.split(' ')   # splitta il nome della PA letta dal CSV in singole parole
                parole_val = len(val_split)
                # per ogni stringa letta dal CSV verifico se e' uguale ad ognuna delle parole in input
                n_parole = 0
                for i in range(0, parole_s_input):
                    for j in range(0, parole_val):
                        if val_split[j].upper() == s_split[i]:
                            n_parole = n_parole + 1
                        if n_parole == parole_s_input:
                            # print '(*) n=', n_parole, ' -> ', nome_ente , ' codice IPA=', codice_ente  # tutte le parole inserite in input hanno avuto riscontro
                            id_ric = id_ric + 1
                            print id_ric, '-> ', val, ' codice trovato=', codice
                            ris_ricerca.append(codice)
            riga = 1

    i = input("Inserire il numero corrispondente alla voce corretta (0 se non esiste): ") - 1
    if i>=0:
        retValue= ris_ricerca[i]
    else:
        retValue="#NOT_FOUND#"
    print("Hai scelto : ", retValue)
    return retValue


########################################################################################################
########                                     INIZIO PROGRAMMA                                   ########
########################################################################################################


#1: Chiedo se il valore da cercare è dato in input o se è un insieme di valori in un campo di un file CSV
ammCom =raw_input("Cerchi un'Amministrazione ('a') o un Comune ('c') ? ")
csv_stringa = raw_input("I valori da cercare sono contenuti in un CSV (s/n) ? ")
# csv_stringa = 'n'
if csv_stringa == 'n':
    # val_input = '00449420348'
    # val_input = 'provincia di firenze   '
    val_input = raw_input("Inserire il nome del valore da cercare (se un Comune inserire solo il nome del comune, non: Comune di ...): ")
    val_input=pulisci_input(val_input).upper()
else:
    nomeFileCSV = raw_input("Nome del file CSV :")
    separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabilazione) : ")
    #separatore = ';'
    if separatore == "TAB":
        separatore = '\t'
    stampaRigaCsv(nomeFileCSV, separatore)
    intestazione = raw_input("La prima riga del file e' una riga di intestazione dei campi (s/n) ? ")
    # intestazione = 's'
    campo_ricerca = raw_input("Qual è il campo da cercare ? ")
    campo_ricerca = int(campo_ricerca) - 1
    # campo_ricerca=1

#2: Chiedo a quale url si trova il LOD da analizzare o qual è il LOD locale in cui cercare

#nomeFileDati = raw_input("Indirizzo del dataset in cui cercare i valori :")
nomeFileDati = 'spcdata.digitpa.gov.it/data/amm.rdf'
nomeFileDati = 'amm.rdf'
formatoDati = 'application/rdf+xml'
g = rdflib.Graph()
try:
    f = open(nomeFileDati)
    g.parse(f, format=formatoDati)
    print 'Ho inizializzato il grafo dal file : ', nomeFileDati
    f.close()
except:
    print 'File', nomeFileDati, 'non trovato'
    sys.exit (1)

#3: Chiedo se si vuole generare un nuovo CSV con i campi trovati
if csv_stringa=='s':
    nuovoCsv = raw_input("Si vuole generare un nuovo CSV con i dati trovati (s/n) ? ")
    # nuovoCsv='s'

#4: ANALISI
#geonames_In = rdflib.URIRef ('http://www.geonames.org/ontology#locatedIn')
#comuniAgID = {}

link="http://spcdata.digitpa.gov.it/"
if ammCom=='a':
    link=link+"Amministrazione"
else:
    link=link+"Comune"
valTrovati={}    # è un dizionario che serve a contenere le stringhe per cui è già stata fatta la ricerca così da non dover ripete la ricerca
nriga=0
if csv_stringa == 's':
    with open(nomeFileCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=separatore)
        for row in reader:
            n = 0
            if nriga == 1 or intestazione == 'n':
                val_input=pulisci_input(row[campo_ricerca])
                val_input=val_input.upper()
                print "CERCO ... ", val_input
                trovato = 0
                for oggetto in g.subjects(predicate=rdflib.RDF.type, object=rdflib.URIRef(link)):
                    nomeOggetto = g.value(oggetto, rdflib.RDFS.label).toPython().upper().replace('-', ' ')
                    n = n + 1
                    # print "nomeComune = ",nomeComune, " (", codiceComune,")"
                    if nomeOggetto == val_input:
                        lungCodice = len(oggetto) - len(link) - 1
                        codice = oggetto[-lungCodice:]
                        if ammCom == 'a':
                            codice= "Amministrazione/" + codice
                        else:
                            codice = "Comune/" + codice
                        print oggetto, "è un ",link
                        print "nome = ", nomeOggetto
                        print "TROVATO --", codice, "--"
                        valTrovati[row[campo_ricerca]] = codice
                        trovato=1
                if trovato==0:
                    valTrovati[row[campo_ricerca]] = ''
            if nriga == 0 and intestazione == 's':
                nriga=1

    print valTrovati
    csvfile.close()
    # valTrovati={'Cividale del Friuli': u'C758', 'Otranto': u'G188', 'Torino': u'L219', 'Milano': u'F205', 'Roma': u'H501'}

    # SE RICHIESTO SCRIVE SUL NUOVO FILE
    nriga=0
    if nuovoCsv=='s':
        nomeNuovoCSV=nomeFileCSV[:-4]+"_n.csv"
        csvnew = open(nomeNuovoCSV, 'wb')
        print 'Sto scrivendo su ', nomeNuovoCSV
        with open(nomeFileCSV, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=separatore)
            for row in reader:
                nuovo_record=row
                print nuovo_record
                n=len(row)
                if nriga == 1 or intestazione == 'n':
                    row.append(valTrovati[row[campo_ricerca]])
                if nriga == 0 and intestazione == 's':
                    nriga = 1
                    row.append('CAMPO_SPCDATA')
                writer = csv.writer(csvnew,delimiter=separatore)
                writer.writerow(nuovo_record)

    csvnew.close()
    csvfile.close()

if csv_stringa == 'n':
    print "CERCO ... ", val_input
    print "link = ",link
    for oggetto in g.subjects(predicate=rdflib.RDF.type, object=rdflib.URIRef(link)):
        nomeOggetto = g.value(oggetto, rdflib.RDFS.label).toPython().upper().replace('-', ' ')
        #print "nomeOggetto = ",nomeOggetto
        if nomeOggetto == val_input:
            lungCodice=len(oggetto)-len(link)-1
            codice = oggetto[-lungCodice:]
            if ammCom == 'a':
                codice = "Amministrazione/" + codice
            else:
                codice = "Comune/" + codice
            print "TROVATO --", nomeOggetto, "--"
            print "oggetto = ", oggetto
            print "lungCod = ", lungCodice
            print "codice = ", codice
            #valTrovati[row[campo_ricerca]] = codiceComune

print "Process ended"

