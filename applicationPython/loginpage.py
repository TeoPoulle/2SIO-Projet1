import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta


HOST = "172.27.0.50" 
USER = "grp03Admin"
PASSWORD = "grp03Mdp"
DATABASE = "grp03ClinPasteur"


class Database:
    """Gère la connexion et les opérations DB."""
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

    def execute(self, sql, params=None):
        """Exécute INSERT, UPDATE, DELETE et commit."""
        if not self.is_connected(): return False
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except Error as e:
            print(f"Erreur d'exécution SQL: {e}")
            return False

    def verify_login(self, email, password):
        """Vérifie l'email/mdp. Retourne {'id', 'role'} si succès, sinon None."""
        if not self.is_connected(): return None
        
        sql = "SELECT id, role FROM Clients WHERE email = %s AND motDePasse = %s"
        try:
            self.cursor.execute(sql, (email, password))
            resultat = self.cursor.fetchone()
            
            return resultat if resultat else None
        except Error as e:
            print(f"Erreur de vérification de login : {e}")
            return None

    # METHODES OTP

    def set_otp(self, user_id, otp_code, expiration_time):
        """Stocke le code OTP et son expiration pour un utilisateur."""
        expiration_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S') 
        sql = "UPDATE Clients SET otp_code = %s, otp_expiration = %s WHERE id = %s"
        return self.execute(sql, (otp_code, expiration_str, user_id))

    def verify_otp(self, user_id, submitted_otp):
        """Vérifie l'OTP soumis contre la valeur stockée et l'heure d'expiration."""
        sql = "SELECT COUNT(*) AS match_count FROM Clients WHERE id = %s AND otp_code = %s AND otp_expiration > NOW()"
        try:
            if not self.is_connected(): return False
            self.cursor.execute(sql, (user_id, submitted_otp))
            result = self.cursor.fetchone()
            
            match = result['match_count'] == 1
            if match:
                self.clear_otp(user_id) # Efface l'OTP après un succès
            return match
        except Error as e:
            print(f"Erreur de vérification OTP : {e}")
            return False

    def clear_otp(self, user_id):
        """Efface les valeurs OTP de la base de données."""
        sql = "UPDATE Clients SET otp_code = NULL, otp_expiration = NULL WHERE id = %s"
        self.execute(sql, (user_id,))

    def close(self):
        """Ferme la connexion et le curseur."""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connexion MySQL fermée.")



db = Database(HOST, USER, PASSWORD, DATABASE)

def generate_otp():
    """Generer un code OTP """
    return str(random.randint(100000, 999999))

def open_main_interface(user_info):
    role = user_info['role']
    # Ferme la fenêtre de login principale
    Window.destroy() 

    # Crée une nouvelle fenêtre simple pour montrer la réussite
    app_root = tk.Tk()
    app_root.title(f"Tableau de Bord ({role})")
    app_root.geometry("400x150")
    
    tk.Label(app_root, text=f"Bienvenue, {role}!", font=('Arial', 18, 'bold')).pack(pady=20)
    tk.Label(app_root, text=f"ID utilisateur: {user_info['id']}").pack()
    
    # Ici, vous lanceriez la classe OrganeManagerApp ou autre interface CRUD
    app_root.mainloop()


def open_otp_window(user_id, login_window, user_info):
    """Ouvre une fenêtre Toplevel pour la saisie du code OTP."""
    otp_window = tk.Toplevel(login_window)
    otp_window.title("Vérification OTP")
    otp_window.geometry("300x180")
    
    tk.Label(otp_window, text="Entrez le code OTP reçu :", font=('Arial', 10, 'bold')).pack(pady=10)
    otp_entry = tk.Entry(otp_window, show="*", width=20)
    otp_entry.pack(pady=5)

    def on_otp_close():
        """Gère la fermeture de la fenêtre OTP (annulation)."""
        if messagebox.askyesno("Annuler", "Voulez-vous annuler la connexion et effacer le code OTP ?"):
            db.clear_otp(user_id) # Efface l'OTP de la DB en cas d'annulation
            otp_window.destroy()
            login_window.deiconify() # Affiche à nouveau la fenêtre de login pour réessayer
    
    otp_window.protocol("WM_DELETE_WINDOW", on_otp_close)

    def submit_otp():
        """Vérifie le code soumis par l'utilisateur."""
        submitted_otp = otp_entry.get().strip()
        
        if db.verify_otp(user_id, submitted_otp):
            messagebox.showinfo("Succès", "OTP validé. Connexion complète.")
            otp_window.destroy()
            open_main_interface(user_info) # Lance l'application principale
            
        else:
            messagebox.showerror("Échec OTP", "Code incorrect ou expiré.")
            db.clear_otp(user_id) # Efface l'OTP en cas d'échec pour forcer la réinitialisation
            otp_window.destroy()
            login_window.deiconify() # Revenir au formulaire de login

    tk.Button(otp_window, text="Valider OTP", command=submit_otp).pack(pady=10)


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
        # --- PHASE 2FA : Génération et Stockage de l'OTP ---
        
        otp_code = generate_otp()
        # Valide pendant 5 minutes
        expiration = datetime.now() + timedelta(minutes=5)
        
        if db.set_otp(user_info['id'], otp_code, expiration):
            
            # Affichage du code dans la console pour le test
            print("----------------------------------------------------------------------")
            print(f"--- ⚠️ CODE OTP (TEST) pour {email} : {otp_code} ---")
            print("Valable jusqu'à :", expiration.strftime('%H:%M:%S'))
            print("----------------------------------------------------------------------")

            messagebox.showinfo("Vérification OTP", f"Code généré. Consultez votre console ou votre email.")
            
            # Masque la fenêtre de login et ouvre la fenêtre OTP
            Window.withdraw() 
            open_otp_window(user_info['id'], Window, user_info) 
        
        else:
            messagebox.showerror("Erreur", "Échec de la préparation OTP (DB non mise à jour?).")

    else:
        messagebox.showerror("Échec", "Email ou mot de passe incorrect.")


Window = tk.Tk()
Window.title("Login sécurisé 2FA")
Window.geometry("340x200")

# Définition et placement des Widgets
login_label = tk.Label(Window, text="Connexion (Étape 1)", font=('Arial', 16, 'bold'))
Email_label = tk.Label(Window, text="Email :")
Email_entry = tk.Entry(Window)
MotDePasse_label = tk.Label(Window, text="Mot de passe :")
MotDePasse_entry = tk.Entry(Window, show='*')
login_button = tk.Button(Window, text="Connexion", command=verification_login) 

login_label.grid(row=0, column=0, columnspan=2, pady=10)
Email_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
Email_entry.grid(row=1, column=1, padx=5, pady=5)
MotDePasse_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
MotDePasse_entry.grid(row=2, column=1, padx=5, pady=5)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# --- 5. BOUCLE PRINCIPALE ET NETTOYAGE ---
try:
    Window.mainloop()
finally:
    db.close()