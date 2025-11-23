from PyQt5.QtWidgets import QWidget, QMessageBox

class Confirmation(QWidget) :
    def __init__(self, message) :
        QWidget.__init__(self)
        self.message = message

        # Permet de mieux voir la fenêtre de confirmation
        style = """QMessageBox {
            border: 1px solid black;
        }"""
        self.setStyleSheet(style)

        # Fenêtre de confirmation
        self.confirmationBox = QMessageBox(self)
        self.confirmationBox.setWindowTitle("Enregistrement réussi")
        self.confirmationBox.setText(message)
        self.confirmationBox.setIcon(QMessageBox.Information)
        self.confirmationBox.setStandardButtons(QMessageBox.Ok)
        self.confirmationBox.exec()