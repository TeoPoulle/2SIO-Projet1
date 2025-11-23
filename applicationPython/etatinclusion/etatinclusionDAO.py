from etatinclusion.etatinclusion import EtatInclusion

class EtatInclusionDAO:
    def __init__(self, db):
        self.db = db

    def get_all_etats(self):      # Sélection de toutes les états d'inclusion
        sql = "SELECT * FROM etatinclusion"
        rows = self.db.query(sql)
        etat = [EtatInclusion(row['id'], row['libelleEtat']) for row in rows]
        return etat
    
    def get_etat(self, id) :         # Sélection d'un état précis (en fonction de sa clé primaire)
        sql = "SELECT id, libelleEtat FROM etatinclusion WHERE id=%s" # %s paramètres sécurisés (en gros = même chose que les requêtes préparées en php pdo)
        row = self.db.query_one(sql, (id,))
        etat = EtatInclusion(row['id'], row['libelleEtat'])
        return etat
    
    def set_etat(self, id, libelleEtat) :     # Update d'un état en fonction de l'id
        sql = "UPDATE etatinclusion SET libelleEtat = %s WHERE id = %s"
        parametres = (libelleEtat, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_etat(self, libelleEtat) :         # Insertion d'un nouvel état
        sql = "INSERT INTO etatinclusion (libelleEtat) VALUES (%s)"
        row = self.db.execute(sql, (libelleEtat,))
        return f"{row} ligne(s) concernée(s)"

    def del_etat(self, id) :         # Delete un état précis
        sql = "DELETE FROM etatinclusion WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"

    def get_etat_by_name(self, libelleEtat) :
        sql = "SELECT id, libelleEtat FROM etatinclusion WHERE libelleEtat=%s"
        row = self.db.query_one(sql, (libelleEtat,))
        etat = EtatInclusion(row['id'], row['libelleEtat'])
        return etat
    
    def get_id_etat(self, libelleEtat) : 
        sql = "SELECT id FROM etatinclusion WHERE libelleEtat=%s"
        row = self.db.query_one(sql, (libelleEtat,))
        etat = row['id']
        return etat