from stade import Stade

class StadeDAO:
    def __init__(self, db):
        self.db = db

    def get_all_stades(self):      # Sélection de tous les stades
        sql = "SELECT id, nomStade FROM Stades"
        rows = self.db.query(sql)
        stades = [Stade(row['id'], row['nomStade']) for row in rows]
        return stades
        
    def get_stade(self, id) :         # Sélection d'un stade précis (en fonction de sa clé primaire)
        sql = "SELECT id, nomStade FROM Stades WHERE id=%s" 
        rows = self.db.query(sql, (id,))
        if rows:
            row = rows[0]
            stade = Stade(row['id'], row['nomStade'])
            return stade
        return None
        
    def set_stade(self, id, nomStade) :      # Update du nom du stade en fonction de l'id
        sql = "UPDATE Stades SET nomStade = %s WHERE id = %s"
        parametres = (nomStade, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_stade(self, nomStade) :          # Insertion d'un nouveau stade
        sql = "INSERT INTO Stades (nomStade) VALUES (%s)"
        row = self.db.execute(sql, (nomStade,))
        return f"{row} ligne(s) concernée(s)"

    def del_stade(self, id) :         # Delete un stade précis
        sql = "DELETE FROM Stades WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"