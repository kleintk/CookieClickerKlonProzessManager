
# -*- coding: utf-8 -*-
'''
Created on 27.03.2014

@author: Phate
'''




from PySide.QtCore import *
from PySide.QtGui import *
import sys
import time
import pickle

import hauptfenster


class MainWindow(QMainWindow, hauptfenster.Ui_MainWindow):
    
    # SCORE Werte
    SCORE = 600
    SCOREassistenten = 0
    SCOREdos = 0
    SCOREserver = 0
    SCOREmatrix = 0
    # Baumenue KONSTANTEN
    PREISassistent = 200
    PRODUKTIONassistent = 1
    PREISdos = 500
    PRODUKTIONdos = 4
    PREISserver = 3000
    PRODUKTIONserver = 10
    PREISmatrix = 10000
    PRODUKTIONmatrix = 40
    # Klick KONSTANTE
    PRODUKTIONklick = 1
    
    BESITZTUEMER = {"assistent": 0, "dos": 0, "server": 0, "matrix": 0}
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle("Prozess Manager")
        # alle Besitztümer verstecken
        #self.groupBoxAssistenten.hide()
        #self.groupBoxDOS.hide()
        #self.groupBoxServer.hide()
        #self.groupBoxMatrix.hide()
        
        # alle Baumöglichekiten verstecken        
        #self.frameAssistent.hide()
        #self.frameDOS.hide()
        #self.frameServer.hide()
        #self.frameMatrix.hide()
        
        # Kosten und Produktion im Interface anpassen
        self.labelPreisAssistent.setText("Preis : $ "+str(self.PREISassistent))
        self.labelProduktionAssistent.setText("+"+str(self.PRODUKTIONassistent)+" / Sekunde")
        self.labelPreisDOS.setText("Preis : $ "+str(self.PREISdos))
        self.labelProduktionDOS.setText("+"+str(self.PRODUKTIONdos)+" / Sekunde")
        self.labelPreisServer.setText("Preis : $ "+str(self.PREISserver))
        self.labelProduktionServer.setText("+"+str(self.PRODUKTIONserver)+" / Sekunde")
        self.labelPreisMatrix.setText("Preis : $ "+str(self.PREISmatrix))
        self.labelProduktionMatrix.setText("+"+str(self.PRODUKTIONmatrix)+" / Sekunde")
        
        # Buttons verknuepfen
        self.pushButtonAssistentHinzufuegen.clicked.connect(self.assistentHinzufuegen)
        self.pushButtonDOSHinzufuegen.clicked.connect(self.dosHinzufuegen)
        self.pushButtonServerHinzufuegen.clicked.connect(self.serverHinzufuegen)
        self.pushButtonMatrixHinzufuegen.clicked.connect(self.matrixHinzufuegen)
        
        self.pushButtonProzess.clicked.connect(self.prozessButtonGeklickt)
               
        # startet den Thread der konstant ein showSignal emitet
        self.schuftet = scoreThread()
        self.schuftet.start()        
        self.schuftet.showSignal.connect(self.scoreAusgabe)
        
        # startet den Thread der konstant die automatischen einnahmen berechnet
        self.schuftetAuch = besitztuemerProduktionsThread()
        self.schuftetAuch.start()
        
        # buttons des menues triggern
        self.actionBeenden.triggered.connect(self.programmBeenden)
        self.actionUeber.triggered.connect(self.ueberKlicken)
        self.actionSpiel_speichern.triggered.connect(self.speichern)
        self.actionSpiel_laden.triggered.connect(self.laden)
        
    
    # gibt konstant die punkte am scoreboard aus
    def scoreAusgabe(self):
        self.labelScore.setText(str(self.SCORE))
        self.labelAssistentenProzesseGesammt.setText(str(self.SCOREassistenten))
        self.labelDOSProzesseGesammt.setText(str(self.SCOREdos))
        self.labelServerProzesseGesammt.setText(str(self.SCOREserver))
        self.labelMatrixProzesseGesammt.setText(str(self.SCOREmatrix))
        
    def prozessButtonGeklickt(self):
        self.SCORE +=self.PRODUKTIONklick
        
    
    def assistentHinzufuegen(self):
        if self.SCORE >= self.PREISassistent:
            self.SCORE -= self.PREISassistent
            self.BESITZTUEMER["assistent"] += 1
            zahl = int(self.labelAnzahlAssitenten.text())
            self.labelAnzahlAssitenten.setText(str(zahl+1))
            
            zahl = int(self.labelAssistentenProzesseProSekunde.text())
            self.labelAssistentenProzesseProSekunde.setText(str(zahl + self.PRODUKTIONassistent))
            zahl = int(self.labelProzesseProSekunde.text())
            self.labelProzesseProSekunde.setText(str(zahl + self.PRODUKTIONassistent))
            
            self.PREISassistent = round(self.PREISassistent * 1.15)
            self.labelPreisAssistent.setText("Preis : $ "+str(self.PREISassistent))
        else:
            self.statusbar.showMessage("Zu wenig Prozesse für den Kauf.", 2000)
        
    
    def dosHinzufuegen(self):
        if self.SCORE >= self.PREISdos:
            self.SCORE -= self.PREISdos
            self.BESITZTUEMER["dos"] += 1
            zahl = int(self.labelAnzahlDOS.text())
            self.labelAnzahlDOS.setText(str(zahl+1))
            
            zahl = int(self.labelDOSProzesseProSekunde.text())
            self.labelDOSProzesseProSekunde.setText(str(zahl + self.PRODUKTIONdos))
            zahl = int(self.labelProzesseProSekunde.text())
            self.labelProzesseProSekunde.setText(str(zahl + self.PRODUKTIONdos))
            
            self.PREISdos = round(self.PREISdos * 1.15)
            self.labelPreisDOS.setText("Preis : $ "+str(self.PREISdos))
        else:
            self.statusbar.showMessage("Zu wenig Prozesse für den Kauf.", 2000)

    def serverHinzufuegen(self):
        if self.SCORE >= self.PREISserver:
            self.SCORE -= self.PREISserver
            self.BESITZTUEMER["server"] += 1
            zahl = int(self.labelAnzahlServer.text())
            self.labelAnzahlServer.setText(str(zahl+1))
            
            zahl = int(self.labelServerProzesseProSekunde.text())
            self.labelServerProzesseProSekunde.setText(str(zahl + self.PRODUKTIONserver))
            zahl = int(self.labelProzesseProSekunde.text())
            self.labelProzesseProSekunde.setText(str(zahl + self.PRODUKTIONserver))
            
            self.PREISserver = round(self.PREISserver * 1.15)
            self.labelPreisServer.setText("Preis : $ "+str(self.PREISserver))
        else:
            self.statusbar.showMessage("Zu wenig Prozesse für den Kauf.", 2000)

    def matrixHinzufuegen(self):
        if self.SCORE >= self.PREISmatrix:
            self.SCORE -= self.PREISmatrix
            self.BESITZTUEMER["matrix"] += 1
            zahl = int(self.labelAnzahlMatrix.text())
            self.labelAnzahlMatrix.setText(str(zahl+1))
            
            zahl = int(self.labelMatrixProzesseProSekunde.text())
            self.labelMatrixProzesseProSekunde.setText(str(zahl + self.PRODUKTIONmatrix))
            zahl = int(self.labelProzesseProSekunde.text())
            self.labelProzesseProSekunde.setText(str(zahl + self.PRODUKTIONmatrix))
            
            self.PREISmatrix = round(self.PREISmatrix * 1.15)
            self.labelPreisMatrix.setText("Preis : $ "+str(self.PREISmatrix))
        else:
            self.statusbar.showMessage("Zu wenig Prozesse für den Kauf.", 2000)

        
    def programmBeenden(self):
        self.schuftet.terminate()
        self.schuftetAuch.terminate()
        sys.exit()
    
    def ueberKlicken(self):
        QMessageBox.information(self, "Prozess Manager!", "Coded by Tkinter/Phate")
        
    def speichern(self):
        try:
            fobj = open("savegame.sav", "wb")
            liste = []
            liste.append(self.SCORE)    # 0
            liste.append(self.SCOREassistenten)
            liste.append(self.SCOREdos)
            liste.append(self.SCOREserver)
            liste.append(self.SCOREmatrix)
            liste.append(self.PREISassistent)
            liste.append(self.PRODUKTIONassistent)
            liste.append(self.PREISdos)
            liste.append(self.PRODUKTIONdos)
            liste.append(self.PREISserver)
            liste.append(self.PRODUKTIONserver)
            liste.append(self.PREISmatrix)
            liste.append(self.PRODUKTIONmatrix)
            liste.append(self.PRODUKTIONklick)
            liste.append(self.BESITZTUEMER)    # 14  
            pickle.dump(liste, fobj)
            QMessageBox.information(self, "Prozess Manager", "Gespeichert.")
            fobj.close()
        except:
            QMessageBox.warning(self, "Prozess Manager", "Fehler beim Speichern.")
        
    def laden(self):
        try:
            fobj = open("savegame.sav", "rb")
            liste = pickle.load(fobj)
            fobj.close()
            self.SCORE = liste[0]
            self.SCOREassistenten = liste[1]
            self.SCOREdos = liste[2]
            self.SCOREserver = liste[3]
            self.SCOREmatrix = liste[4]
            self.PREISassistent = liste[5]
            self.PRODUKTIONassistent = liste[6]
            self.PREISdos = liste[7]
            self.PRODUKTIONdos = liste[8]
            self.PREISserver = liste[9]
            self.PRODUKTIONserver = liste[10]
            self.PREISmatrix = liste[11]
            self.PRODUKTIONmatrix = liste[12]
            self.PRODUKTIONklick = liste[13]
            self.BESITZTUEMER = liste[14]
            
            #self.labelAnzahlAssitenten.setText(self.BESITZTUEMER["assistenten"])
        except:
            QMessageBox.warning(self, "Prozess Manager", "Fehler beim Laden.")
            
        

class scoreThread(QThread):
    
    showSignal = Signal()
    
    def __init__(self, parent=None):
        super(scoreThread, self).__init__(parent)
        
    def run(self): # override der run-methode des QThread
        while True:
            time.sleep(0.1)
            self.showSignal.emit()
        

class besitztuemerProduktionsThread(QThread):
    
    
    def __init__(self, parent=None):
        super(besitztuemerProduktionsThread, self).__init__(parent)
        
    def run(self): # override der run-methode des QThread
        while True:
            time.sleep(1)
            zusatzSCORE = 0
            localDICT = form.BESITZTUEMER
            
            anzahlAssisten = localDICT["assistent"]
            anzahlDOS = localDICT["dos"]
            anzahlServer = localDICT["server"]
            anzahlMatrix = localDICT["matrix"]
            
            for i in range(anzahlAssisten):
                zusatzSCORE += form.PRODUKTIONassistent
                form.SCOREassistenten +=form.PRODUKTIONassistent
            
            for i in range(anzahlDOS):
                zusatzSCORE += form.PRODUKTIONdos
                form.SCOREdos +=form.PRODUKTIONdos

            for i in range(anzahlServer):
                zusatzSCORE += form.PRODUKTIONserver
                form.SCOREserver +=form.PRODUKTIONserver
            
            for i in range(anzahlMatrix):
                zusatzSCORE += form.PRODUKTIONmatrix
                form.SCOREmatrix +=form.PRODUKTIONmatrix

            form.SCORE += zusatzSCORE















        
app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()























