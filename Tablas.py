import pyodbc

try: 
    conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x4276227;Password=x4276227')
    print("Conectado a la base de datos")
    # Aquí continuais vuestro codigo

    #The cursor object created by cursor() allows you to execute queries.
    cursor = conexion.cursor()
    
    #Eliminamos las tablas, el orden de eliminacion es crucial debido a que la tabla detalle-pedido contiene referencias a las otras 2 tablas
    cursor.execute('drop table Detalle-pedido; ')
    cursor.execute('drop table Pedido; ')
    cursor.execute('drop table Stock; ')
    
    #Creamos las 3 tablas
    cursor.execute('Create table Stock( Cproducto number(2) primary key, Cantidad number(4)  check (Cantidad >= 1)); ')
    cursor.execute('create table Pedido( Cpedido number(5) primary key, Ccliente number(4) not null, Fecha-pedido date); ')
    cursor.execute('create table Detalle-pedido( Cproducto constraint Cproducto_clave_externa references Stock(Cproducto), Cpedido constraint Cpedido_clave_externa references Pedido(Cpedido), Cantidad number(4) not null check (status >= 1),constraint clave_primaria primary key (Cproducto ,Cpedido) ); ')
    
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

    #Hacemos un savepoint
    cursor.execute('SAVEPOINT inicial;')
    # cursor.execute('ROLLBACK TO do_insert;')
except Exception as ex:
    print(ex)
finally:
    conexion.close()
    print("Desconectado de la base de datos")