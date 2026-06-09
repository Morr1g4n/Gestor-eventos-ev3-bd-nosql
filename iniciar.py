#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()

cant = input("Ingrese cantidad de eventos a mostrar: ")

manager.busqueda_top_eventos(cant)