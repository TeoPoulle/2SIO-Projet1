from etudes.etude import Etudes

class EtudeDAO:
    def __init__(self, db):
        self.db = db

    def get_all_etudes(self):
        sql = "SELECT * FROM etudes"
        rows = self.db.query(sql)
        etudes = [Etudes(row['id'], row['nomEtu'], row['descEtude'], row['idProtocole'], row['idQuestion'], row['idOrganisme'], row['dateDebEtu'], row['dateFinEtu'], row['idChirResp']) for row in rows]
        return etudes
    
    def get_etude(self, id) :
        sql = "SELECT id, nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp FROM etudes WHERE id=%s"
        row = self.db.query_one(sql, (id,))
        etude = Etudes(row['id'], row['nomEtu'], row['descEtude'], row['idProtocole'], row['idQuestion'], row['idOrganisme'], row['dateDebEtu'], row['dateFinEtu'], row['idChirResp'])
        return etude
    
    """ # A voir plus tard
    def set_etude(self, id, nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp) :
        sql = "UPDATE etudes SET nomEtu = %s, descEtude = %s, idProtocole = %s, idQuestion = %s, idOrganisme = %s, dateDebEtu = %s, dateFinEtu = %s, idChirResp = %s WHERE id = %s"
        parametres = (nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"
    """

    def add_etude(self, nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp) :   
        sql = "INSERT INTO patients (nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        row = self.db.execute(sql, (nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp,))
        return f"{row} ligne(s) concernée(s)"

    def del_etude(self, id) :
        sql = "DELETE FROM etudes WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"
    
    def get_id_etude(self, nomEtu) : 
        sql = "SELECT id FROM etudes WHERE nomEtu=%s"
        row = self.db.query_one(sql, (nomEtu,))
        etude = row['id']
        return etude