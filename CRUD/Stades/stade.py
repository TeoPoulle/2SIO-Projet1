class Stade:
    def __init__(self, id, nom_stade):
        self.id = id
        self.nom_stade = nom_stade

    def __str__(self):
        return f"Stade(ID: {self.id}, Nom: {self.nom_stade})"
    
    def __repr__(self):
        return self.__str__()