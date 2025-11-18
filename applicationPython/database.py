import mysql.connector 

class Database:
    _database = None
    def __new__(cls, host, user, password, database):
        if not cls._database : 
            cls._database = super(Database, cls).__new__(cls)
        else : 
            print("Connexion à la base de données déjà établie, utilisation de la connexion existante.")
        return cls._database

    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True) # Résultats sous forme de dict

    def query(self, sql, params=None): # Quand on a plusieurs enregistrements
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()
    
    def query_one(self, sql, params=None): # Quand on ne cherche qu'un seul enregistrement
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()
    
    def execute(self, sql, params=None) : # Utilisable pour UPDATE, DELETE et INSERT INTO
        self.cursor.execute(sql, params or ())
        self.conn.commit()
        return self.cursor.rowcount # Nb de ligne affectées par les changements

    def close(self):
        self.cursor.close()
        self.conn.close()