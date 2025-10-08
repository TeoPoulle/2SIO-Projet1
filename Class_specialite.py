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

class specialite:
    def __init__(self, id_specialite, nom, email):
        self.id_specialite = id_specialite
        self.nom = nom
        self.email = email
    def __str__(self):
        return f"{self.id_specialite} - {self.nom} ({self.email})"

class specialiteDAO:
    def __init__(self, db):
        self.db = db

    def get_all_specialite(self):
        sql = "SELECT * FROM specialite"
        rows = self.db.query(sql)
        specialite = [Organismes(row['id_specialite'], row['nom'], row['email'])
for row in rows]
        return specialite