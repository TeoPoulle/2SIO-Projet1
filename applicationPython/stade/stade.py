class Stade:
    def __init__(self, id, nomStade):
        self.id = id
        self.nomStade = nomStade

    def __str__(self):
        return f"Stade(ID: {self.id}, Nom: {self.nomStade})"
    
    def __repr__(self):
        return self.__str__()