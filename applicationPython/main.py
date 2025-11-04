from donnees.database import Database
from mysql.connector import Error

if __name__ == "__main__":
    try : 
        db = Database(host="172.27.0.50", user="grp03Admin", password="grp03Mdp",database="grp03ClinPasteur")
    
    except Error as e:
        print(f"Erreur : {e}")
    
    finally : 
        db.close()