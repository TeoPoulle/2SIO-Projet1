class EtatInclusion:
    def __init__(self, id, libelleEtat):
        self.id = id
        self.libelleEtat = libelleEtat

    def __str__(self):
        return f"{self.id} - {self.libelleEtat}"