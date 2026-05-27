from bdd.database import Database
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication
from interface.interfaceAppli import FenetreAppli
import sys

if __name__ == "__main__":
    try : 
        
        db = Database(host="localhost", user="teo", password="16122004",database="2SIO-Projet1")

        application = QApplication(sys.argv)
        appli = FenetreAppli(db)
        
        appli.show()
        application.exec_()
    
    except Error as e:
        print(f"Erreur : {e}")
    
    finally : 
        db.close()