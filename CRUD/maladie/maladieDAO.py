from maladie import Maladies 

class MaladieDAO:
    def __init__(self, db):
        self.db = db

    def get_all_maladies(self):      # Sélection de toutes les maladies
        sql = "SELECT * FROM maladies"
        rows = self.db.query(sql)
        maladies = [Maladies(row['id'], row['nomMaladie']) for row in rows]
        return maladies
    
    def get_maladie(self, id) :         # Sélection d'une maladie précise (en fonction de sa clé primaire)
        sql = "SELECT id, nomMaladie FROM maladies WHERE id=%s" # %s paramètres sécurisés (en gros = même chose que les requêtes préparées en php pdo)
        row = self.db.query_one(sql, (id,))
        maladie = Maladies(row['id'], row['nomMaladie'])
        return maladie
    
    def set_maladie(self, id, nomMaladie) :     # Update du nom de maladie en fonction de l'id
        sql = "UPDATE maladies SET nomMaladie = %s WHERE id = %s"
        parametres = (nomMaladie, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_maladie(self, nomMaladie) :         # Insertion d'une nouvelle maladie
        sql = "INSERT INTO maladies (nomMaladie) VALUES (%s)"
        row = self.db.execute(sql, (nomMaladie,))
        return f"{row} ligne(s) concernée(s)"

    def del_maladie(self, id) :         # Delete une maladie précise
        sql = "DELETE FROM maladies WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"