if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="root",
database="grp03ClinPasteur")

    specialite_dao = specialiteDAO(db)
    specialite = specialite.get_all_specialite()

    for c in specialite:
        print(c)

    db.close()