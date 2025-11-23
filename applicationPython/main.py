from bdd.database import Database
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication
from interface.interfaceAppli import FenetreAppli
import sys

if __name__ == "__main__":
    try : 
        
        db = Database(host="172.27.0.50", user="grp03Admin", password="grp03Mdp",database="grp03ClinPasteur")

        application = QApplication(sys.argv)
        appli = FenetreAppli(db)
        
        appli.show()
        application.exec_()
    
    except Error as e:
        print(f"Erreur : {e}")
    
    finally : 
        db.close()