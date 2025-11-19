import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import sys

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
            self.conn = mysql.connector.connect(self.connect_info)
            if self.conn and self.conn.is_connected():
                print("Connexion MySQL réussie pour l'interface des études.")
                self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Erreur de connexion (etudes_list.py) : {e}", file=sys.stderr)
            messagebox.showerror("Erreur DB", f"Impossible de se connecter pour charger les études : {e}")

    def is_connected(self):
        """Vérifie si la connexion est active."""
        return self.conn is not None and self.conn.is_connected()
    
    def get_available_etudes(self):
        """Récupère les études (nomEtu, descEtude)."""
        if not self.is_connected(): return []
        
        sql = """
        SELECT nomEtu AS nom_de_l_etude, 
               descEtude AS Description, 
               NULL AS Type_de_l_etude,    
               NULL AS Date_de_fin         
        FROM etudes 
        """
        
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erreur de lecture des études : {e}", file=sys.stderr)
            messagebox.showerror("Erreur Requête", f"Erreur lors de la lecture des études : {e}.")
            return []

    def close(self):
        """Ferme la connexion."""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()


class EtudesListApp(tk.Toplevel):
    """Fenêtre qui affiche la liste des études."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Liste des études disponibles")
        self.geometry("800x600")
        
        self.parent = parent 
        self.parent.withdraw() 
        
        self.db = Database(HOST, USER, PASSWORD, DATABASE)
        
        if not self.db.is_connected():
            self.go_back()
            return

        self.create_widgets()
        self.load_etudes()

    def create_widgets(self):
        tk.Label(self, text="Liste des études disponibles", font=('Arial', 24, 'bold')).pack(pady=20)
        
        frame_table = tk.Frame(self)
        frame_table.pack(padx=20, pady=10, fill='both', expand=True)

        columns = ("nom_de_l_etude", "Description", "Type_de_l_etude", "Date_de_fin")
        self.tree = ttk.Treeview(frame_table, columns=columns, show='headings')
        
        self.tree.heading("nom_de_l_etude", text="Nom de l'étude")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Type_de_l_etude", text="Type de l'étude")
        self.tree.heading("Date_de_fin", text="Date de fin")
        
        self.tree.column("nom_de_l_etude", width=150, anchor=tk.W)
        self.tree.column("Description", width=350, anchor=tk.W)
        self.tree.column("Type_de_l_etude", width=100, anchor=tk.CENTER)
        self.tree.column("Date_de_fin", width=100, anchor=tk.CENTER)
        
        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        tk.Button(self, 
                 text="Retour", 
                 command=self.go_back, 
                 bg='#6A5ACD',
                 fg='white', 
                 font=('Arial', 12, 'bold'),
                 width=10).pack(pady=20)
        
        self.protocol("WM_DELETE_WINDOW", self.go_back)

    def load_etudes(self):
        """Charge les études depuis la base de données et les affiche."""
        etudes = self.db.get_available_etudes()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not etudes:
            messagebox.showinfo("Information", "Pour le moment il n'y a aucune étude en cours")
            self.go_back() 

        else:
            for etude in etudes:
                type_etude = etude['Type_de_l_etude'] if etude['Type_de_l_etude'] else "N/A"
                date_fin = etude['Date_de_fin'] if etude['Date_de_fin'] else "N/A"

                self.tree.insert('', tk.END, values=(
                    etude['nom_de_l_etude'], 
                    etude['Description'], 
                    type_etude, 
                    date_fin
                ))

    def go_back(self):
        """Ferme la fenêtre des études et revient au tableau de bord."""
        if self.db.is_connected():
            self.db.close()
        self.parent.deiconify() 
        self.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw() 
    app = EtudesListApp(root)
    root.mainloop()