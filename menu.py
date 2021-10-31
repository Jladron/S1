import streamlit as st
import pyodbc


with st.container():
    st.header("Práctica Sesión 1")
    st.subheader("miniprograma para gestión de pedidos")
    option = st.selectbox('¿Qué quiere hacer?',('Reiniciar programa', 'Dar de alta nuevo pedido', 'Mostrar contenido de las tablas', 'Salir del programa y cerrar sesión'))

    if option == 'Reiniciar programa':
        st.button('Reiniciar')
    elif option == 'Dar de alta nuevo pedido':
        cliente = st.selectbox('Cliente',('Paco','Manolo','Cristina'))
        producto = st.text_input('Producto')
        cantidad = st.number_input('Cantidad',0)
        fecha = st.date_input('Fecha Pedido')
        st.button('Dar de alta')
    elif option == 'Mostrar contenido de las tablas':
        try: 
            conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Host=oracle0.ugr.es;Direct=TRUE;Service Name=practbd.oracle0.ugr.es;User ID=x5569257;Password=x5569257')
            print("Conectado a la base de datos")
            # Aquí continuais vuestro codigo
            csr = conexion.cursor()

            #CONSULTA DE TABLA YA CREADA
            rows = csr.execute("SELECT numero,nombre FROM prueba").fetchall()
            print("Primera consulta:")
            for row in rows:
                st.write(row[0], row[1])

        except Exception as ex:
            print(ex)
        finally:
            conexion.close()
    elif option == 'Salir del programa y cerrar sesión':
        st.button('Cerrar Sesión')

    

with st.container():
    st.subheader("made with ❤️ & 🐍")

#para correr el menú primero instalar streamlit con pip install streamlit
#y luego ejecutar con streamlit run menu.py y se abrirá un liveserver en local 
#por el momento el front-end está desconectado del back-end

