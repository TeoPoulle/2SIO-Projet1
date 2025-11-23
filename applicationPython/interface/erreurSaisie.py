from PyQt5.QtWidgets import  QWidget, QDialog, QGridLayout, QLabel, QDialogButtonBox

class ErreurSaisie(QWidget) : 
    def __init__(self) : 
        QWidget.__init__(self)

        # Permet de mieux voir la fenêtre d'erreur
        style = """QDialog {
            border: 1px solid black;
        }"""
        self.setStyleSheet(style)

        # Si un champ est vide, on affiche un message d'erreur
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
