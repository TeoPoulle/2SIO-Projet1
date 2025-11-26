from inclusion.inclusion import Inclusion

class InclusionDAO:
    def __init__(self, db):
        self.db = db

    def get_all_inclusions(self):
        sql = "SELECT * FROM inclusions"
        rows = self.db.query(sql)
        inclusions = [Inclusion(row['id'], row['idPatient'], row['dateInclusion'], row['idEtude'], row['idEtat']) for row in rows]
        return inclusions
    
    def get_inclusion(self, id) :
        sql = "SELECT id, idPatient, dateInclusion, idEtude, idEtat FROM inclusions WHERE id=%s"
        row = self.db.query_one(sql, (id,))
        inclusion = Inclusion(row['id'], row['idPatient'], row['dateInclusion'], row['idEtude'], row['idEtat'])
        return inclusion
    
    def add_inclusion(self, idPatient, dateInclusion, idEtude, idEtat) :   
        sql = "INSERT INTO inclusions (idPatient, dateInclusion, idEtude, idEtat) VALUES (%s, %s, %s, %s)"
        row = self.db.execute(sql, (idPatient, dateInclusion, idEtude, idEtat,))
        return f"{row} ligne(s) concernée(s)"
    
    def del_inclusion(self, id) :
        sql = "DELETE FROM inclusions WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"
    
    def set_inclusion(self, id, idPatient, dateInclusion, idEtude, idEtat) :
        sql = "UPDATE inclusions SET idPatient=%s, dateInclusion=%s, idEtude=%s, idEtat=%s WHERE id=%s"
        row = self.db.execute(sql, (idPatient, dateInclusion, idEtude, idEtat, id,))
        return f"{row} ligne(s) concernée(s)"