import pyodbc
import os

#FUNCIONES AUXILIARES
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")#PARA LINUX
    elif os.name == "dos":
        os.system ("cls")#PARA WINDOWS
        
#CREACION DEL MENU EN LA CONSOLA DE COMANDOS

salir = False

while not salir:
    print("OPCIONES:")
    print("1.-REINICIO")
    print("2.-NUEVO PEDIDO")
    print("3.-MOSTRAR TABLAS")
    print("4.-SALIR")

    opcion = int(input("INTRODUCE EL NUMERO DE LA OPCION: "))
    os.system("cls")
    #SORPRENDENTEMENTE NO EXISTE SWITCH EN PYTHON

    if opcion == 1:
        print("opcion 1")
    elif opcion == 2:
        print("opcion 2")
    elif opcion == 3:
        print("opcion 3")
    elif opcion==4:
        print("opcion 4")
        salir = True
    else:
        print("Escribe una opcion correcta")
    