class Maladies:
    def __init__(self, id, nomMaladie):
        self.id = id
        self.nomMaladie = nomMaladie

    def __str__(self):
        return f"{self.id} - {self.nomMaladie}"