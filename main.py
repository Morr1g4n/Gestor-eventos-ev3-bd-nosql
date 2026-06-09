#test de conexion e input, se cambiará por un menú

from database.db import MongoManager

manager = MongoManager()


fecha1 = input("Ingrese fecha 1 (AAAA-MM-DD) incluya los guiones: ")
fecha2 = input("Ingrese fecha 2 (AAAA-MM-DD) incluya los guiones (Enter vacío para misma fecha que fecha 1): ")

manager.busqueda_evento_fecha(fecha1, fecha2)