from patient.patients import Patients
from pseudonymisation.cryptograph import Crypto
from pseudonymisation.secretKey import secretKey

class PatientDAO:
    def __init__(self, db):
        self.db = db
        self._chiffrement = Crypto(secretKey)

    def get_all_patients(self):
        sql = "SELECT * FROM patients"
        rows = self.db.query(sql)
        patients = [Patients(row['id'], self._chiffrement.decrypt(row['nomPat']), self._chiffrement.decrypt(row['prenomPat']), self._chiffrement.decrypt(row['dateNaisPat']), self._chiffrement.decrypt(row['sexe']), self._chiffrement.decrypt(row['numDossierClinique'])) for row in rows]
        return patients
    
    def get_patient(self, numDossierClinique) :
        sql = "SELECT id, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique FROM patients WHERE numDossierClinique=%s"
        row = self.db.query_one(sql, (self._chiffrement.hash(numDossierClinique),))
        patient = Patients(row['id'], self._chiffrement.decrypt(row['nomPat']), self._chiffrement.decrypt(row['prenomPat']), self._chiffrement.decrypt(row['dateNaisPat']), self._chiffrement.decrypt(row['sexe']), self._chiffrement.decrypt(row['numDossierClinique']))
        return patient
    
    # A voir plus tard
    def set_patient(self, id, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) :
        sql = "UPDATE patients SET nomPat = %s, prenomPat = %s, dateNaisPat = %s, sexe = %s, numDossierClinique = %s WHERE id = %s"
        parametres = (self._chiffrement.encrypt(nomPat), self._chiffrement.encrypt(prenomPat), self._chiffrement.encrypt(dateNaisPat), self._chiffrement.encrypt(sexe), self._chiffrement.hash(numDossierClinique), id)
        row = self.db.execute(sql, parametres)
        return f"{row} ligne(s) affectée(s)"

    def add_patient(self, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) :   
        sql = "INSERT INTO patients (nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) VALUES (%s, %s, %s, %s, %s)"
        row = self.db.execute(sql, (self._chiffrement.encrypt(nomPat), self._chiffrement.encrypt(prenomPat), self._chiffrement.encrypt(dateNaisPat), self._chiffrement.encrypt(sexe), self._chiffrement.hash(numDossierClinique),))
        return f"{row} ligne(s) concernée(s)"

    def del_patient(self, id) :
        sql = "DELETE FROM patients WHERE id=%s"
        row = self.db.execute(sql, (id,))
        return f"{row} ligne(s) concernée(s)"
    
    def get_id_patient(self, numDossierClinique) : 
        sql = "SELECT id FROM patients WHERE numDossierClinique=%s"
        row = self.db.query_one(sql, (self._chiffrement.hash(numDossierClinique),))
        patient = row['id']
        return patient

    def get_nom_prenom(self, numDossierClinique) :
        sql = "SELECT nomPat, prenomPat FROM patients WHERE numDossierClinique=%s"
        row = self.db.query_one(sql, (self._chiffrement.hash(numDossierClinique),))
        nomPrenom = f"{self._chiffrement.decrypt(row['nomPat'])} {self._chiffrement.decrypt(row['prenomPat'])}"
        return nomPrenom