import pandas as pd
import yfinance as yf
import joblib
import warnings

# Suprimir advertencias
warnings.filterwarnings('ignore', category=Warning)

# Obtención de datos
def obtener_datos_acciones(ticker):
    yesterday = pd.Timestamp.now() - pd.Timedelta(days=1)
    df = yf.download(ticker, start="2000-01-01", end=yesterday)
    if df.empty:
        print(f"Error al obtener datos para {ticker}")
        return None
    df['ticker'] = ticker
    return df

# Predicción
def predecir_mes_siguiente(ticker):

    # Formatear ticker
    ticker = ticker.upper().strip()

    # Obtener los datos del ticker ingresado
    df_ticker = obtener_datos_acciones(ticker)
    if df_ticker is None:
        return None

    # Verificar si las columnas tienen MultiIndex y aplanarlas
    if isinstance(df_ticker.columns, pd.MultiIndex):
        df_ticker.columns = ['_'.join(col).strip() for col in df_ticker.columns]

    # Renombrar las columnas para que sean consistentes con el resto del código
    columnas_renombradas = {
        'Close_'+ticker: 'Close',
        'High_'+ticker: 'High',
        'Low_'+ticker: 'Low',
        'Open_'+ticker: 'Open',
        'Volume_'+ticker: 'Volume'
    }
    df_ticker.rename(columns=columnas_renombradas, inplace=True)

    # Procesar los datos más recientes del ticker
    df_ticker['Date'] = pd.to_datetime(df_ticker.index)
    df_ticker['Month'] = df_ticker['Date'].dt.to_period('M')
    df_monthly_ticker = df_ticker.groupby('Month').agg(
        Open=('Open', 'first'),
        High=('High', 'max'),
        Low=('Low', 'min'),
        Close=('Close', 'last'),
        Volume=('Volume', 'sum')
    ).reset_index()

    # Seleccionar los datos del último mes
    try:
        ultimo_mes = df_monthly_ticker.iloc[-1][['Open', 'High', 'Low', 'Close', 'Volume']]
        print(ultimo_mes)
        ultimo_precio_cierre = df_monthly_ticker.iloc[-1]['Close']

    except IndexError:
        print("No se encontraron datos válidos para el último mes.")
        return None

    # Hacer la predicción
    model = joblib.load("models/regression_model.pkl")
    prediccion = model.predict([ultimo_mes.values])[0]
    variacion_porcentaje = ((prediccion - ultimo_precio_cierre) / ultimo_precio_cierre) * 100

    print(f"\nÚltimo precio de cierre para {ticker}: {ultimo_precio_cierre:.2f}")
    print(f"Predicción para el próximo mes: {prediccion:.2f}")
    print(f"Variación esperada: {variacion_porcentaje:.2f}%")
    return prediccion, variacion_porcentaje
