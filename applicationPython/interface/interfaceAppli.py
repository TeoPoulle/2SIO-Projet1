from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from applicationPython.interface.interfaceUS4 import InterfaceUS4

class fenetreAppli(QWidget) :
    def __init__(self) :
        QWidget.__init__(self)

        # Fenêtre basique de l'application
        self.resize(1000, 500)
        contenuAppli = QVBoxLayout()
        self.setLayout(contenuAppli)

        # Ajout d'onglets pour faciliter la navigation
        self.onglets = QTabWidget()
        # Onglet correspondant à l'US4
        self.ongletUS4 = InterfaceUS4()
        self.onglets.addTab(self.ongletUS4, "Enregistrer un patient")


        # 
        contenuAppli.addWidget(self.onglets)

        self.setWindowTitle("Clinique Pasteur")


