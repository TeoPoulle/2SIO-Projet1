from database.py import Database
from maladieDAO.py import MaladieDAO

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp03Admin", password="grp03Mdp",database="grp03ClinPasteur")
    maladies_dao = MaladieDAO(db)
    
    # Test pour get_maladie()
    #print('------------------')
    #getMaladie = maladies_dao.get_maladie(2)
    #print(getMaladie)
    
    # Test pour add_maladie()
    #print('------------------')
    #createdMaladie = maladies_dao.add_maladie('Cancer du cerveau')
    #print(createdMaladie)

    # Test pour set_maladie()
    #print('------------------')
    #updatedMaladie = maladies_dao.set_maladie(6, "Cancer de l'estomac")

    # Test pour del_maladie()
    #print('------------------')
    #deletedMaladie = maladies_dao.del_maladie(6)
    #print(deletedMaladie)

    # Test pour get_all_maladies()
    print('------------------')
    allMaladies = maladies_dao.get_all_maladies()
    for maladie in allMaladies:
        print(maladie)

    db.close()