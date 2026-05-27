from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
from patientmaladie.patientsMaladiesDAO import PatientsMaladiesDAO

class InterfaceUS14(QWidget):
    def __init__(self, db):
        QWidget.__init__(self)
        self.db = db
        self.patientMaladieDAO = PatientsMaladiesDAO(self.db)
        self.groupeActif = "controle"

        self.layout = QVBoxLayout(self)
        self.initInterface()


    def initInterface(self):
        self.titre = QLabel("Répartition des stades II / III par groupe")
        self.sousTitre = QLabel("Le groupe est déterminé par la parité de l'identifiant patient : \n pair = Test, impair = Contrôle.")

        self.figure = Figure(figsize=(6, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        boutonLigne = QHBoxLayout()
        self.boutonBasculer = QPushButton()
        self.boutonBasculer.clicked.connect(self.basculerGroupe)
        boutonLigne.addWidget(self.boutonBasculer)
        boutonLigne.addStretch(1)

        self.label = QLabel()

        self.layout.addWidget(self.titre)
        self.layout.addWidget(self.sousTitre)
        self.layout.addLayout(boutonLigne)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.label)

        self.actualiserGraphique()

    def basculerGroupe(self): # Permettre le changement du groupe
        if self.groupeActif == "controle" :
            self.groupeActif = "test"
        else : 
            self.groupeActif = "controle"
        self.actualiserGraphique()

    def actualiserGraphique(self):
        repartition = self.patientMaladieDAO.get_repartition_stades_par_groupe()
        donneesGroupe = repartition[self.groupeActif]

        self.figure.clear()
        axe = self.figure.add_subplot(111)

        stages = ["Stade II", "Stade III"]
        valeurs = [donneesGroupe["II"], donneesGroupe["III"]]
        couleurs = ["#2A9D8F", "#E76F51"]

        if sum(valeurs) == 0:
            axe.text(0.5, 0.5, "Aucune donnée disponible pour ce groupe.", ha="center", va="center", fontsize=12)
            axe.set_axis_off()
            self.label.setText(f"Groupe affiché : {self.libelleGroupe(self.groupeActif)} - 0 enregistrements")
            self.boutonBasculer.setText(self.libelleBouton())
            self.canvas.draw()
            return None 

        barres = axe.bar(stages, valeurs, color=couleurs, width=0.55)
        axe.set_title(f"Répartition des stades II / III - {self.libelleGroupe(self.groupeActif)}")
        axe.set_ylabel("Nombre d'enregistrements")
        limiteHaute = max(10, ((max(valeurs) + 9) // 10) * 10)
        axe.set_ylim(0, limiteHaute)
        axe.yaxis.set_major_locator(MultipleLocator(10))
        axe.grid(axis="y", linestyle="--", alpha=0.3)

        for barre in barres:
            hauteur = barre.get_height()
            axe.annotate(
                f"{int(hauteur)}",
                xy=(barre.get_x() + barre.get_width() / 2, hauteur),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

        self.boutonBasculer.setText(self.libelleBouton())
        self.canvas.draw()

    def libelleGroupe(self, groupe):
        if groupe == "test" :
            groupeChoisi = "Test"
        else :
            groupeChoisi = "Contrôle"
        return f"Groupe {groupeChoisi}"

    def libelleBouton(self):
        if self.groupeActif == "test" :
            groupeAffiche = "Test"
        else :
            groupeAffiche = "Contrôle"
        return f"Afficher le groupe {groupeAffiche}"