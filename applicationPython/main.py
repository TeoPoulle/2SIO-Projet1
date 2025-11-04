from database import Database

if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp03Admin", password="grp03Mdp",database="grp03ClinPasteur")
    

    
    db.close()