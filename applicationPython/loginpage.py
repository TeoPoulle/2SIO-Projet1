import tkinter
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        self.conn = None
        self.cursor = None
        self.connect_info = {'host': host, 'user': user, 'password': password, 'database': database}
        self.connect()

    def connect(self):
        """Tente d'établir la connexion à la base de données."""
        try:
            self.conn = mysql.connector.connect(**self.connect_info)
            if self.conn and self.conn.is_connected():
                print("Connexion MySQL réussie.")
                self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Erreur de connexion : {e}")

    def is_connected(self):
        """Vérifie si la connexion est active."""
        return self.conn is not None and self.conn.is_connected()

    def verify_login(self, email, password):
        if not self.is_connected():
            return None
        
        sql = "SELECT id, role FROM Clients WHERE email = %s AND motDePasse = %s"
        try:
            self.cursor.execute(sql, (email, password))
            resultat = self.cursor.fetchone()
            
            if resultat:
                return resultat
            else:
                return None
        except Error as e:
            print(f"Erreur de vérification de login : {e}")
            return None

    def close(self):
        """Ferme la connexion """
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connexion MySQL fermée.")


HOST = "172.27.0.50" 
USER = "grp03Admin"
PASSWORD = "grp03Mdp"
DATABASE = "grp03ClinPasteur"

db = Database(HOST, USER, PASSWORD, DATABASE) 


def verification_login():
    """Fonction appelée par le bouton 'Connexion'."""
    email = Email_entry.get()
    mot_de_passe = MotDePasse_entry.get()

    if not email or not mot_de_passe:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
        return

    if not db.is_connected():
        messagebox.showerror("Erreur DB", "Impossible de se connecter à la base de données. Vérifiez les identifiants.")
        return
        
    user_info = db.verify_login(email, mot_de_passe)
    
    if user_info:
        role = user_info['role']
        messagebox.showinfo("Succès", f"Connexion réussie ! Bienvenue, {email}. Rôle: {role}.")
        
        if role == 'Medecin':
            print("Ouverture du tableau de bord Médecin.")
            
        elif role == 'Client':
            print("Ouverture de l'interface Client/Patient.")
            
        else:
            print(f"Rôle {role} non géré.")
            
    else:
        messagebox.showerror("Échec", "Email ou mot de passe incorrect.")

Window = tkinter.Tk()
Window.title("Login")
Window.geometry("340x200")

login_label = tkinter.Label(Window, text="Connexion", font=('Arial', 16, 'bold'))
Email_label = tkinter.Label(Window, text="Email :")
Email_entry = tkinter.Entry(Window)
MotDePasse_label = tkinter.Label(Window, text="Mot de passe :")
MotDePasse_entry = tkinter.Entry(Window, show='*')
login_button = tkinter.Button(Window, text="Connexion", command=verification_login) 

login_label.grid(row=0, column=0, columnspan=2, pady=10)
Email_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
Email_entry.grid(row=1, column=1, padx=5, pady=5)
MotDePasse_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
MotDePasse_entry.grid(row=2, column=1, padx=5, pady=5)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

try:
    Window.mainloop()
finally:
    db.close()