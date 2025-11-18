from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from interfaceUS4_1 import InterfaceUS4_1

class FenetreAppli(QWidget) :
    def __init__(self, db) :
        QWidget.__init__(self)
        self.db = db

        # Fenêtre basique de l'application
        self.resize(1000, 500)
        contenuAppli = QVBoxLayout()
        self.setLayout(contenuAppli)

        # Ajout d'onglets pour faciliter la navigation
        self.onglets = QTabWidget()
        # Onglet correspondant à l'US4_1
        self.ongletUS4_1 = InterfaceUS4_1(self.db)
        self.onglets.addTab(self.ongletUS4_1, "Enregistrer un patient")


        # 
        contenuAppli.addWidget(self.onglets)

        self.setWindowTitle("Clinique Pasteur")


