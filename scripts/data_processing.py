import yfinance as yf

def obtener_datos_acciones(ticker):
    try:
        datos = yf.download(ticker, period="1y")
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None