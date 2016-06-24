#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
import csv
import string
import rdflib


# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def pulisci_input(v):
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

#nomeFileDati = raw_input("Indirizzo del dataset in cui cercare i valori (nome file o indirizzo web:")
nomeFileDati = 'spcdata.digitpa.gov.it/data/amm.rdf'
nomeFileDati = 'amm.rdf'
print "inizializzazione del grafo ... L'operazione potrebbe richiedere diversi minuti."
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
                if row[campo_ricerca]<>"":
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
                    if row[campo_ricerca]<>"":
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

