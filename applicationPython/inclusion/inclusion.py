class Inclusion:
    def __init__(self, id, idPatient, dateInclusion, idEtude, idEtat):
        self.id = id
        self.idPatient = idPatient
        self.dateInclusion = dateInclusion
        self.idEtude = idEtude
        self.idEtat = idEtat
    
    def __str__(self):
        return f"{self.id} - {self.idPatient} - {self.dateInclusion} - {self.idEtude} - {self.idEtat}"
