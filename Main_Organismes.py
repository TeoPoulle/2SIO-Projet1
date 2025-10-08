if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="root",
database="grp03ClinPasteur")

    Organismes_dao = OrganismesDAO(db)
    Organismes = Organismes.get_all_Organismes()

    for c in Organismes:
        print(c)

    db.close()