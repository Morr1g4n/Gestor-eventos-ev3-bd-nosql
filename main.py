#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()

rut = input("Ingrese RUT (con puntos y guión): ")

manager.busqueda_invitado_validar_estado(rut)