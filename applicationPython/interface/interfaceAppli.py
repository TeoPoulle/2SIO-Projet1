from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from interface.interfaceUS4_1 import InterfaceUS4_1
from interface.interfaceUS4_2 import InterfaceUS4_2

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

        self.ongletsUS4_2 = InterfaceUS4_2(self.db)
        self.onglets.addTab(self.ongletsUS4_2, "Enregistrer une maladie par patient")


        # 
        contenuAppli.addWidget(self.onglets)

        self.setWindowTitle("Clinique Pasteur")


