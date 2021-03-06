#
# Su Ubuntu/Debian i pacchetti necessari si installano con:
# apt-get install python-rdflib python-requests
#

import rdflib
import requests
import sys
import csv

#
# Lettura dei dati di AgID
# TODO: rendere questa porzione di codice una funzione!!
#

grafo_AgID = rdflib.Graph ()

fonteDati = 'AgID'
nomeFileDati = 'DatiAgID.ttl'
formatoDati = 'n3'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.ttl'
try:
    grafo_AgID.parse (file=open (nomeFileDati), format=formatoDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da', fonteDati, ', termino.'
            sys.exit (1)
    grafo_AgID.parse (data=datiDaRete.text, format=formatoDati)
    grafo_AgID.serialize (destination=open (nomeFileDati, 'w'), format=formatoDati)
    print 'Dati salvati su', nomeFileDati, 'per usi futuri'
    datiDaRete = None  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

# print len (grafo_AgID)

nomeFileDati = 'DatiAgID.csv'
separatoreDati = '\t'
URL_Dati = 'http://spcdata.digitpa.gov.it/data/amm.csv'
try:
    letturaRighe = csv.reader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da AgID, termino.'
            sys.exit (1)
    f = open (nomeFileDati, 'w')
    f.write (datiDaRete.text)
    print 'Ho scritto i dati sul file', nomeFileDati
    f.close ()
    letturaRighe = csv.reader (open (nomeFileDati), delimiter = separatoreDati)
    datiDaRete = None  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

# Legge dal CSV quali sono le scuole ed aggiunge la tripla corretta al grafo
spcdata_catAmm = rdflib.Namespace('http://spcdata.digitpa.gov.it/Categoriaamministrazione/')
IRI_scuola = spcdata_catAmm.L33
IRI_orgClassif = rdflib.URIRef ('http://www.w3.org/ns/org#classification')
pref_amministrazione = 'http://spcdata.digitpa.gov.it/Amministrazione/'

contoScuole = 0
for riga in letturaRighe:
    if riga [11] == 'Istituti di Istruzione Statale di Ogni Ordine e Grado':
        if not grafo_AgID.value (rdflib.URIRef (pref_amministrazione + riga[0]),  IRI_orgClassif):
            grafo_AgID.set ( (rdflib.URIRef (pref_amministrazione + riga[0]), IRI_orgClassif, IRI_scuola) )
            contoScuole += 1
        else:
            print 'Questa scuola ha una categoria associata, non aggiungo altro'

comuni = set (grafo_AgID.subjects (predicate=rdflib.RDF.type, object=rdflib.URIRef ('http://spcdata.digitpa.gov.it/Comune')))
scuole = set (grafo_AgID.subjects (predicate=IRI_orgClassif, object=IRI_scuola))

grafo_AgID_essenziale = rdflib.Graph ()
daAggiungere = comuni | scuole
aggiunti = set ()
while len (daAggiungere) != 0:
    dato = daAggiungere.pop ()
    aggiunti.add (dato)
    for p, o in grafo_AgID.predicate_objects (dato):
        grafo_AgID_essenziale.add ( (dato, p, o) )
        if p not in aggiunti:
            daAggiungere.add (p)
        if type (o) == type (p) and o not in aggiunti:
            daAggiungere.add (o)

aggiunti.clear ()

#
# Qualche manipolazione sul grafo AgID
#

IRI_pec = rdflib.URIRef ('http://spcdata.digitpa.gov.it/PEC')
IRI_mail = rdflib.namespace.FOAF.mbox
IRI_locatedIn = rdflib.URIRef ('http://www.geonames.org/ontology#locatedIn')
IRI_label = rdflib.URIRef ('http://www.w3.org/2000/01/rdf-schema#label')

listaMeccanograficiAgID = []
listaScuolePerComune = {}
contoAgID = 0
for amministrazione in grafo_AgID.subjects (predicate=IRI_orgClassif, object=IRI_scuola):
    meccanograficoScuola = ''
    contoAgID += 1
    if contoAgID % 1000 == 0:
        print 'Analizzate', contoAgID, 'amministrazioni, trovate', len (listaMeccanograficiAgID), 'possibili scuole'
    # cerca se la PEC ha dominio istruzione.it
    for pec in grafo_AgID.objects (amministrazione, IRI_pec):
        if 'ISTRUZIONE.IT' in str (pec).upper ():
            meccanograficoScuola = str (pec).split ('@')[0]
    if len(meccanograficoScuola) != 10:  # Cerca ancora solo se non trovata prima
        if meccanograficoScuola != '':
            print "%s sembra una scuola, ma la pec %s non sembra indicare un meccanografico, cerco la e-mail"%(str(amministrazione), meccanograficoScuola)
        for mail in grafo_AgID.objects (amministrazione, IRI_mail):
            if 'ISTRUZIONE.IT' in str (mail).upper ():
                meccanograficoScuola = str (mail).split ('@')[0]
    if meccanograficoScuola != '':
        if len(meccanograficoScuola) != 10:
            print "%s sembra una scuola, ma il codice %s non sembra un meccanografico"%(str(amministrazione), meccanograficoScuola)
        else:
            codiceCatastaleComune = '';
            for Comune in grafo_AgID.objects(amministrazione,IRI_locatedIn):
                codiceCatastaleComune = str(Comune).split('/')[-1];
                if codiceCatastaleComune in listaScuolePerComune:
                    listaScuolePerComune[codiceCatastaleComune].append(meccanograficoScuola.upper ())
                else:
                    listaScuolePerComune[codiceCatastaleComune] = [meccanograficoScuola.upper ()]
            if codiceCatastaleComune == '':
                print "Non trovato il comune, stampo quel che so su questa amministrazione"
                for p,o in grafo_AgID.predicate_objects(amministrazione):
                    print str(p), str(o)
                    for lab in grafo_AgID.objects(o,IRI_label):
                        print ':::: label', str(lab)
        listaMeccanograficiAgID.append (meccanograficoScuola.upper ())
        unaScuola = amministrazione
    else:
        print 'Scuola di cui non si trova un meccanografico ...'

print 'Su', contoAgID, 'scuole, ho trovato', len (listaMeccanograficiAgID), 'probabili meccanografici, distribuiti su', len (listaScuolePerComune), 'comuni'

sommaScuoleConComune = 0
numeroScuolePerComune = {}
for i in listaScuolePerComune:
    numeroScuolePerComune[i] = len(listaScuolePerComune[i])
    sommaScuoleConComune += numeroScuolePerComune[i]

comuniOrdinatiPerNumeroScuole = sorted (numeroScuolePerComune, key = lambda x:numeroScuolePerComune[x])

print 'Trovate in tutto', sommaScuoleConComune, 'scuole distribuite nei seguenti comuni:', [(x,numeroScuolePerComune[x]) for x in comuniOrdinatiPerNumeroScuole]

print 'Lista delle', numeroScuolePerComune['L219'], 'scuole trovate nel comune di Torino', listaScuolePerComune['L219']

#
# Lettura dei dati da MIUR
# TODO: Rendere anche questa porzione una funzione!
#

fonteDati = 'MIUR'
nomeFileDati = 'DatiMIUR.csv'
separatoreDati = ';'
URL_Dati = 'http://www.istruzione.it/scuolainchiaro_dati/7-Anagrafe_Scuole_Statali_201516.csv'
try:
    letturaRighe = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da AgID, termino.'
            sys.exit (1)
    # TODO: Forse scrivere il file su disco ed aprirlo?
    f = open (nomeFileDati, 'w')
    f.write (datiDaRete.text)
    print 'Ho scritto i dati sul file', nomeFileDati
    f.close ()
    letturaRighe = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    datiDaRete = None # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

catalogoMeccanograficiMIUR = {}

voceDaConteggiare = 'ISTITUTO PRINCIPALE'
voceDaFiltrare = 'COMUNE'
voceDaSalvare = 'PLESSO/SCUOLA'
valoreDaCercare = 'TORINO'

contoMIUR = 0
valoriTrovati = []
istitutiTrovati = set ()

if voceDaConteggiare in letturaRighe.fieldnames:
    for riga in letturaRighe:
        contoMIUR += 1
        if riga[voceDaConteggiare] in catalogoMeccanograficiMIUR:
            catalogoMeccanograficiMIUR[riga[voceDaConteggiare]] += 1
        else:
            catalogoMeccanograficiMIUR[riga[voceDaConteggiare]] = 1
        if voceDaSalvare in letturaRighe.fieldnames and voceDaFiltrare in letturaRighe.fieldnames:
            if riga[voceDaFiltrare] == valoreDaCercare:
                valoriTrovati.append (riga[voceDaSalvare])
                istitutiTrovati.add (riga[voceDaConteggiare])
else:
    print 'La voce', voceDaConteggiare, 'non si trova...'

print 'Su', contoMIUR, 'scuole, ho trovato', len (catalogoMeccanograficiMIUR), 'istituzoni'
print 'Per', voceDaFiltrare, 'pari a', valoreDaCercare, 'ho trovato i seguenti', len (valoriTrovati), 'valori per', voceDaSalvare, ':', valoriTrovati

contoAgID_noMIUR = 0
for unaScuola in listaMeccanograficiAgID:
    if unaScuola in catalogoMeccanograficiMIUR:
        if catalogoMeccanograficiMIUR[unaScuola] == 0:
            print 'Strano, per', unaScuola, 'non riultano plessi, forse duplicato su AgID?'
        else:
            catalogoMeccanograficiMIUR[unaScuola] = 0
    else:
        contoAgID_noMIUR += 1

contoMIUR_noAgID = 0
for unaScuola in catalogoMeccanograficiMIUR:
    if catalogoMeccanograficiMIUR[unaScuola] != 0:
        contoMIUR_noAgID += 1

print 'Trovate ', len (listaMeccanograficiAgID), 'scuole su AgID e', len (catalogoMeccanograficiMIUR), 'su MIUR'
print 'Su AgID ci sono', contoAgID_noMIUR, 'istituzioni non presenti su MIUR'
print 'Su MIUR ci sono', contoMIUR_noAgID, 'istituzioni non presenti su AgID'

#
# Lettura dei dati da Comune di Torino
# TODO: Rendere anche questa porzione una funzione!
#

fonteDati = 'Torino'
nomeFileDati = 'DatiTorino.csv'
separatoreDati = ';'
URL_Dati = 'http://aperto.comune.torino.it/sites/default/files/scuole_0.csv'
try:
    letturaRighe = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    print 'Ho letto i dati', fonteDati, 'dal file', nomeFileDati
except:
    # Se riesco a scaricare da rete, ha senso salvare nel nome file per avere una copia locale ed accelerare le cose?
    print 'File', nomeFileDati, 'non trovato, provo da rete'
    try:
        # Proviamo a scaricare i dati dall'URL
        datiDaRete = requests.get (URL_Dati)
        print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati
    except:
        # Se non siamo riusciti, forse serve impostare il proxy della della Regione
        print '... provo col proxy della Regione'
        proxies = {
            'http': 'http://10.102.162.8:80',
            'https': 'http://10.102.162.8:80',
        }
        try:
            datiDaRete = requests.get (URL_Dati, proxies=proxies)
            print 'Ho scaricato i dati', fonteDati, 'da', URL_Dati, 'usando il proxy'
        except:
            print 'Impossibile scaricare i dati da AgID, termino.'
            sys.exit (1)
    # TODO: Forse scrivere il file su disco ed aprirlo?
    f = open (nomeFileDati, 'w')
    f.write (datiDaRete.text)
    print 'Ho scritto i dati sul file', nomeFileDati
    f.close ()
    letturaRighe = csv.DictReader (open (nomeFileDati), delimiter = separatoreDati)
    datiDaRete = None  # ha senso *cancellare* la variabile per liberare memoria? metodi migliori?

voceDaFiltrare = 'EMAIL'

meccanograficiComune = set ()
contoComune = 0
contoIstruzione = 0
if voceDaFiltrare in letturaRighe.fieldnames:
    for riga in letturaRighe:
        contoComune += 1
        if 'ISTRUZIONE.IT' in riga[voceDaFiltrare].upper ():
            meccanograficoScuola = riga[voceDaFiltrare].split ('@')[0]
            if len(meccanograficoScuola) != 10:
                print "%s sembra una scuola, ma il codice %s non sembra un meccanografico"%(riga[voceDaFiltrare], meccanograficoScuola)
            else:
                contoIstruzione += 1
                meccanograficiComune.add (meccanograficoScuola.upper ())
else:
    print 'La voce', voceDaFiltrare, 'non si trova...'

print 'Su', contoComune, 'scuole catalogate dal comune, per', contoIstruzione, 'si riesce ad ipotizzare il meccanografico'
print 'Tolti i doppioni, i codici sono', len (meccanograficiComune), ':', list(meccanograficiComune)
print 'Di questi, i seguenti non appaiono (vecchi?) tra i codici MIUR:', meccanograficiComune - set(catalogoMeccanograficiMIUR)
print 'In compenso,', len(istitutiTrovati - meccanograficiComune), 'istituti che MIUR localizza in Torino, non vengono trovati in questa lista (probabilmente per e-mail differente)'
