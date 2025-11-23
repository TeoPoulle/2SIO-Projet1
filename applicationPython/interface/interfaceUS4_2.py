from PyQt5.QtWidgets import QWidget, QPushButton, QCalendarWidget, \
                            QLabel, QLineEdit, QGridLayout, \
                            QComboBox, QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime
from interface.erreurSaisie import ErreurSaisie
from interface.confirmation import Confirmation
from patient.patientDAO import PatientDAO
from maladie.maladieDAO import MaladieDAO
from stade.stadedao import StadeDAO
from organe.organeDAO import OrganeDAO
from patientmaladie.patientsMaladiesDAO import PatientsMaladiesDAO

class InterfaceUS4_2(QWidget) : 
    def __init__(self, db) :
        QWidget.__init__(self)
        self.db = db
        self.maladieDAO = MaladieDAO(self.db)
        self.organeDAO = OrganeDAO(self.db)
        self.stadeDAO = StadeDAO(self.db)
        self.patientDAO = PatientDAO(self.db)
        self.patientMaladieDAO = PatientsMaladiesDAO(self.db)
        self.layout = QGridLayout(self)
        self.initInterface()

    def initInterface(self) :
        # Création des labels des catégories
        self.labelRechPatient = QLabel("Numéro de dossier :")
        self.labelRechMaladie = QLabel("Maladie :")
        self.labelDateDiag = QLabel("Date de diagnostic :")
        self.labelStade = QLabel("Stade de la maladie :")
        self.labelOrgane = QLabel("Organe affecté :")

        # Ajout des labels sur la page
        self.layout.addWidget(self.labelRechPatient, 0, 0)
        self.layout.addWidget(self.labelRechMaladie, 1, 0)
        self.layout.addWidget(self.labelDateDiag, 2, 0)
        self.layout.addWidget(self.labelStade, 4, 0)
        self.layout.addWidget(self.labelOrgane, 5, 0)

        # Création des champs de saisie
        self.rechPatient = QLineEdit("DCL-")
        self.rechMaladie = QComboBox() # Liste déroulante
        self.dateDiag = QCalendarWidget() # Calendrier pour sélectionner la date de diagnostic
        self.dateDiagSelec = QLabel("Date sélectionnée : *vide*")
        self.dateDiagText = QLabel()
        self.rechStade = QComboBox() # Liste déroulante
        self.rechOrgane = QComboBox() # liste déroulante

        # Configuration liste déroulante pour les maladies
        self.rechMaladie.addItem("------")
        self.listeMaladies = self.maladieDAO.get_all_maladies()
        for maladie in self.listeMaladies :
            self.rechMaladie.addItem(maladie.nomMaladie)

        self.rechStade.addItem("------")
        self.listeStades = self.stadeDAO.get_all_stades()
        for stade in self.listeStades : 
            self.rechStade.addItem(stade.nomStade)

        self.rechOrgane.addItem("------")
        self.listeOrganes = self.organeDAO.get_all_organes()
        for organe in self.listeOrganes : 
            self.rechOrgane.addItem(organe.nomOrgane)

        # Ajout des champs de saisie sur la page
        self.layout.addWidget(self.rechPatient, 0, 1)
        self.layout.addWidget(self.rechMaladie, 1, 1)
        self.layout.addWidget(self.dateDiag, 2, 1)
        self.layout.addWidget(self.dateDiagSelec, 3, 1)
        self.layout.addWidget(self.rechStade, 4, 1)
        self.layout.addWidget(self.rechOrgane, 5, 1)

        # Bouton de validation & effet 
        self.dateDiag.clicked.connect(self.afficherDate)

        self.valider = QPushButton("Valider")
        self.layout.addWidget(self.valider, 6, 0, 1, 2)
        self.valider.clicked.connect(self.afficherValidation)


    def afficherDate(self, date) : 
        # Affichage de la date pour l'utilisateur (format DD/MM/YYYY) + stockage dans un label
        dateDiag = date.toString("dd/MM/yyyy")
        self.dateDiagSelec.setText(f"Date sélectionnée : {dateDiag}")
        self.dateDiagText.setText(dateDiag)

    def afficherValidation(self) :
        donneesSaisies = []
        # Récupération des données saisies
        self.infoPatient = self.rechPatient.text()
        self.infoMaladie = self.rechMaladie.currentText()
        self.infoDateDiag = self.dateDiagText.text()
        self.infoStade = self.rechStade.currentText()
        self.infoOrgane = self.rechOrgane.currentText()

        # Vérification que tous les champs sont remplis
        donneesSaisies.append(self.infoPatient)
        donneesSaisies.append(self.infoMaladie)
        donneesSaisies.append(self.infoDateDiag)
        donneesSaisies.append(self.infoStade)
        donneesSaisies.append(self.infoOrgane)

        if "" in donneesSaisies or "------" in donneesSaisies :
            # Objet qui permet d'afficher un message d'erreur
            self.erreur = ErreurSaisie()

        else : 
            # Initiation de la fenêtre de validation
            self.validation = QDialog(self)
            self.validation.setWindowTitle("Confirmation des informations")
            self.validation.resize(400, 200)
            validLayout = QGridLayout()
            self.validation.setLayout(validLayout)

            # Récupération des informations saisies pour confirmation
            patientLabel = QLabel(f"Information patient : {self.patientDAO.get_nom_prenom(self.infoPatient)}, {self.infoPatient}")
            maladieLabel = QLabel(f"Maladie : {self.infoMaladie}")
            dateDiagLabel = QLabel(f"Date de diagnostic : {self.infoDateDiag}")
            stadeLabel = QLabel(f"Stade de la maladie : {self.infoStade}")
            organeLabel = QLabel(f"Organe affecté : {self.infoOrgane}")

            # Affichage des informations saisies pour confirmation
            validLayout.addWidget(patientLabel, 0, 0, 1, 2)
            validLayout.addWidget(maladieLabel, 1, 0, 1, 2)
            validLayout.addWidget(dateDiagLabel, 2, 0, 1, 2)
            validLayout.addWidget(stadeLabel, 3, 0, 1, 2)
            validLayout.addWidget(organeLabel, 4, 0, 1, 2)

            # Boutons OK et Annuler
            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            validLayout.addWidget(buttonBox, 5, 0, 1, 2)
            buttonBox.accepted.connect(lambda: self.accept(self.infoPatient, self.infoMaladie, self.infoDateDiag, self.infoStade, self.infoOrgane))
            buttonBox.rejected.connect(self.validation.reject)
            self.validation.exec()
    
    def accept(self, infoPatient, infoMaladie, infoDateDiag, infoStade, infoOrgane) :
        # Récupération des id et formatage de la date pour l'insertion dans la table patientmaladie
        infoPatient = self.patientDAO.get_id_patient(infoPatient)
        infoMaladie = self.maladieDAO.get_id_maladie(infoMaladie)
        infoDateDiag = datetime.strptime(infoDateDiag, "%d/%m/%Y") # Conversion de str à objet datetime
        infoDateDiag = infoDateDiag.strftime("%Y-%m-%d") # Format compatible avec MySQL
        infoStade = self.stadeDAO.get_id_stade(infoStade)
        infoOrgane = self.organeDAO.get_id_organe(infoOrgane)

        # Insertion dans la table patientmaladie
        self.patientMaladieDAO.add_patientmaladie(infoPatient, infoMaladie, infoDateDiag, infoStade, infoOrgane)

        # Réinitialiation des champs de saisies
        self.rechPatient.clear()
        self.rechMaladie.setCurrentIndex(0)
        self.dateDiag.setSelectedDate(QDate.currentDate())
        self.dateDiagSelec.setText("Date sélectionnée : *vide*")
        self.dateDiagText.setText("")
        self.rechStade.setCurrentIndex(0)
        self.rechOrgane.setCurrentIndex(0)
        self.validation.close()

        # Affichage d'un message de confirmation grâce à la classe Confirmation
        self.confirmation = Confirmation("Le patient malade a été enregistré avec succès.")
    
    def reject(self) :
        self.validation.close()