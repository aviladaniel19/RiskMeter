"""
train_model.py — Script de entrenamiento para el Módulo de Machine Learning.

Este script:
1. Descarga datos históricos de activos de referencia.
2. Calcula indicadores técnicos (Features).
3. Genera etiquetas de supervisión (Target: 0=Sell, 1=Hold, 2=Buy).
4. Entrena un Random Forest Classifier.
5. Guarda el artefacto en app/static/trading_model.joblib.
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Asegurar que el directorio raíz del backend esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.api_client import descargar_precios
from app.services.indicators import rsi, macd, bollinger_bands, sma

def generar_features(precios_serie: pd.Series):
    """Genera el conjunto de variables independientes (X)."""
    df = pd.DataFrame({"close": precios_serie})
    
    # Indicadores Técnicos
    df["rsi"] = rsi(df["close"])
    macd_data = macd(df["close"])
    df["macd"] = macd_data["MACD"]
    df["macd_hist"] = macd_data["Histograma"]
    
    bb = bollinger_bands(df["close"])
    df["bb_width"] = (bb["Superior"] - bb["Inferior"]) / bb["Media"]
    
    df["sma_dist"] = (df["close"] - sma(df["close"], 20)) / df["close"]
    
    # Volatilidad y retornos
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=20).std()
    
    return df.dropna()

def generar_target(precios_serie: pd.Series, horizon=5, threshold=0.015):
    """
    Genera la variable dependiente (y).
    2: BUY (Retorno futuro > threshold)
    0: SELL (Retorno futuro < -threshold)
    1: HOLD (En medio)
    """
    future_returns = precios_serie.shift(-horizon) / precios_serie - 1
    
    target = pd.Series(1, index=precios_serie.index) # Default Hold
    target[future_returns > threshold] = 2 # Buy
    target[future_returns < -threshold] = 0 # Sell
    
    return target

def main():
    print("Iniciando entrenamiento del modelo de ML...")
    
    tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NFLX", "META", "NVDA"]
    all_data_x = []
    all_data_y = []
    
    for t in tickers:
        try:
            print(f"Descargando datos para {t}...")
            precios_df = descargar_precios([t], periodo="5y")
            serie = precios_df[t]
            
            X = generar_features(serie)
            y = generar_target(serie).loc[X.index]
            
            # Quitar las últimas 'horizon' filas porque no tienen target real
            X = X.iloc[:-5]
            y = y.iloc[:-5]
            
            all_data_x.append(X)
            all_data_y.append(y)
        except Exception as e:
            print(f"Error con {t}: {e}")

    if not all_data_x:
        print("No se pudieron obtener datos para el entrenamiento.")
        return

    X_full = pd.concat(all_data_x)
    y_full = pd.concat(all_data_y)
    
    # Features finales para el modelo
    feature_cols = ["rsi", "macd", "macd_hist", "bb_width", "sma_dist", "returns", "volatility"]
    X_train_final = X_full[feature_cols]

    # Split Temporal (80% entrenamiento, 20% prueba)
    split = int(len(X_train_final) * 0.8)
    X_train, X_test = X_train_final.iloc[:split], X_train_final.iloc[split:]
    y_train, y_test = y_full.iloc[:split], y_full.iloc[split:]

    print(f"Entrenando Random Forest con {len(X_train)} muestras...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Precision en Test (Accuracy): {acc:.2%}")
    print("\nReporte de Clasificacion:")
    print(classification_report(y_test, y_pred, target_names=["SELL", "HOLD", "BUY"]))

    # Guardar modelo y metadatos
    static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
    os.makedirs(static_dir, exist_ok=True)
    
    output_path = os.path.join(static_dir, "trading_model.joblib")
    payload = {
        "model": model,
        "features": feature_cols,
        "trained_at": datetime.now().isoformat(),
        "accuracy": acc
    }
    
    joblib.dump(payload, output_path)
    print(f"Modelo guardado en: {output_path}")

if __name__ == "__main__":
    main()
