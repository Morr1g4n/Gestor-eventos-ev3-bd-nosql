from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
import re
from tabulate import tabulate #usada para generar tablas dinámicas, da mejores resultados que alineamentos hard codeados

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "prueba3_rbeltran"
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

class MongoManager:

    def busqueda_evento_nombre(self, data):
        try:
            data = data.strip()
            regex = re.compile(f"{data}$", re.IGNORECASE)
            cursor = bd[COL_EVENTOS].find({"nombre": regex})
            resultados = list(cursor) #mete los resultados del cursor dentro de una lista para comprobar si se devolvió algo o no
            #(el objeto Cursor si está vacío seguirá dando True si se comprueba con un if, pero dará False al estar en una lista, pues esta estará vacía)
            cursor.close()
            if resultados: #revisa si hay algo dentro de la lista (True)
                self.printEvento(resultados)
            else:
                print("No se encuentran resultados.")
        except Exception as e:
            print(e)

    def busqueda_evento_codigo(self, data):
        try:
            data = data.strip()
            data = "EVT-" + data #Añade el prefijo "EVT-" a la string
            #print(data) < print debug
            patron_re = re.compile("^(EVT).\\d{4}.\\d{3}$") #El patrón busca el grupo de caracteres "EVT" al inicio del string, los puntos indican cualquier carácter incluidos espacios
            #luego \d busca cualquier carácter númerico y se indica la cantidad de esos carácteres.
            if patron_re.match(data): #compara el string introducido con el patrón de regex para realizar la busqueda, si es incorrecto no se realiza.
                busqueda_re = re.compile(f"^(EVT).{data[4:8]}.{data[9:12]}$")
                #print(busqueda_re) < print debug
                cursor = bd[COL_EVENTOS].find({"codigo": busqueda_re})
                resultados = list(cursor)
                cursor.close()
                if resultados:
                    self.printEvento(resultados)
                else:
                    print("No se encuentran resultados.")
            else:
                print("Formato de código incorrecto, intente nuevamente.")

        except Exception as e:
            print(e)

    def busqueda_invitado_nombre(self, data):
        try:
            data = data.strip()
            regex_nombre = re.compile(f"^{data}", re.IGNORECASE) #se usará para buscar al inicio del string, encontrará solo nombre o nombre completo
            #re.IGNORECASE hace que no sea case sensitive (ignora si es mayuscula o minuscula la busqueda)
            cursor = bd[COL_INVITADOS].find({"nombre": regex_nombre})
            resultados = list(cursor)
            cursor.close()
            if resultados:
                self.printInvitado(resultados)
            else: #intenta busqueda por apellido en caso de no encontrar resultados
                regex_apellido = re.compile(f"{data}$", re.IGNORECASE) #busca al final de la string, encontrará solo apellido o nombre completo
                cursor = bd[COL_INVITADOS].find({"nombre": regex_apellido})
                resultados = list(cursor)
                if resultados:
                    self.printInvitado(resultados)
                else:
                    print("No se encuentran resultados.")
        except Exception as e:
            print(e)
    
    def busqueda_invitado_dominio(self, data):
        try:
            data = data.strip()
            regex_busqueda = re.compile(f"{data}$", re.IGNORECASE) #busca el dominio al final del string, por lo que da igual si se usa @ o no
            cursor = bd[COL_INVITADOS].find({"correo": regex_busqueda})
            resultados = list(cursor)
            cursor.close()
            if resultados:
                self.printInvitado(resultados)
            else:
                print("No se encuentran resultados.")
        except Exception as e:
            print(e)

    def busqueda_invitado_rut(self, data):
        try:
            data = data.strip()
            cursor = bd[COL_INVITADOS].find({"rut": data})
            resultados = list(cursor)
            cursor.close()
            if resultados:
                self.printInvitado(resultados)
            else:
                print("No se encuentran resultados.")
        except Exception as e:
            print(e) 

    def busqueda_invitado_validar_estado(self, data):
        try:
            data = data.strip()
            cursor = bd[COL_INVITADOS].find_one({"rut": data}) #al ser 1 solo resultado, no se agrega a una lista
            if cursor:
                self.printEstado(cursor)
            else:
                print("No se encuentran resultados.")
        except Exception as e:
            print(e)
    
    def busqueda_invitado_confirmar_evento(self, evento, rut):
        try:
            rut = rut.strip()
            re_evento = re.compile(f"{evento}$")
            cursor = bd[COL_EVENTOS].aggregate(
                [
                    {
                        "$unwind": "$invitados"  #deconstruye el array de invitados para que muestre un resultado diferente por cada elemento de este array
                        #será usado para que solo se encuentre un resultado a la hora de hacer el lookup en vez del array entero
                    },
                    {
                        "$match": { #query de busqueda
                            "nombre": re_evento, 
                            "invitados.rut": rut
                        }
                    },
                    {
                        "$lookup": { #crea un campo llamado "invitado" donde estará la información del invitado que se buscó con la información sacada de la colección
                            #invitados, se usará para mostrar el nombre del invitado
                            "from": "invitados",
                            "localField": "invitados.rut",
                            "foreignField": "rut",
                            "as": "datos_invitado"
                        }
                    }
                ]
            )
            resultados = list(cursor)
            cursor.close()
            if resultados:
                self.printConfirmacion(resultados)
            else:
                print("No se encuentran resultados.")
        except Exception as e:
            print(e)

    def busqueda_top_eventos(self, data):
        try:
            data = int(data)
            if data <= 0:
                raise ValueError
            cursor = bd[COL_EVENTOS].aggregate(
                [
                    {
                        "$addFields":{
                            "cant_invitados": {
                                "$size": "$invitados" #añade el campo cant_invitados y le asigna el valor del tamaño del array de invitados (cantidad de elementos en el array)
                            }
                        }
                    },
                    {
                        "$sort":{
                            "cant_invitados": -1 #ordena de forma descendiente según el nuevo campo
                        }
                    },
                    {
                        "$limit": data #limita la cantidad de resultados
                    }
                ]
            )
            resultados = list(cursor)
            if resultados:
                self.printTopEventos(resultados)
            else:
                print("No se encuentran resultados.")
        except ValueError:
            print("Ingrese un válor válido.")
        except Exception as e:
            print(e)

    def printEvento(self, lista):
        tabla = []
        headers = ["Código", "Nombre", "Fecha", "Lugar", "Categoría"]
        for resultado in lista:
            codigo = str(resultado["codigo"])
            nombre = str(resultado["nombre"])
            fecha = str(resultado["fecha"][0:10])
            lugar = str(resultado["lugar"])
            categoria = str(resultado["categoria"])
            dato = [codigo, nombre, fecha, lugar, categoria]
            tabla.append(dato)
        print(tabulate(tabla, headers=headers))

    def printInvitado(self, lista):
        tabla = []
        headers = ["RUT", "Nombre", "Correo", "Empresa", "Estado"]
        for resultado in lista:
            rut = str(resultado["rut"])
            nombre = str(resultado["nombre"])
            correo  = str(resultado["correo"])
            empresa = str(resultado["empresa"])
            estado = str(resultado["estado"])
            dato = [rut, nombre, correo, empresa, estado]
            tabla.append(dato)
        print(tabulate(tabla, headers=headers))
    
    def printConfirmacion(self, lista):
        tabla = []
        headers = ["Código Evento", "Nombre Evento", "RUT", "Nombre Invitado", "Estado Confirmación", "Check-in"]
        for resultado in lista:
            codigo = str(resultado["codigo"])
            nom_evento = str(resultado["nombre"])
            datos_inv = resultado["invitados"] #se hace así y no con un for porque invitados cuenta como un diccionario de diccionarios y no como un array
            #por lo que se debe acceder de forma directa
            rut = str(datos_inv["rut"])
            estado = str(datos_inv["estado"])
            estado = estado.capitalize()
            checkin = datos_inv["checkin"]
            if checkin:
                checkin = "Realizado"
            else:
                checkin = "No realizado"
            for i in resultado["datos_invitado"]:
                nombre = str(i["nombre"])
            dato = [codigo, nom_evento, rut, nombre, estado, checkin] #type: ignore
            tabla.append(dato)
        print(tabulate(tabla, headers=headers))
    
    def printEstado(self, cursor):
        rut = cursor["rut"]
        nombre = cursor["nombre"]
        estado = cursor["estado"]
        estado = estado.capitalize()
        print(f"Estado actual para el invitado '{nombre}' (RUT: {rut}): {estado}")
    
    def printTopEventos(self, lista):
        tabla = []
        headers = ["Código", "Nombre", "Fecha", "Lugar", "Categoría", "Cant. Invitados"]
        for resultado in lista:
            codigo = str(resultado["codigo"])
            nombre = str(resultado["nombre"])
            fecha = str(resultado["fecha"][0:10])
            lugar = str(resultado["lugar"])
            categoria = str(resultado["categoria"])
            cant_invitados = str(resultado["cant_invitados"])
            dato = [codigo, nombre, fecha, lugar, categoria, cant_invitados]
            tabla.append(dato)
        print(tabulate(tabla, headers=headers))
            


    #def printEvento(self, lista):    print con alineamentos manuales, no se usará
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



