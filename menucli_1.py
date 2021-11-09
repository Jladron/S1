from typing_extensions import TypeGuard
import pyodbc
import os

#FUNCIONES AUXILIARES
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")#PARA LINUX
    elif os.name == "dos":
        os.system ("cls")#PARA WINDOWS
        
#Menu para dar de alta un pedido (opcion 2 del menu inicial)
def menu_dar_de_alta_pedido():
    cursor = conexion.cursor

    cursor.execution('SAVEPOINT detalles')

    while not salir_m2:
        print("1.-Añadir detalle de producto")
        print("2.-Eliminar todos los detalles de producto")
        print("3.-Cancelar pedido")
        print("4.-Finalizar pedido")

        opcion_m2 = int(input("INTRODUCE EL NUMERO DE LA OPCION: "))

        
        if opcion_m2 == 1:
            print("opcion 1")
        elif opcion_m2 == 2:
            print("opcion 2")
            cursor.execute('ROLLBACK TO detalles')
        elif opcion_m2 == 3:
            print("opcion 3")
            cursor.execute('ROLLBACK')
            salir_m2 = True
        elif opcion_m2 == 4:
            print("opion 4")
            cursor.execute('COMMIT')
            opcion_m2 = True
        else:
            print("Escribe una opcion correcta")


#CREACION DEL MENU EN LA CONSOLA DE COMANDOS
salir = False

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x4276227;Password=x4276227')

while not salir:
    print("OPCIONES:")
    print("1.-REINICIO")
    print("2.-NUEVO PEDIDO")
    print("3.-MOSTRAR TABLAS")
    print("4.-SALIR")

    opcion = int(input("INTRODUCE EL NUMERO DE LA OPCION: "))
    os.system("clear")
    #SORPRENDENTEMENTE NO EXISTE SWITCH EN PYTHON

    if opcion == 1:
        print("opcion 1")
    elif opcion == 2:
        print("opcion 2")
        salir_m2 = False
        menu_dar_de_alta_pedido()

    elif opcion == 3:
        print("opcion 3")
    elif opcion==4:
        print("opcion 4")
        salir = True
    else:
        print("Escribe una opcion correcta")
    