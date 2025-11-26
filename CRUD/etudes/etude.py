class Etudes:
    def __init__(self, id, nomEtu, descEtude, idProtocole, idQuestion, idOrganisme, dateDebEtu, dateFinEtu, idChirResp):
        self.id = id
        self.nomEtu = nomEtu
        self.descEtude = descEtude
        self.idProtocole = idProtocole
        self.idQuestion = idQuestion
        self.idOrganisme = idOrganisme
        self.dateDebEtu = dateDebEtu
        self.dateFinEtu = dateFinEtu
        self.idChirResp = idChirResp

    def __str__(self):
        return f"{self.id} - {self.nomEtu} - {self.descEtude} - {self.idProtocole} - {self.idQuestion} - {self.idOrganisme} - {self.dateDebEtu} - {self.dateFinEtu} - {self.idChirResp}"