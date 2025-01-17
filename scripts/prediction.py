def predecir_mes_siguiente(datos, modelo):
    """
    Realiza una predicción para el próximo mes basado en los datos y un modelo.

    Args:
        datos (pd.DataFrame): Datos procesados de la acción.
        modelo (object): Modelo de machine learning entrenado.

    Returns:
        float: Predicción del precio.
    """
    try:
        # Supongamos que el modelo espera un array con [Open, High, Low, Close, Volume]
        ultima_fila = datos.iloc[-1][['Open', 'High', 'Low', 'Close', 'Volume']].values
        prediccion = modelo.predict([ultima_fila])[0]
        return prediccion
    except Exception as e:
        print(f"Error al realizar predicción: {e}")
        return None
