from patientmaladie.patientsMaladies import PatientsMaladies

class PatientsMaladiesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_patientsmaladies(self):      # Sélection de toutes les patientsmaladies
        sql = "SELECT PM.id, P.nomPat, M.nomMaladie, dateDiagnostic, S.nomStade, O.nomOrgane FROM patientsmaladies AS PM JOIN patients AS P ON P.id = PM.idPatient JOIN maladies AS M ON M.id = PM.idMaladie JOIN stades AS S ON S.id = PM.idStade JOIN organes AS O ON O.id = PM.idOrgane"
        rows = self.db.query(sql)
        patientsmaladies = [PatientsMaladies(row['id'], row['nomPat'], row['nomMaladie'], row['dateDiagnostic'], row['nomStade'], row['nomOrgane']) for row in rows]
        return patientsmaladies
    
    def get_patientmaladie(self, id) :         # Sélection d'un patient  précis atteint d'une maladie précise (en fonction de sa clé primaire)
        sql = "SELECT PM.id, P.nomPat, M.nomMaladie, dateDiagnostic, S.nomStade, O.nomOrgane FROM patientsmaladies AS PM JOIN patients AS P ON P.id = PM.idPatient JOIN maladies AS M ON M.id = PM.idMaladie JOIN stades AS S ON S.id = PM.idStade JOIN organes AS O ON O.id = PM.idOrgane WHERE PM.id=%s" 
        # %s paramètres sécurisés (en gros = même chose que les requêtes préparées en php pdo)
        row = self.db.query_one(sql, (id,))
        patientmaladie = PatientsMaladies(row['id'], row['nomPat'], row['nomMaladie'], row['dateDiagnostic'], row['nomStade'], row['nomOrgane'])
        return patientmaladie
    
    def set_patientmaladie(self, id, idPatient, idMaladie, dateDiagnostic, idStade, idOrgane) :     # Update des données en fonction de l'id
        sql = "UPDATE patientsmaladies SET idPatient = %s, idMaladie = %s, dateDiagnostic = %s, idStade = %s, idOrgane = %s WHERE id = %s"
        parametres = (idPatient, idMaladie, dateDiagnostic, idStade, idOrgane, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_patientmaladie(self, idPatient, idMaladie, dateDiagnostic, idStade, idOrgane) :         # Insertion d'une nouvelle maladie
        sql = "INSERT INTO patientsmaladies (idPatient, idMaladie, dateDiagnostic, idStade, idOrgane) VALUES (%s, %s, %s, %s, %s)"
        row = self.db.execute(sql, (idPatient, idMaladie, dateDiagnostic, idStade, idOrgane,))
        return f"{row} ligne(s) concernée(s)"

    def del_patientmaladie(self, id) :         # Delete une maladie précise
        sql = "DELETE FROM patientsmaladies WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"
    
