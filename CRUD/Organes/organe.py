class Organe:
    def __init__(self, id, nom_organe):
        self.id = id
        self.nom_organe = nom_organe

    def __str__(self):
        return f"Organe(ID: {self.id}, Nom: {self.nom_organe})"
    
    def __repr__(self):
        return self.__str__()