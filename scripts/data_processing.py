import pandas as pd
import yfinance as yf

def obtener_datos_acciones(ticker):
    """
    Descarga datos históricos de una acción usando Yahoo Finance.

    Args:
        ticker (str): Símbolo de la acción.

    Returns:
        pd.DataFrame: Datos de la acción.
    """
    try:
        data = yf.download(ticker)
        return data
    except Exception as e:
        print(f"Error al descargar datos para {ticker}: {e}")
        return None
