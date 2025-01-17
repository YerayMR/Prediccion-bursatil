import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# Cargar un modelo preentrenado (puedes sustituirlo con tu modelo real)
model = LinearRegression()

# Lista de tickers del índice S&P 500 (puedes usar una lista más completa si lo deseas)
sp500_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA']

# Título de la aplicación
st.title("Predicción del precio de acciones del S&P 500")

# Selector desplegable para que el usuario elija una acción
ticker = st.selectbox("Seleccione una acción:", sp500_tickers)

# Botón para ejecutar el procesamiento
if st.button("Ejecutar predicción"):
    # Función para descargar y procesar los datos de una acción
    def obtener_datos_acciones(ticker):
        """Descarga datos históricos de Yahoo Finance y calcula agregados mensuales."""
        try:
            fin = datetime.now()
            inicio = fin - timedelta(days=365 * 5)  # Últimos 5 años
            datos = yf.download(ticker, start=inicio, end=fin)

            # Mostrar los datos descargados
            st.write("Datos descargados:")
            st.dataframe(datos)

            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if datos.empty or not all(column in datos.columns for column in required_columns):
                st.error(f"No se encontraron datos suficientes para el ticker {ticker}.")
                return None, None

            # Asegurarse de que el índice es de tipo datetime
            datos.index = pd.to_datetime(datos.index)
            
            # Agregar una columna de mes y calcular agregados mensuales
            datos['Date'] = datos.index
            datos['Month'] = datos['Date'].dt.to_period('M')
            datos_mensuales = datos.groupby('Month').agg(
                Open=('Open', 'first'),
                High=('High', 'max'),
                Low=('Low', 'min'),
                Close=('Close', 'last'),
                Volume=('Volume', 'sum')
            ).reset_index()
            return datos, datos_mensuales
        except Exception as e:
            st.error(f"Error al obtener datos: {e}")
            return None, None

    # Cargar datos para el ticker seleccionado
    datos_diarios, datos_mensuales = obtener_datos_acciones(ticker)

    if datos_diarios is not None and datos_mensuales is not None:
        # Mostrar precio actual
        precio_actual = datos_diarios['Close'].iloc[-1]
        st.metric("Precio actual de la acción", f"${precio_actual:.2f}")

        # Procesar datos para el modelo
        try:
            # Último mes como entrada para el modelo
            ultimo_mes = datos_mensuales.iloc[-1][['Open', 'High', 'Low', 'Close', 'Volume']]

            # Escalado de datos (ajustar según cómo se entrenó el modelo)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(datos_mensuales[['Open', 'High', 'Low', 'Close', 'Volume']])
            
            # Predecir el próximo mes
            prediccion = model.predict([X_scaled[-1]])[0]
            variacion_porcentaje = ((prediccion - ultimo_mes['Close']) / ultimo_mes['Close']) * 100

            # Mostrar resultados
            st.metric("Precio predicho para el próximo mes", f"${prediccion:.2f}")
            st.write(f"Variación esperada: {variacion_porcentaje:.2f}%")

        except Exception as e:
            st.error(f"Error en la predicción: {e}")

        # Mostrar los datos recientes como tabla
        st.write("Datos recientes de la acción:")
        st.dataframe(datos_diarios.tail(10))
    else:
        st.warning("Seleccione un ticker para mostrar los datos.")
