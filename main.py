#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()


evento = input("Nombre evento: ")

manager.busqueda_evento_nombre(evento)