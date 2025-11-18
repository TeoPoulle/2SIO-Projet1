class Patients:
    def __init__(self, id, nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique):
        self.id = id
        self.nomPat = nomPat
        self.prenomPat = prenomPat
        self.dateNaisPat = dateNaisPat
        self.sexe = sexe
        self.numDossierClinique = numDossierClinique

    def __str__(self):
        return f"{self.id} - {self.nomPat} - {self.prenomPat} - {self.dateNaisPat} - {self.sexe} - {self.numDossierClinique}"