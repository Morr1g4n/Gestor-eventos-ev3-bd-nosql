from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
import re
from tabulate import tabulate #usada para generar tablas dinámicas, da mejores resultados que alineamentos hard codeados

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "prueba3"
COL_EVENTOS = "eventos"
COL_INVITADOS = "invitados"

def conexion_mongo(uri = MONGO_URI, nombre_bd = DB_NAME) -> Database:
        try:
            cliente = MongoClient(uri, serverSelectionTimeoutMS = 3000)
            cliente.admin.command("ping")
            bd = cliente[nombre_bd]
            return bd
        except ConnectionFailure as error:
            raise RuntimeError(f"No fue posible la conexión: {error}")

bd = conexion_mongo()
eventos = bd[COL_EVENTOS]
invitados = bd[COL_INVITADOS]



class MongoManager:
    def busqueda_evento_nombre(self, data):
        try:
            regex = re.compile(f"{data}$")
            cursor = bd[COL_EVENTOS].find({"nombre": regex})
            resultados = list(cursor)
            cursor.close()
            if resultados:
                self.printEvento(resultados)
            else:
                print("No se encontró ningún evento.")
        except Exception as e:
            print(e)
    
    def printEvento(self, lista):
        tabla = []
        headers = ["Codigo", "Nombre", "Fecha", "Lugar", "Categoria"]
        for resultado in lista:
            codigo = str(resultado["codigo"])
            nombre = str(resultado["nombre"])
            fecha = str(resultado["fecha"][0:10])
            lugar = str(resultado["lugar"])
            categoria = str(resultado["categoria"])
            dato = [codigo, nombre, fecha, lugar, categoria]
            tabla.append(dato)
        print(tabulate(tabla, headers=headers))
    #def printEvento(self, lista):
        #print("-" * 140)
        #print("Eventos encontrados:")
        #print(f"{'Codigo':<20}{'Nombre':<20}{'Fecha':<20}{'Lugar':<30}{'Categoria':<20}")
        #for resultado in lista:
            #codigo = str(resultado["codigo"])
            #nombre = str(resultado["nombre"])
            #fecha = str(resultado["fecha"])
            #lugar = str(resultado["lugar"])
            #categoria = str(resultado["categoria"])
            #print(f"{codigo:<20}{nombre:<20}{fecha:<20}{lugar:<20}{categoria:<20}")
        #print("-" * 140)



