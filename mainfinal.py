import pyodbc
import os

#ANTES DE USAR EL MAIN HE EJECUTADO EL SCRIPT SQL EN MI GESTOR DE BASES DE DATOS PARA TENER TODAS LAS TABLAS CREADAS Y RELLENAS MENOS DETALLE PEDIDO
#FUNCIONES AUXILIARES

def conexion():
    try: 
        conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Host=oracle0.ugr.es;Direct=TRUE;Service Name=practbd.oracle0.ugr.es;User ID=x5569257;Password=x5569257')
        print("Conectado a la base de datos")
    except Exception as ex:
        print(ex)
    finally:
        return conexion

def desconexion(conexion):
    conexion.commit()
    conexion.close()
    print('Desconexion de la base de datos')
    

def reiniciar(conexion):
    try:
        cursor = conexion.cursor()
        # print("1")
        # Eliminamos las tablas, el orden de eliminacion es crucial debido a que la tabla detalle-pedido contiene referencias a las otras 2 tablas
        cursor.execute('''
        DECLARE cnt NUMBER;
        BEGIN
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'DETALLEPEDIDO';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE DETALLEPEDIDO';
                END IF;
        END;''')

        cursor.execute('''
        DECLARE cnt NUMBER;
        BEGIN
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'PEDIDO';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE PEDIDO';
                END IF;
        END;''')

        cursor.execute('''
        DECLARE cnt NUMBER;
        BEGIN
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'STOCK';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE STOCK';
                END IF;
        END;''')
        print("2")
        #Creamos las 3 tablas
        cursor.execute('''
            CREATE TABLE STOCK(
            Cproducto INT PRIMARY KEY NOT NULL,
            Cantidad INT
            )
        ''')
        cursor.execute('''
            CREATE TABLE PEDIDO( 
            Cpedido INT PRIMARY KEY, 
            Ccliente VARCHAR(30) NOT NULL, 
            Fechapedido DATE
            )
        ''')
        cursor.execute('''
            CREATE TABLE DETALLEPEDIDO( 
            Cproducto CONSTRAINT Cproducto_clave_externa REFERENCES Stock(Cproducto), 
            Cpedido CONSTRAINT Cpedido_clave_externa REFERENCES Pedido(Cpedido), 
            Cantidad INT NOT NULL CHECK (Cantidad >= 1),
            CONSTRAINT clave_primaria PRIMARY KEY(Cproducto ,Cpedido)
            )
        ''')
        print("3")
        #Insertamos las 10 lineas obligatorias en la tabla de Stock
        cursor.execute('INSERT INTO Stock VALUES(01, 102);')
        cursor.execute('INSERT INTO Stock VALUES(02, 95);')
        cursor.execute('INSERT INTO Stock VALUES(03, 350);')
        cursor.execute('INSERT INTO Stock VALUES(04, 422);')
        cursor.execute('INSERT INTO Stock VALUES(05, 372);')
        cursor.execute('INSERT INTO Stock VALUES(06, 564);')
        cursor.execute('INSERT INTO Stock VALUES(07, 264);')
        cursor.execute('INSERT INTO Stock VALUES(08, 943);')
        cursor.execute('INSERT INTO Stock VALUES(09, 120);')
        cursor.execute('INSERT INTO Stock VALUES(10, 712);')
        print("4")
        #Hacemos un savepoint
        cursor.execute('SAVEPOINT inicial')
        # cursor.execute('ROLLBACK TO do_insert;')
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()

# OPCIÓN 2 (MENÚ PRINCIPAL): Dar de alta nuevo pedido

def nuevo_pedido(conexion):

    cursor = conexion.cursor()

    # conexion.autocommit = False

    print("Se va a dar de alta un nuevo pedido.")

    conexion.execute("SAVEPOINT antes_pedido")

    # Variables correspondientes a las claves primarias
    Cpedido = input("Introduzca el código de pedido: ")
    Ccliente = input("Introduzca el código de cliente: ")

    try:
        cursor.execute("INSERT INTO PEDIDO VALUES ("+Cpedido+", '"+Ccliente+"', SYSDATE)")

        print("Pedido creado correctamente.")

    except Exception as ex:
        print("las claves son: "+Ccliente+" y "+Cpedido)
        print("Ha fallado el proceso alta del pedido.")
        print(ex)
        
        conexion.execute("ROLLBACK TO SAVEPOINT antes_pedido")
    finally:
        conexion.execute("SAVEPOINT pedido_creado")
        mostrar_tablas(conexion)#hay que mostrar
        menu_dar_de_alta_pedido(conexion,Cpedido)
        cursor.close()

def add_detalle(conexion, Cpedido):

    cursor = conexion.cursor()

    # conexion.autocommit = False
    
    Cproducto = input("Introduzca el código del producto: ")

    print("codigo de producto es: "+Cproducto)

    stock = int((cursor.execute("SELECT Cantidad FROM STOCK where STOCK.Cproducto = "+Cproducto ).fetchall())[0][0])
    print("Stock disponible actualmente: " + str(stock) )

    cantidad = input("Introduzca la cantidad del producto: ")

    if (stock >= int(cantidad)):
        restante = stock - int(cantidad)
        cursor.execute("UPDATE STOCK SET Cantidad = " + str(restante) + "WHERE STOCK.Cproducto = " + Cproducto)
        cursor.execute("INSERT INTO Detallepedido VALUES ("+str(Cproducto)+", " +str(Cpedido)+", "+cantidad+")")
    
        conexion.execute("SAVEPOINT detalles_insertados")
    else:
        print("ERROR: Stock insuficiente. Stock actual: " + str(stock))

        conexion.execute("ROLLBACK TO pedido_creado")
                   
def mostrar_tablas(conexion):
    csr = conexion.cursor()

    #CONSULTA DE TABLA YA CREADA
    rows = csr.execute("SELECT Cproducto, Cantidad FROM Stock").fetchall()
    print("Tabla stock:")

    print ("{:<30} {:<30}".format('Cod. prod.','cantidad'))
    for row in rows:
        code, cantidad = row
        print ("{:<30} {:<30}".format( code, cantidad))
    
    rows = csr.execute("SELECT Cpedido, Ccliente, Fechapedido FROM Pedido").fetchall()
    print("Tabla Pedidos:")

    print ("{:<30} {:<30} {:<30}".format('Cod. pedido.','Cod. cliente','Fecha-pedido'))
    for row in rows:
        codped, codcli, fecha = row
        print ("{:<30} {:<30} {:<30}".format( codped, codcli,str(fecha)))

    rows = csr.execute("SELECT Cproducto, Cpedido, Cantidad FROM Detallepedido").fetchall()
    print("Tabla Detalle-pedidos:")

    print ("{:<30} {:<30} {:<30}".format('Cod. producto.','Cod. pedido','cantidad'))
    for row in rows:
        codprod, codped, cantidad = row
        print ("{:<30} {:<30} {:<30}".format( codprod, codped,cantidad))
    csr.close()

#Menu para dar de alta un pedido (opcion 2 del menu inicial)
def menu_dar_de_alta_pedido(conexion,Cpedido):
    cursor = conexion.cursor()
    cursor.execute('SAVEPOINT detalles')
                   
    salir_m2 = False

    while not salir_m2:
        print("1.-Añadir detalle de producto")
        print("2.-Eliminar todos los detalles de producto")
        print("3.-Cancelar pedido")
        print("4.-Finalizar pedido")

        opcion_m2 = int(input("INTRODUCE EL NUMERO DE LA OPCION: "))

        
        if opcion_m2 == 1:
            print("opcion 1")
            add_detalle(conexion,Cpedido)
        elif opcion_m2 == 2:
            print("opcion 2")
            cursor.execute('ROLLBACK TO detalles')
            print("detalles del pedido eliminado")
            mostrar_tablas(conexion)
        elif opcion_m2 == 3:
            print("opcion 3")
            cursor.execute('ROLLBACK to antes_pedido')
            print("pedido eliminado")
            mostrar_tablas(conexion)
            salir_m2 = True
        elif opcion_m2 == 4:
            print("opion 4")
            cursor.execute('COMMIT')
            mostrar_tablas(conexion)
            salir_m2 = True
        else:
            print("Escribe una opcion correcta")


#MENU

salir = False

#PRIMERO NOS CONECTAMOS A LA BASE DE DATOS
cxn = conexion()
#lo primero que hago es reiniciar la tabla para asegurarme que está en un estado estable
reiniciar(cxn)
os.system("cls")
#ANTES DE METERNOS EN NUESTRO PROGRAMA HAY QUE TENER CREADAS LAS TABLAS


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
        reiniciar(cxn)

    elif opcion == 2:
        nuevo_pedido(cxn)

    elif opcion == 3:
        mostrar_tablas(cxn)

    elif opcion==4:
        desconexion(cxn)
        salir = True
        
    else:
        print("Escribe una opcion correcta")