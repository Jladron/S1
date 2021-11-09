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
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'SALES';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE Detallepedido';
                END IF;
        END;''')

        cursor.execute('''
        DECLARE cnt NUMBER;
        BEGIN
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'SALES';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE Pedido';
                END IF;
        END;''')

        cursor.execute('''
        DECLARE cnt NUMBER;
        BEGIN
            SELECT COUNT(*) INTO cnt FROM user_tables WHERE table_name = 'SALES';
                IF cnt <> 0 THEN
                    EXECUTE IMMEDIATE 'DROP TABLE Stock';
                END IF;
        END;''')
        print("2")
        #Creamos las 3 tablas
        cursor.execute("CREATE TABLE Stock(Cproducto INT PRIMARY KEY NOT NULL,Cantidad INT)")
        cursor.execute('create table Pedido( Cpedido number(5) primary key, Ccliente number(4) not null, Fechapedido date)')
        cursor.execute('create table Detallepedido( Cproducto constraint Cproducto_clave_externa references Stock(Cproducto), Cpedido constraint Cpedido_clave_externa references Pedido(Cpedido), Cantidad number(4) not null check (status >= 1),constraint clave_primaria primary key (Cproducto ,Cpedido) )')
        print("3")
        #Insertamos las 10 lineas obligatorias en la tabla de Stock
        cursor.execute('insert into Stock values(01, 102);')
        cursor.execute('insert into Stock values(02, 231);')
        cursor.execute('insert into Stock values(03, 350);')
        cursor.execute('insert into Stock values(04, 422);')
        cursor.execute('insert into Stock values(05, 372);')
        cursor.execute('insert into Stock values(06, 564);')
        cursor.execute('insert into Stock values(07, 264);')
        cursor.execute('insert into Stock values(08, 943);')
        cursor.execute('insert into Stock values(09, 120);')
        cursor.execute('insert into Stock values(10, 712);')
        print("4")
        #Hacemos un savepoint
        cursor.execute('SAVEPOINT inicial;')
        # cursor.execute('ROLLBACK TO do_insert;')
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()

# OPCIÓN 2 (MENÚ PRINCIPAL): Dar de alta nuevo pedido

def nuevo_pedido(conexion):

    cursor = conexion.cursor()

    conexion.autocommit = False

    print("Se va a dar de alta un nuevo pedido.")

    conexion.set_savepoint("antes_pedido")

    # Variables correspondientes a las claves primarias
    Cpedido = int(input("Introduzca el código de pedido: "))
    Ccliente = int(input("Introduzca el código de cliente: "))

    try:
        cursor.execute("INSERT INTO Pedido VALUES (" + Cpedido + ", " + Ccliente + ", SYSDATE)")

        print("Pedido creado correctamente.")

    except Exception as ex:
        print("Ha fallado el proceso alta del pedido.")
        conexion.rollback_to("antes_pedido")
    finally:
        conexion.set_savepoint("pedido_creado")
        cursor.close()

def add_detalle(conexion, Cpedido):

    cursor = conexion.cursor()

    conexion.autocommit = False
    
    Cproducto = int(input("Introduzca el código del producto: "))

    stock = 0
    stock = int(cursor.execute("SELECT Cantidad FROM STOCK where STOCK.Cproducto = " + Cproducto))
    print("Stock disponible actualmente: " + str(stock))

    cantidad = int(input("Introduzca la cantidad del producto: ")

    if (stock >= cantidad):
        restante = int(stock - cantidad)
        cursor.execute("UPDATE STOCK SET Cantidad = " + restante + "WHERE STOCK.Cproducto = " + Cproducto)
        cursor.execute("INSERT INTO Detallepedido VALUES ("+Cproducto+", " +Cpedido+", "+cantidad+")")
    
        conexion.set_savepoint("detalles_insertados")
    else:
        print("ERROR: Stock insuficiente. Stock actual: " + stock)

        conexion.rollback_to("pedido_creado")

    conexion.commit()
                   
def mostrar_tablas(conexion):
    csr = conexion.cursor()

    #CONSULTA DE TABLA YA CREADA
    rows = csr.execute("SELECT Cproducto, Cantidad FROM Stock").fetchall()
    print("Tabla stock:")

    print ("{:<10} {:<10}".format('Cod. prod.','cantidad'))
    for row in rows:
        code, cantidad = row
        print ("{:<10} {:<10}".format( code, cantidad))
    
    rows = csr.execute("SELECT Cpedido, Ccliente, Fechapedido FROM Pedido").fetchall()
    print("Tabla Pedidos:")

    print ("{:<10} {:<10} {:<10}".format('Cod. pedido.','Cod. cliente','Fecha-pedido'))
    for row in rows:
        codped, codcli, fecha = row
        print ("{:<10} {:<10} {:<10}".format( codped, codcli,fecha))

    rows = csr.execute("SELECT Cproducto, Cpedido, Cantidad FROM Detallepedido").fetchall()
    print("Tabla Detalle-pedidos:")

    print ("{:<10} {:<10} {:<10}".format('Cod. producto.','Cod. pedido','cantidad'))
    for row in rows:
        codprod, codped, cantidad = row
        print ("{:<10} {:<10} {:<10}".format( codprod, codped,cantidad))
    csr.close()

#MENU

salir = False

#PRIMERO NOS CONECTAMOS A LA BASE DE DATOS
cxn = conexion()


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
        print("opcion 2")
    elif opcion == 3:
        mostrar_tablas(cxn)
    elif opcion==4:
        desconexion(cxn)
        salir = True
    else:
        print("Escribe una opcion correcta")
