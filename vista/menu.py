from database.db import MongoManager
from readchar import readkey
import subprocess

manager = MongoManager()

class Menu():
    def limpiarconsola(self):
        subprocess.run("cls||clear", shell=True)
    
    def continuar(self):
        print("Presione cualquier tecla para continuar...")
        readkey()
        self.limpiarconsola()

    def menuInicial(self):
        self.limpiarconsola()
        print("-" * 5 + "Buscador Gestor de Eventos" + "-" * 5)
        print("1.- Busquedas Eventos")
        print("2.- Busquedas Invitados")
        print("0.- Salir")
        while True:
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                self.menuEventos()
            elif eleccion == "2":
                self.menuInvitados()
            elif eleccion == "0":
                print("Adios!")
                raise SystemExit
            else:
                print("Seleccione una opción válida.")
    
    def menuEventos(self):
        self.limpiarconsola()
        while True:
            print("-" * 5 + "Buscador Eventos" + "-" * 5)
            print("1.- Buscar por nombre")
            print("2.- Buscar por código")
            print("3.- Buscar por top de cantidad de invitados")
            print("4.- Buscar por rango de fechas")
            print("5.- Busqueda for categoría")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                nombre = input("Ingrese nombre del evento (sin incluír prefijo): ")
                self.limpiarconsola()
                manager.busqueda_evento_nombre(nombre)
                self.continuar()

            elif eleccion == "2":
                codigo = input("Ingrese código del evento: EVT-")
                self.limpiarconsola()
                manager.busqueda_evento_codigo(codigo)
                self.continuar()

            elif eleccion == "3":
                cant = input("Ingrese cantidad de eventos a mostrar: ")
                self.limpiarconsola()
                manager.busqueda_top_eventos(cant)
                self.continuar()

            elif eleccion == "4":
                fecha1 = input("Ingrese primera fecha del rango (fecha menor) (formato AAAA-MM-DD, incluya guiones): ")
                fecha2 = input("Ingrese segunda fecha del rango (fecha mayor) o Enter para usar la misma fecha: ")
                fecha2 = fecha2.strip()
                if not fecha2:
                    fecha2 = fecha1
                self.limpiarconsola()
                manager.busqueda_evento_fecha(fecha1, fecha2)
                self.continuar()
            
            elif eleccion == "5":
                categoria = input("Ingrese categoria: ")
                self.limpiarconsola()
                manager.busqueda_evento_categoria(categoria)
                self.continuar()

            elif eleccion == "0":
                self.menuInicial()

            else:
                print("Seleccione una opción válida.")

    def menuInvitados(self):
        self.limpiarconsola()
        while True:
            print("-" * 5 + "Buscador Invitados" + "-" * 5)
            print("1.- Buscar por nombre (parcial o compelto)")
            print("2.- Buscar por rut")
            print("3.- Buscar por dominio de correo")
            print("4.- Válidar estado por rut")
            print("5.- Revisar estado confirmación a evento")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                nombre = input("Ingrese nombre, apellido o nombre completo (incluya tildes): ")
                self.limpiarconsola()
                manager.busqueda_invitado_nombre(nombre)
                self.continuar()
            
            elif eleccion == "2":
                rut = input("Ingrese rut con puntos y guión: ")
                self.limpiarconsola()
                manager.busqueda_invitado_rut(rut)
                self.continuar()
            
            elif eleccion == "3":
                dominio = input("Ingrese dominio de correo: @")
                self.limpiarconsola()
                manager.busqueda_invitado_dominio(dominio)
                self.continuar()

            elif eleccion == "4":
                rut = input("Ingrese rut con puntos y guión: ") 
                self.limpiarconsola()
                manager.busqueda_invitado_validar_estado(rut)
                self.continuar()
            
            elif eleccion == "5":
                evento = input("Ingrese nombre del evento (sin incluír prefijo): ")
                rut = input("Ingrese rut con puntos y guión: ")
                self.limpiarconsola()
                manager.busqueda_invitado_confirmar_evento(evento, rut)
                self.continuar()

            elif eleccion == "0":
                self.menuInicial()
            
            else:
                print("Seleccione una opción válida.")
