import couchdb

class Itcouch:
    def __init__(self):
        self.couch = couchdb.Server("http://admin:1463@localhost:5984/")

        self.db_name = "botlog"
        if self.db_name in self.couch:
            self.db = self.couch[self.db_name]
        else:
            self.db = self.couch.create(self.db_name)

    def insert(self, json):
        self.doc_id, self.doc_rev = self.db.save(json)
        print(f"Documento guardado con id={self.doc_id} rev={self.doc_rev}")

        self.doc = self.db[self.doc_id]
        print("Documento recuperado:", self.doc)

        self.doc["lenguaje"] = "Ruby on Rails + Python"
        self.db.save(self.doc)

        for id in self.db:
            print("ID:", id, "Contenido:", self.db[id])