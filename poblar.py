#Script para poblar base de datos
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.database import Database
import json

DB_NAME = "prueba3_rbeltran"
MONGO_URI = "mongodb://localhost:27017"
COL_EVENTOS = "eventos"
COL_INVITADOS = "invitados"
with open('json/eventos.json') as e_json:
     eventos_json = json.load(e_json)

with open ('json/invitados.json') as i_json:
     invitados_json = json.load(i_json)

def conexion_mongo(uri = MONGO_URI, nombre_bd = DB_NAME) -> Database:
        try:
            cliente = MongoClient(uri, serverSelectionTimeoutMS = 3000)
            cliente.admin.command("ping")
            bd = cliente[nombre_bd]
            return bd
        except ConnectionFailure as error:
            raise RuntimeError(f"No fue posible la conexión: {error}")

def poblar_bd(uri):
     bd = conexion_mongo(uri)
     bd.create_collection("eventos")
     bd.create_collection("invitados")
     bd[COL_EVENTOS].insert_many(eventos_json)
     bd[COL_INVITADOS].insert_many(invitados_json)
     print("Inserción finalizada.\nFavor de revisar que la base de datos e inserciones se hayan hecho correctamente")
     raise SystemExit


def inicializar():
     print(
          'Este script creará una base de datos llamada "prueba3_rbeltran" y las colecciones "eventos" e "invitados"\nEstas colecciones serán pobladas usando los archivos JSON correspondientes.\n'
          )
     while True:
        eleccion = input("¿Continuar?(Y/N): ")
        eleccion = eleccion.lower().replace(" ","")
        if eleccion == "y":
             uri = input("Ingrese URI manualmente o Enter para localhost y puerto default: ")
             uri = uri.strip()
             if not uri:
                  uri = MONGO_URI
             poblar_bd(uri)
        elif eleccion == "n":
             raise SystemExit
        else:
             print("Seleccione una opción válida.")

inicializar()
     
