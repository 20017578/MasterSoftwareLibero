#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
import csv
import string


# FUNZIONE PER LA PULIZIA DELLA STRINGA IN INPUT
def pulisci_input(v):
    v = v.upper()  # trasfoma l'input in maiuscole cosi' da evitare problema di case sensitive
    v = v.replace(' DI ', ' ')  # non consideriamo la preposizione 'di' troppo ricorrente e non significativa
    if v[:3] == 'DI ':
        v = v[3:]
    if v[-3:] == ' DI':
        v = v[:-3]

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
def leggiRigaCsv(nf, sep):
    try:
        csvfile = open(nf, 'rb')
    except:
        try:
            csvfile = urllib.urlopen(nf, 'rb')
            print 'File', nf, 'aperto in lettura'
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

# Chiedo se il valore da cercare è dato in input o se è un insieme di valori in un campo di un file CSV

csv_stringa = raw_input("I valori da cercare sono contenuti in un CSV (s/n) ? ")
# csv_stringa = 's'
if csv_stringa == 'n':
    # val_input = '00449420348'
    val_input = 'provincia di firenze   '
    val_input = raw_input("Inserire il nome del valore da cercare : ")
else:
    # nomeFile = raw_input("Nome del file CSV :")
    nomeFile = "civici_prova.csv"

    separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabilazione) : ")
    separatore = ';'
    if separatore == "TAB":
        separatore = '\t'
    leggiRigaCsv(nomeFile, separatore)
    # intestazione = raw_input("La prima riga del file e' una riga di intestazione dei campi (s/n) ? ")
    intestazione = 's'
    # campo_ricerca = raw_input("Qual  il campo da cercare ? ")
    # campo = int(campo_ricerca) - 1
    campo=1

# Chiedo a quale url si trova il CSV da analizzare o qual è il CSV locale in cui cercare

# fileAnalisi = raw_input("Indirizzo del CSV in cui cercare i valori :")
fileAnalisi = 'http://spcdata.digitpa.gov.it/data/amm.csv'
fileAnalisi = 'amm.csv'
# separatore = raw_input("Inserire il carattere separatore ( scrivere TAB per il carattere di tabilazione) : ")
separatore_f_analisi = 'TAB'
if separatore_f_analisi == "TAB":
    separatore_f_analisi = '\t'
leggiRigaCsv(fileAnalisi, separatore_f_analisi)
#intestazione_Analisi = raw_input("La prima riga del file e' una riga di intestazione dei campi (s/n) ? ")
intestazione_Analisi='n'
#campo_ricerca_analisi = raw_input("Qual  il campo in cui cercare ? ")
campo_ricerca_analisi='2'
campo_analisi = int(campo_ricerca_analisi)-1
#campo_risultato_analisi = raw_input("Qual  il campo col codice da restituire ? ")
campo_risultato_analisi='1'
campo_risultato = int(campo_risultato_analisi)-1

# Chiedo se si vuole generare un nuovo CSV coni campi trovati
if csv_stringa=='s':
    #   nuovoCsv = raw_input("Si vuole generare un nuovo CSV con i dati trovati (s/n) ? ")
    nuovoCsv='s'
# ANALISI

# se richiesto apro il file in scrittura
if nuovoCsv == 's':
    nuovoFile = nomeFile[:-4] + "_new.csv"
    fn = open(nuovoFile, 'wb')
    spamwriter = csv.writer(fn, delimiter=separatore)

valTrovati={}
# apro il file CSV con i dati da ricercare ed analizzo tutti i record

if csv_stringa=='s':
    with open(nomeFile, 'rb') as f1:
        riga = 0
        reader = csv.reader(f1, delimiter=separatore)
        for row in reader:
            n_campi=len(row)
            val_input = row[campo]
            uriConfermata = ''
            if (riga > 0 or intestazione == 'n') and val_input not in valTrovati:
                val_input=pulisci_input(val_input)
                uriConfermata = cerca_uri(val_input, fileAnalisi, separatore_f_analisi,intestazione_Analisi,campo_analisi, campo_risultato)
                print 'uriConfermata=',uriConfermata
                valTrovati[row[campo]]=uriConfermata
            riga = riga+1
            if riga==1 and intestazione == 's':
                uriConfermata='NUOVO CAMPO'
            if uriConfermata=='':
                uriConfermata=valTrovati[row[campo]]
            if nuovoCsv == 's':
                row[n_campi-1]=uriConfermata
                print row
                spamwriter.writerow(row)
    f1.close()
    print valTrovati

else:
    val_input = pulisci_input(val_input)
    uriConfermata = cerca_uri(val_input, fileAnalisi, separatore_f_analisi, intestazione_Analisi, campo_analisi,campo_risultato)
    print uriConfermata
