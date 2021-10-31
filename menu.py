import streamlit as st


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
    # elif option == 'Mostrar contenido de las tablas':

    

with st.container():
    st.subheader("made with ❤️ & 🐍")

#para correr el menú primero instalar streamlit con pip install streamlit
#y luego ejecutar con streamlit run menu.py y se abrirá un liveserver en local 
#por el momento el front-end está desconectado del back-end

