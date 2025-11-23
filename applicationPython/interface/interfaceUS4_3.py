from PyQt5.QtWidgets import QWidget, QPushButton, QCalendarWidget, \
                            QLabel, QLineEdit, QGridLayout, \
                            QComboBox, QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime
from interface.erreurSaisie import ErreurSaisie
from interface.confirmation import Confirmation
from patient.patientDAO import PatientDAO
from etudes.etudeDAO import EtudeDAO
from etatinclusion.etatinclusionDAO import EtatInclusionDAO
from inclusion.inclusionDAO import InclusionDAO

# Faire la maquette écran US4.3

class InterfaceUS4_3(QWidget) : 
    def __init__(self, db) :
        QWidget.__init__(self)
        self.db = db
        self.patientDAO = PatientDAO(self.db)
        self.etudeDAO = EtudeDAO(self.db)
        self.etatInclusionDAO = EtatInclusionDAO(self.db)
        self.inclusionDAO = InclusionDAO(self.db)
        self.layout = QGridLayout(self)
        self.initInterface()

    def initInterface(self) :
        # Création des labels des catégories
        self.labelRechPatient = QLabel("Numéro de dossier :")
        self.labelDateInclusion = QLabel("Date d'inclusion :")
        self.labelRechEtude = QLabel("Étude clinique :")
        self.labelRechEtat = QLabel("État de l'étude :")

        # Ajout des labels sur la page
        self.layout.addWidget(self.labelRechPatient, 0, 0)
        self.layout.addWidget(self.labelDateInclusion, 1, 0)
        self.layout.addWidget(self.labelRechEtude, 3, 0)
        self.layout.addWidget(self.labelRechEtat, 4, 0)

        # Création des champs de saisie
        self.rechPatient = QLineEdit("DCL-")
        self.dateInclusion = QCalendarWidget() # Calendrier pour sélectionner la date d'inclusion
        self.dateInclusionSelec = QLabel("Date sélectionnée : *vide*")
        self.dateInclusionText = QLabel()
        self.rechEtude = QComboBox() # Liste déroulante
        self.rechEtat = QComboBox() # Liste déroulante

        # Configuration liste déroulante pour les études cliniques
        self.rechEtude.addItem("------")
        self.listeEtudes = self.etudeDAO.get_all_etudes()
        for etude in self.listeEtudes :
            self.rechEtude.addItem(etude.nomEtu)

        # Configuration liste déroulante pour les états d'inclusion
        self.rechEtat.addItem("------")
        self.listeEtat = self.etatInclusionDAO.get_all_etats()
        for etat in self.listeEtat :
            self.rechEtat.addItem(etat.libelleEtat)

        # Ajout des champs sur la page
        self.layout.addWidget(self.rechPatient, 0, 1)
        self.layout.addWidget(self.dateInclusion, 1, 1)
        self.layout.addWidget(self.dateInclusionSelec, 2, 1)
        self.layout.addWidget(self.rechEtude, 3, 1)
        self.layout.addWidget(self.rechEtat, 4, 1)

        # Pour le calendrier
        self.dateInclusion.clicked.connect(self.afficherDate)

        # Bouton de validation
        self.boutonValider = QPushButton("Valider")
        self.boutonValider.clicked.connect(self.afficherValidation)
        self.layout.addWidget(self.boutonValider, 5, 0, 1, 2)

    def afficherDate(self, date) : 
        # Affichage de la date pour l'utilisateur (format DD/MM/YYYY) + stockage dans un label
        dateInclusion = date.toString("dd/MM/yyyy")
        self.dateInclusionSelec.setText(f"Date sélectionnée : {dateInclusion}")
        self.dateInclusionText.setText(dateInclusion)

    def afficherValidation(self) : 
        donneesSaisies = []
        # Récupération des données saisies
        self.infoPatient = self.rechPatient.text()
        self.infoDateInclusion = self.dateInclusionText.text()
        self.infoEtude = self.rechEtude.currentText()
        self.infoEtat = self.rechEtat.currentText()

        # Vérification que tous les champs sont renseignés
        donneesSaisies.append(self.infoPatient)
        donneesSaisies.append(self.infoDateInclusion)
        donneesSaisies.append(self.infoEtude)
        donneesSaisies.append(self.infoEtat)

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
            dateInclusionLabel = QLabel(f"Date d'inclusion : {self.infoDateInclusion}")
            etudeLabel = QLabel(f"Étude clinique : {self.infoEtude}")
            etatLabel = QLabel(f"État d'inclusion : {self.infoEtat}")

            # Affichage des information de saisies pour confirmation
            validLayout.addWidget(patientLabel, 0, 0)
            validLayout.addWidget(dateInclusionLabel, 1, 0)
            validLayout.addWidget(etudeLabel, 2, 0)
            validLayout.addWidget(etatLabel, 3, 0)

            # Boutons OK et Annuler
            self.boutonsValidation = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            self.boutonsValidation.accepted.connect(lambda: self.accept(self.infoPatient, self.infoDateInclusion, self.infoEtude, self.infoEtat))
            self.boutonsValidation.rejected.connect(self.reject)
            validLayout.addWidget(self.boutonsValidation, 4, 0)
            self.validation.exec()

    def accept(self, infoPatient, infoDateInclusion, infoEtude, infoEtat) :
        # Récupération des IDs nécessaires pour l'insertion
        infoPatient = self.patientDAO.get_id_patient(infoPatient)
        infoDateInclusion = datetime.strptime(infoDateInclusion, "%d/%m/%Y") # Conversion de str à objet datetime
        infoDateInclusion = infoDateInclusion.strftime("%Y-%m-%d") # Format compatible avec MySQL
        infoEtude = self.etudeDAO.get_id_etude(infoEtude)
        infoEtat = self.etatInclusionDAO.get_id_etat(infoEtat)

        # Insertion dans la table inclusion
        self.inclusionDAO.add_inclusion(infoPatient, infoDateInclusion, infoEtude, infoEtat)

        # Réinitialisation des champs de saisie
        self.rechPatient.setText("DCL-")
        self.dateInclusion.setSelectedDate(QDate.currentDate())
        self.dateInclusionSelec.setText("Date sélectionnée : *vide*")
        self.dateInclusionText.setText("")
        self.rechEtude.setCurrentIndex(0)
        self.rechEtat.setCurrentIndex(0)
        self.validation.close()

        # Affichage d'un message de confirmation grâce à la classe Confirmation
        self.confirmation = Confirmation("Le patient malade a été inclu dans cette étude avec succès.")
    
    def reject(self) :
        self.validation.close()