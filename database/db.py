from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "prueba3"
COL_EVENTOS = "eventos"
COL_INVITADOS = "invitados"

class MongoManager:
    bd = None
    invitados = bd[COL_INVITADOS] #type: ignore
    eventos = bd[COL_EVENTOS] #type: ignore

    def conexion_mongo(self, uri = MONGO_URI, bd = DB_NAME):
        try:
            cliente = MongoClient(uri, serverSelectionTimeoutMS = 3000)
            cliente.admin.command("ping")
            MongoManager.bd = cliente[bd]
        except ConnectionFailure as error:
            raise RuntimeError(f"No fue posible la conexión: {error}")
    
    def busqueda_evento_nombre(self, data):
        cursor = self.eventos.find({""})
