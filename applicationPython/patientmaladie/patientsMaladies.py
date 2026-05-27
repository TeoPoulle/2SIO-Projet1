from bdd.database import Database 

class PatientsMaladies:
    def __init__(self, id, idPatient, idMaladie, dateDiagnostic, idStade, idOrgane):
        self.id = id
        self.idPatient = idPatient
        self.idMaladie = idMaladie
        self.dateDiagnostic = dateDiagnostic
        self.idStade = idStade
        self.idOrgane = idOrgane

    def __str__(self):
        return f"{self.id} - {self.idPatient} - {self.idMaladie} - {self.dateDiagnostic} - {self.idStade} - {self.idOrgane}"