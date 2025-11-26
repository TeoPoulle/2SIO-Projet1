from organe.organe import Organe

class OrganeDAO:
    def __init__(self, db):
        self.db = db

    def get_all_organes(self):      # Sélection de tous les organes
        sql = "SELECT id, nomOrgane FROM organes"
        rows = self.db.query(sql)
        organes = [Organe(row['id'], row['nomOrgane']) for row in rows]
        return organes
        
    def get_organe(self, id) :         # Sélection d'un organe précis (en fonction de sa clé primaire)
        sql = "SELECT id, nomOrgane FROM organes WHERE id=%s" 
        rows = self.db.query(sql, (id,))
        if rows:
            row = rows[0]
            organe = Organe(row['id'], row['nomOrgane'])
            return organe
        return None
        
    def set_organe(self, id, nomOrgane) :      # Update du nom de l'organe en fonction de l'id
        sql = "UPDATE organes SET nomOrgane = %s WHERE id = %s"
        parametres = (nomOrgane, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_organe(self, nomOrgane) :          # Insertion d'un nouvel organe
        sql = "INSERT INTO organes (nomOrgane) VALUES (%s)"
        row = self.db.execute(sql, (nomOrgane,))
        return f"{row} ligne(s) concernée(s)"

    def del_organe(self, id) :         # Delete un organe précis
        sql = "DELETE FROM organes WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"
    
    def get_organe_by_name(self, nomOrgane) :
        sql = "SELECT id, nomOrgane FROM organes WHERE nomOrgane=%s"
        row = self.db.query_one(sql, (nomOrgane,))
        organe = Organe(row['id'], row['nomOrgane'])
        return organe
    
    def get_id_organe(self, nomOrgane) : 
        sql = "SELECT id FROM organes WHERE nomOrgane=%s"
        row = self.db.query_one(sql, (nomOrgane,))
        organe = row['id']
        return organe