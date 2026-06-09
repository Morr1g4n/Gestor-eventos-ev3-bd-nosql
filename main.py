#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()


evento = input("Ingrese codigo (XXXX-XXX) EVT-: ")

manager.busqueda_evento_codigo(evento)