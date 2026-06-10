#Script para poblar base de datos
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.database import Database
from datetime import datetime
import json

DB_NAME = "prueba3_rbeltran"
MONGO_URI = "mongodb://localhost:27017"
COL_EVENTOS = "eventos"
COL_INVITADOS = "invitados"

def DecodificarDateTime(dict): #hook personalizado para la deserialización de json, transforma las fechas en formato ISO que están como string en objetos datetime de python
     #para luego ser insertados por pymongo
     if "fecha" in dict:
          dict["fecha"] = datetime.fromisoformat(dict["fecha"])
     return dict #como "invitados" es un array, también mira los diccionarios de este, entonces si el return va dentro del if pensará que al no haber un campo
     #"fecha" en los diccionarios del array, no debe devolverlo. Por lo tanto, debe ir fuera del if para que los devuelva se cumpla o no la condición

with open('json/eventos.json', encoding='utf-8') as e_json: #sin el encoding los tildes se vuelven caracteres basura
     eventos_json = json.load(e_json, object_hook = DecodificarDateTime) #se añade el hook personalizado

with open ('json/invitados.json', encoding='utf-8') as i_json:
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
     
