import streamlit as st
from scripts.data_processing import obtener_datos_acciones
from scripts.prediction import predecir_mes_siguiente

# Título de la aplicación
st.title("Predicción de Acciones")

# Input del usuario
ticker = st.text_input("Introduce el ticker de la acción:")

# Botón para realizar la predicción
if st.button("Predecir"):
    if ticker:
        datos = obtener_datos_acciones(ticker)
        if datos is not None:
            st.write("Datos históricos:")
            st.dataframe(datos.tail())
            # Aquí debes cargar un modelo entrenado para usar con predecir_mes_siguiente
            # modelo = cargar_modelo() 
            # prediccion = predecir_mes_siguiente(datos, modelo)
            # st.write(f"Predicción para el próximo mes: {prediccion}")
        else:
            st.error("No se pudieron descargar los datos.")
    else:
        st.error("Por favor, introduce un ticker válido.")
