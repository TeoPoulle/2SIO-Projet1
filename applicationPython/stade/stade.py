class Stade:
    def __init__(self, id, nomStade):
        self.id = id
        self.nomStade = nomStade

    def __str__(self):
        return f"Stade(ID: {self.id}, Nom: {self.nomStade})"