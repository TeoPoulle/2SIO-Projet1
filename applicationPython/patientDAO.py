from patients import Patients

class PatientDAO:
    def __init__(self, db):
        self.db = db

    def get_all_patients(self):
        sql = "SELECT * FROM patients"
        rows = self.db.query(sql)
        patients = [Patients(row['id'], row['nomPat'], row['prenomPat'], row['dateNaisPat'], row['sexe'], row['numDossierClinique']) for row in rows]
        return patients
    
    def get_patient(self, numDossierClinique) :
        sql = "SELECT id, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique FROM patients WHERE numDossierClinique=%s"
        row = self.db.query_one(sql, (numDossierClinique,))
        patient = Patients(row['id'], row['nomPat'], row['prenomPat'], row['dateNaisPat'], row['sexe'], row['numDossierClinique'])
        return patient
    
    """ # A voir plus tard
    def set_patient(self, id, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) :
        sql = "UPDATE patients SET nomPat = %s, prenomPat = %s, dateNaisPat = %s, sexe = %s, numDossierClinique = %s WHERE id = %s"
        parametres = (nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique, id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"
    """

    def add_patient(self, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) :   
        sql = "INSERT INTO patients (nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) VALUES (%s, %s, %s, %s, %s)"
        row = self.db.execute(sql, (nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique,))
        return f"{row} ligne(s) concernée(s)"

    def del_patient(self, id) :
        sql = "DELETE FROM patients WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"