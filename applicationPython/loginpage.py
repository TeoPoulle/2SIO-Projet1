import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta
import sys 

try:
    from etudes_list import EtudesListApp  
except ImportError:
    messagebox.showerror("Erreur Fichier", "Le fichier 'etude_liste.py' est introuvable. Placez-le dans le même dossier.")
    sys.exit()

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
            else:
                 print("Échec de la connexion à la DB.")
        except Error as e:
            print(f"ERREUR DB FATALE: {e}")
            messagebox.showerror("Erreur DB", f"Échec de la connexion: {e}")

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
            messagebox.showerror("Erreur DB", f"Erreur SQL: {e}")
            return False

    def verify_login(self, email, password):
        """Vérifie l'email/mdp. Retourne {'id', 'role'} si succès, sinon None."""
        if not self.is_connected(): return None
        
        sql = "SELECT id, role FROM Clients WHERE email = %s AND motDePasse = %s"
        try:
            self.cursor.execute(sql, (email, password))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Erreur de vérification de login : {e}")
            return None
    
    def set_otp(self, user_id, otp_code, expiration_time):
        expiration_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S') 
        sql = "UPDATE Clients SET otp_code = %s, otp_expiration = %s WHERE id = %s"
        return self.execute(sql, (otp_code, expiration_str, user_id))

    def verify_otp(self, user_id, submitted_otp):
        sql = "SELECT COUNT(*) AS match_count FROM Clients WHERE id = %s AND otp_code = %s AND otp_expiration > NOW()"
        try:
            if not self.is_connected(): return False
            self.cursor.execute(sql, (user_id, submitted_otp))
            result = self.cursor.fetchone()
            
            match = result['match_count'] == 1
            if match:
                self.clear_otp(user_id)
            return match
        except Error as e:
            print(f"Erreur de vérification OTP : {e}")
            return False

    def clear_otp(self, user_id):
        sql = "UPDATE Clients SET otp_code = NULL, otp_expiration = NULL WHERE id = %s"
        self.execute(sql, (user_id,))

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connexion MySQL fermée.")

db = Database(HOST, USER, PASSWORD, DATABASE)

def generate_otp():
    """Génère un code OTP à 6 chiffres."""
    return str(random.randint(100000, 999999))


def open_main_interface(user_info):
    """Ouvre le tableau de bord et affiche le bouton 'études' si c'est un médecin."""
    role = user_info['role']
    print(f"DEBUG: Rôle détecté : '{role}'") 
    print(f"DEBUG: user_info : {user_info}")  
    Window.destroy() 

    app_root = tk.Tk()
    app_root.title(f"Tableau de Bord ({role})")
    app_root.geometry("500x250")
    
    tk.Label(app_root, text=f"Bienvenue, {role}!", font=('Arial', 18, 'bold')).pack(pady=20)
    
    if role == 'medecin':
        print("Rôle 'medecin' détecté. Le bouton d'accès aux études est affiché.")
        
        def open_etudes_list():
            EtudesListApp(app_root, user_info['id']) 
            
        tk.Button(app_root, 
                 text="Voir la liste d'études", 
                 command=open_etudes_list, 
                 font=('Arial', 12, 'bold'),
                 bg='#6A5ACD',
                 fg='white', 
                 padx=10, pady=5).pack(pady=20)
    
    app_root.mainloop()

def open_otp_window(user_id, login_window, user_info):
    """Ouvre une fenêtre Toplevel pour la saisie du code OTP."""
    print("DEBUG: open_otp_window appelée.")  
    otp_window = tk.Toplevel(login_window)
    otp_window.title("Vérification OTP")
    otp_window.geometry("300x180")
    
    
    tk.Label(otp_window, text="Entrez le code OTP reçu (voir console) :", font=('Arial', 10, 'bold')).pack(pady=10)
    otp_entry = tk.Entry(otp_window, show="*", width=20)
    otp_entry.pack(pady=5)

    otp_entry.bind('<Return>', lambda event: submit_otp())

    def on_otp_close():
        """Gère la fermeture de la fenêtre OTP (annulation)."""
        if messagebox.askyesno("Annuler", "Voulez-vous annuler la connexion ?"):
            db.clear_otp(user_id) 
            otp_window.destroy()
            login_window.deiconify() 
    
    otp_window.protocol("WM_DELETE_WINDOW", on_otp_close)

    def submit_otp():
        """Vérifie le code soumis par l'utilisateur."""
        submitted_otp = otp_entry.get().strip()
        
        if db.verify_otp(user_id, submitted_otp):
            otp_window.destroy()
            open_main_interface(user_info) 
        else:
            messagebox.showerror("Échec OTP", "Code incorrect ou expiré.")
            db.clear_otp(user_id) 
            otp_window.destroy()
            login_window.deiconify() 

    tk.Button(otp_window, text="Valider OTP", command=submit_otp).pack(pady=10)
    
    otp_window.update()
    print("DEBUG: otp_window.update() appelée.")  

def verification_login():
    """Fonction appelée par le bouton 'Connexion'."""
    email = Email_entry.get()
    mot_de_passe = MotDePasse_entry.get()

    if not email or not mot_de_passe:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
        return

    if not db.is_connected():
        messagebox.showerror("Erreur DB", "La base de données est inaccessible.")
        return
        
    user_info = db.verify_login(email, mot_de_passe)
    
    if user_info:
        otp_code = generate_otp()
        expiration = datetime.now() + timedelta(minutes=5)
        
        if db.set_otp(user_info['id'], otp_code, expiration):
            
            print(f"--- CODE OTP pour {email} : {otp_code} ---")
            print("Valable jusqu'à :", expiration.strftime('%H:%M:%S'))

            messagebox.showinfo("Vérification OTP", f"Code généré. Consultez votre console.")
            
            Window.withdraw()  
            open_otp_window(user_info['id'], Window, user_info) 
        
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement de l'OTP.")

    else:
        messagebox.showerror("Échec", "Email ou mot de passe incorrect.")

Window = tk.Tk()
Window.title("Connexion 2FA")
Window.geometry("340x200")

login_label = tk.Label(Window, text="Connexion", font=('Arial', 16, 'bold'))
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

try:
    if not db.is_connected():
        print("L'application démarre, mais la DB est inaccessible. La connexion échouera.")
    Window.mainloop()
finally:
    db.close()
