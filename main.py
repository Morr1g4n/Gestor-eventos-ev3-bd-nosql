#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()

evento = input("Ingrese nombre de evento: ")
rut = input("Ingrese RUT (con puntos y guión): ")

manager.busqueda_invitado_confirmar_evento(evento, rut)