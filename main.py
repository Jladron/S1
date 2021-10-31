import pyodbc,time

try: 
    conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Host=oracle0.ugr.es;Direct=TRUE;Service Name=practbd.oracle0.ugr.es;User ID=x5569257;Password=x5569257')
    print("Conectado a la base de datos")
    # Aquí continuais vuestro codigo
    csr = conexion.cursor()

    #CONSULTA DE TABLA YA CREADA
    rows = csr.execute("SELECT numero,nombre FROM prueba").fetchall()
    print("Primera consulta:")
    for row in rows:
        print(row[0], row[1])

    #INSERCIÓN DE DATOS EN LA TABLA

    print("\nInsercion y segunda consulta")
    csr.execute("INSERT INTO prueba VALUES (13,'JASON');")
    csr.commit()
    #esperamos unos segundos
    # time.sleep(5)
    #CONSULTA DE NUEVO
    rows = csr.execute("SELECT numero,nombre FROM prueba").fetchall()
    for row in rows:
        print(row[0], row[1])
    #ELIMINAMOS LA ÚLTIMA inserción para dejar la tabla en el mismo estado
    csr.execute("DELETE FROM prueba WHERE numero=13;")
    csr.commit()
    #hacemos la última consulta
    print("\nUltima cosulta:")
    rows = csr.execute("SELECT numero,nombre FROM prueba").fetchall()
    for row in rows:
        print(row[0], row[1])

    #CREACIÓN DE TABLA
    print("\nCreacion de una tabla:")
    csr.execute('''
    CREATE TABLE prueba2(
        numero INT
    );
    ''')
except Exception as ex:
    print(ex)
finally:
    conexion.close()
    print("Desconectado de la base de datos")