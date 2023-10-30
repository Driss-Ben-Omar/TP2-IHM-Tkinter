import sqlite3

connexion=sqlite3.connect("scolarite.db")

curseur = connexion.cursor()

class Etudiant:
    def createBaseDonnee(self) :
        curseur.execute("""
        CREATE TABLE IF NOT EXISTS etudiant(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, 
        email TEXT,
        phone TEXT,
        id_filiere INTEGER,
        FOREIGN KEY(id_filiere) REFERENCES filiere(id)
        )
        """)
        curseur.execute("""
            CREATE TABLE IF NOT EXISTS module (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            domaine TEXT
        )
        """)
        curseur.execute("""
            CREATE TABLE IF NOT EXISTS filiere (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            departement TEXT
        )
        """)

        curseur.execute("""
            CREATE TABLE IF NOT EXISTS ModulesEtudiants (
            id_module INTEGER,
            id_etudiant INTEGER,
            FOREIGN KEY (id_module) REFERENCES module (id),
            FOREIGN KEY (id_etudiant) REFERENCES etudiant (id)
        )
        """)
        curseur.execute("""
            CREATE TABLE IF NOT EXISTS ModulesFilieres (
            id_module INTEGER,
            id_filiere INTEGER,
            FOREIGN KEY (id_module) REFERENCES module (id),
            FOREIGN KEY (id_filiere) REFERENCES filiere (id)
        )
        """)

        print("creation d'etudiant")

        connexion.commit()

    def __init__(self, id, name, email,phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone= phone
    def insertEtudiant(self, name, email,phone,id_filiere,modules) :
        curseur.execute("""INSERT INTO etudiant (name,email,phone,id_filiere) VALUES (?,?,?,?)""",(name,email,phone,id_filiere))

        id_etudiant = curseur.lastrowid
        if modules!=None:
            for id_module in modules:
                curseur.execute("""INSERT INTO ModulesEtudiants (id_etudiant, id_module) VALUES (?, ?)""", (id_etudiant, id_module))
        print("insert etudiant")

        connexion.commit()
    def deleteEtudiant(self, id) :
        curseur.execute("""DELETE FROM etudiant WHERE id = ?""", (id,))
        curseur.execute("""DELETE FROM ModulesEtudiants WHERE id_etudiant = ?""", (id,))
        connexion.commit()
    
    def updateEtudiant(self, id, name, email,phone,id_filiere,modules) :
        curseur.execute("""
        UPDATE etudiant 
        SET name=?,email=?,phone=?, id_filiere=?
        WHERE id=?""",(name,email,phone,id_filiere,id))

        curseur.execute("""DELETE FROM ModulesEtudiants WHERE id_etudiant = ?""", (id,))
        if modules!=None:
            for id_module in modules:
                curseur.execute("""INSERT INTO ModulesEtudiants (id_etudiant, id_module) VALUES (?, ?)""", (id, id_module))
        connexion.commit()
    
    def readEtudiants(self) :
        result = curseur.execute("""SELECT * FROM etudiant """).fetchall()
        connexion.commit()
        return result
    def readRaltionWithModule(self):
        result=curseur.execute("""SELECT * FROM ModulesEtudiants""").fetchall()
        connexion.commit()
        return result

class Module:
    def __init__(self, id,name, domaine):
        self.id = id
        self.name = name
        self.domaine = domaine

    def insertModule(self, name, domaine,etudiants,filieres) :
        curseur.execute("""INSERT INTO module (name,domaine) VALUES (?,?)""",(name,domaine))

        id_module = curseur.lastrowid
        if etudiants!=None:
            for id_etudiant in etudiants:
                curseur.execute("""INSERT INTO ModulesEtudiants (id_etudiant, id_module) VALUES (?, ?)""", (id_etudiant, id_module))
        if filieres!=None:
            for id_filiere in filieres:
                curseur.execute("""INSERT INTO ModulesFilieres (id_filiere, id_module) VALUES (?, ?)""", (id_filiere, id_module))
        
        print("insert module")

        connexion.commit()

    def deleteModule(self, id) :
        curseur.execute("""DELETE FROM module WHERE id = ?""", (id,))
        curseur.execute("""DELETE FROM ModulesEtudiants WHERE id_module = ?""", (id,))
        curseur.execute("""DELETE FROM ModulesFilieres WHERE id_module = ?""", (id,))
        connexion.commit()
    
    def updateModule(self, id, name, domaine,etudiants,filieres) :
        curseur.execute("""
        UPDATE module 
        SET name=?,domaine=?
        WHERE id=?""",(name,domaine,id))

        curseur.execute("""DELETE FROM ModulesEtudiants WHERE id_module = ?""", (id,))
        curseur.execute("""DELETE FROM ModulesFilieres WHERE id_module = ?""", (id,))
        if etudiants!=None:
            for id_etudiant in etudiants:
                curseur.execute("""INSERT INTO ModulesEtudiants (id_etudiant, id_module) VALUES (?, ?)""", (id_etudiant,id))
        if filieres!=None:
            for id_filiere in filieres:
                curseur.execute("""INSERT INTO ModulesFilieres (id_filiere, id_module) VALUES (?, ?)""", (id_filiere,id))
        connexion.commit()
    
    def readModules(self) :
        result = curseur.execute("""SELECT * FROM module """).fetchall()
        connexion.commit()
        return result
    def readRaltionWithEtudiant(self):
        result=curseur.execute("""SELECT * FROM ModulesEtudiants""").fetchall()
        connexion.commit()
        return result
    def readRaltionWithFiliere(self):
        result=curseur.execute("""SELECT * FROM ModulesFilieres""").fetchall()
        connexion.commit()
        return result
class Filiere:
    def __init__(self, id,name, departement):
        self.id = id
        self.name = name
        self.departement = departement
    def insertFiliere(self, name, departement ,modules) :
        curseur.execute("""INSERT INTO filiere (name,departement) VALUES (?,?)""",(name,departement))

        id_filiere = curseur.lastrowid
        if modules!=None:
            for id_module in modules:
                curseur.execute("""INSERT INTO ModulesFilieres (id_filiere, id_module) VALUES (?, ?)""", (id_filiere, id_module))
        print("insert filiere")

        connexion.commit()

    def deleteFiliere(self, id) :
        curseur.execute("""DELETE FROM filiere WHERE id = ?""", (id,))
        curseur.execute("""DELETE FROM ModulesFilieres WHERE id_filiere = ?""", (id,))
        connexion.commit()
    
    def updateFiliere(self, id, name, departement ,modules) :
        curseur.execute("""
        UPDATE filiere 
        SET name=?,departement=?
        WHERE id=?""",(name,departement,id))

        curseur.execute("""DELETE FROM ModulesFilieres WHERE id_filiere = ?""", (id,))
        if modules!=None:
            for id_module in modules:
                curseur.execute("""INSERT INTO ModulesFilieres (id_filiere, id_module) VALUES (?, ?)""", (id,id_module))
        connexion.commit()
    
    def readFilieres(self) :
        result = curseur.execute("""SELECT * FROM filiere """).fetchall()
        connexion.commit()
        return result
    def readRaltionWithModule(self):
        result=curseur.execute("""SELECT * FROM ModulesFilieres""").fetchall()
        connexion.commit()
        return result

if __name__ == "__main__" :
    e=Etudiant(12,"driss","driss@gmail.com","+212 6666666")
    # e.deleteEtudiant(2)
    e.createBaseDonnee()
    # list=e.readEtudiants()
    # for i in list:
    #     print(i)
    # e.insertEtudiant("driss","driss@gmail.com","+212 6666666",None,None)
    # list=e.readEtudiants()
    # for i in list:
    #     print(i)
    # e.updateEtudiant(2,"driss","driss@gmail.com","+212 77777",None)
    m=Module(2,"ML","IT")
    # m.insertModule("ML","IT",[2,3],None)
    # # m.deleteModule(1)
    # list=m.readRaltionWithEtudiant()
    # for i in list:
    #     print(i)
    f=Filiere(2,"QL","informatique")
    # f.insertFiliere("QL","informatique",[1,2,3])
    f.deleteFiliere(2)
    list=f.readRaltionWithModule()
    for i in list:
        print(i)
