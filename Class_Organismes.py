import mysql.connector
class Database:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=grp03ClinPasteur)

    self.cursor = self.conn.cursor(dictionary=True)

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Organismes:
    def __init__(self, id_Organismes, nom, email):
        self.id_Organismes = id_Organismes
        self.nom = nom
        self.email = email
    def __str__(self):
        return f"{self.id_Organismes} - {self.nom} ({self.email})"

class OrganismesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_Organismes(self):
        sql = "SELECT * FROM Organismes"
        rows = self.db.query(sql)
        Organismes = [Organismes(row['id_Organismes'], row['nom'], row['email'])
for row in rows]
        return Organismes