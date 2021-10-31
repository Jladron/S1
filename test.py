import pyodbc 

cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es,1521;Service Name=practbd.oracle0.ugr.es;User ID=x5569257;Password=x5569257')
cursor = cnxn.cursor()

#Sample select query
cursor.execute("SELECT * FROM prueba;") 
rows = cursor.fetchall() 
for row in rows: 
    print(row)

#Sample insert query
count = cursor.execute("INSERT INTO prueba VALUES (666,'El numero de la bestia')").rowcount
cnxn.commit()
print('Rows inserted: ' + str(count))

cnxn.close()
