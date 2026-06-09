#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()

email = input("Ingrese dominio de E-mail a buscar: @")

manager.busqueda_invitado_dominio(email)