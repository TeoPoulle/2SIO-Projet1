class Organe:
    def __init__(self, id, nomOrgane):
        self.id = id
        self.nomOrgane = nomOrgane

    def __str__(self):
        return f"Organe(ID: {self.id}, Nom: {self.nomOrgane})"
    
    def __repr__(self):
        return self.__str__()