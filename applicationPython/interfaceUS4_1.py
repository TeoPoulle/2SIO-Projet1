from PyQt5.QtWidgets import QWidget, QPushButton, QCalendarWidget, \
                            QLabel, QLineEdit, QGridLayout, \
                            QRadioButton, QGroupBox, QHBoxLayout, QButtonGroup, \
                            QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime
from patientDAO import PatientDAO

class InterfaceUS4_1(QWidget) : 
    def __init__(self, db) :
        QWidget.__init__(self)
        self.db = db
        self.patientDAO = PatientDAO(self.db)
        self.layout = QGridLayout(self)
        self.initInterface()

    def initInterface(self) :
        # Création des labels des catégories
        self.labelNom = QLabel("Nom du patient :")
        self.labelPrenom = QLabel("Prénom du patient :")
        self.labelDateNais = QLabel("Date de naissance :")
        self.labelSexe = QLabel("Sexe :")
        self.labelNumDossier = QLabel("Numéro de dossier :")

        # Ajout des labels sur la page
        self.layout.addWidget(self.labelNom, 0, 0)
        self.layout.addWidget(self.labelPrenom, 1, 0)
        self.layout.addWidget(self.labelDateNais, 2, 0)
        self.layout.addWidget(self.labelSexe, 4, 0)
        self.layout.addWidget(self.labelNumDossier, 5, 0)

        # Création des champs à remplir
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.dateNais = QCalendarWidget() # Calendrier pour sélectionner la date de naissance du patient
        self.dateNaisSelect = QLabel("Date sélectionnée : *vide*")
        self.dateNaisText = QLabel()
        self.numDossier = QLineEdit("DCL-")
        # Pour définir le sexe du patient
        sexe = QGroupBox()
        sexeLayout = QHBoxLayout(sexe)
        self.sexe = QButtonGroup() 
        self.masculin = QRadioButton("Masculin")
        self.sexe.addButton(self.masculin, 1)
        sexeLayout.addWidget(self.masculin)
        self.feminin = QRadioButton("Féminin")
        self.sexe.addButton(self.feminin, 2)
        sexeLayout.addWidget(self.feminin)
        self.nonBinaire = QRadioButton("Non-binaire")
        self.sexe.addButton(self.nonBinaire, 3)
        sexeLayout.addWidget(self.nonBinaire)
        self.autre = QRadioButton("Autre")
        self.sexe.addButton(self.autre, 4)
        sexeLayout.addWidget(self.autre)
        self.sexeText = QLabel()

        # Ajout des champs sur la page
        self.layout.addWidget(self.nom, 0, 1)
        self.layout.addWidget(self.prenom, 1, 1)
        self.layout.addWidget(self.dateNais, 2, 1)
        self.layout.addWidget(self.dateNaisSelect, 3, 1)
        self.layout.addWidget(sexe, 4, 1)
        self.layout.addWidget(self.numDossier, 5, 1)

        # Pour afficher et obtenir la date sélectionnée
        self.dateNais.clicked.connect(self.afficherDate)
        # Pour obtenir la valeur du bouton sélectionné
        self.sexe.buttonClicked[int].connect(self.afficherSexe)

        # Création du bouton de validation
        self.valider = QPushButton("Valider")
        self.layout.addWidget(self.valider, 6, 0, 1, 2)
        
        # Pour une première validation des informations saisies
        self.valider.clicked.connect(self.afficherValidation)

    def afficherDate(self, date) : 
        # Affichage de la date pour l'utilisateur (format DD/MM/YYYY) + stockage dans un label
        dateNaisPat = date.toString("dd/MM/yyyy")
        self.dateNaisSelect.setText(f"Date sélectionnée : {dateNaisPat}")
        self.dateNaisText.setText(dateNaisPat)

    def afficherSexe(self, id) : 
        # Stocker la valeur du bouton radio correspondant au sexe dans un label
        radioSexe = self.sexe.button(id)
        radioSexeText = radioSexe.text()
        self.sexeText.setText(radioSexeText)
        
    def afficherValidation(self) : 
        # Récupération des données saisies 
        donneesSaisies = []
        self.nomValide = self.nom.text()
        self.prenomValide = self.prenom.text()
        self.dateNaisValidee = self.dateNaisText.text()
        self.sexeValide = self.sexeText.text()
        self.numDossValide = self.numDossier.text()
        # Vérification que tous les champs sont remplis
        donneesSaisies.append(self.nomValide)
        donneesSaisies.append(self.prenomValide)
        donneesSaisies.append(self.dateNaisValidee)
        donneesSaisies.append(self.sexeValide)
        donneesSaisies.append(self.numDossValide)
        if "" in donneesSaisies :
            # Si un champ est vide, on n'ouvre pas la fenêtre de confirmation
            erreurDialog = QDialog(self)
            erreurDialog.setWindowTitle("Erreur de saisie")
            erreurDialog.resize(300, 100)
            erreurLayout = QGridLayout()
            erreurDialog.setLayout(erreurLayout)
            erreurLabel = QLabel("Tous les champs doivent être remplis avant validation.")
            erreurLayout.addWidget(erreurLabel, 0, 0, 1, 2)
            okButton = QDialogButtonBox.Ok
            erreurBox = QDialogButtonBox(okButton)
            erreurLayout.addWidget(erreurBox, 1, 0, 1, 2)
            erreurBox.accepted.connect(erreurDialog.accept)
            erreurDialog.exec()
            return
        
        else :
            # Initiation de la fenêtre de confirmation
            self.validation = QDialog(self)
            self.validation.setWindowTitle("Confirmation des informations saisies")
            self.validation.resize(500, 250)
            validationLayout = QGridLayout()
            self.validation.setLayout(validationLayout)
            # Affichage des données saisies dans la fenêtre de confirmation
            validNom = QLabel(f"Nom : {self.nomValide}")
            validPrenom = QLabel(f"Prénom : {self.prenomValide}")
            validDateNais = QLabel(f"Date de naissance : {self.dateNaisValidee}")
            validSexe = QLabel(f"Sexe : {self.sexeValide}")
            validNumDoss = QLabel(f"Numéro de dossier : {self.numDossValide}")
            # Ajout des champs sur la fenêtre de confirmation
            validationLayout.addWidget(validNom, 0, 0, 1, 2)
            validationLayout.addWidget(validPrenom, 1, 0, 1, 2)
            validationLayout.addWidget(validDateNais, 2, 0, 1, 2)
            validationLayout.addWidget(validSexe, 3, 0, 1, 2)
            validationLayout.addWidget(validNumDoss, 4, 0, 1, 2)
            # Bouton de confirmation 
            confirmButton = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            self.confirmBox = QDialogButtonBox(confirmButton)
            validationLayout.addWidget(self.confirmBox, 5, 0, 1, 2)
            # Connexion des boutons aux fonctions adaptées
            self.confirmBox.accepted.connect(lambda: self.accept(self.nomValide, self.prenomValide, self.dateNaisValidee, self.sexeValide, self.numDossValide)) # 
            self.confirmBox.rejected.connect(self.reject)
            self.validation.exec()

    def accept(self, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) :
        dateNaisPat = datetime.strptime(dateNaisPat, "%d/%m/%Y") # Conversion de str à objet datetime
        dateNaisPat = dateNaisPat.strftime("%Y-%m-%d") # Format compatible avec MySQL
        self.patientDAO.add_patient(nomPat, prenomPat, dateNaisPat, sexe[0], numDossierClinique)
        # Réinitialisation des champs après validation
        self.nom.clear()
        self.prenom.clear()
        self.dateNais.setSelectedDate(QDate.currentDate())
        self.dateNaisSelect.setText("Date sélectionnée : *vide*")
        self.dateNaisText.setText("")
        self.sexe.setExclusive(False)
        self.masculin.setChecked(False)
        self.feminin.setChecked(False)
        self.nonBinaire.setChecked(False)
        self.autre.setChecked(False)
        self.sexe.setExclusive(True)
        self.sexeText.setText("")
        self.numDossier.setText("DCL-")
        self.validation.close()

        self.confirmation = QMessageBox(self)
        self.confirmation.setWindowTitle("Enregistrement réussi")
        self.confirmation.resize(300, 100)
        self.confirmation.setText("Le patient a été enregistré avec succès.")
        self.confirmation.setIcon(QMessageBox.Information)
        self.confirmation.exec()

    def reject(self) :
        self.validation.close()





