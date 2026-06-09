#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()

nombre = input("Ingrese nombre, apellido o nombre completo del invitado (incluya tildes): ")

manager.busqueda_invitado_nombre(nombre)