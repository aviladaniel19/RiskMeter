"""
ml_service.py — Capa de Inteligencia Artificial (Módulo 3).

Implementa el patrón Singleton para asegurar que el modelo de Machine Learning
(Random Forest) se cargue una sola vez en memoria, optimizando el rendimiento
de la API. Provee métodos para realizar predicciones de señales de trading.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any

class MLService:
    _instance: Optional['MLService'] = None
    _model: Any = None
    _features_names: list[str] = []

    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._load_model()
        self._initialized = True

    def _load_model(self):
        """Carga el modelo serializado desde la carpeta static."""
        # Buscamos en backend/app/static/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "static", "trading_model.joblib")
        
        if os.path.exists(model_path):
            try:
                payload = joblib.load(model_path)
                # El payload puede ser el modelo directo o un dict con metadatos
                if isinstance(payload, dict):
                    self._model = payload.get("model")
                    self._features_names = payload.get("features", [])
                else:
                    self._model = payload
                
                print(f"MLService: Modelo cargado exitosamente ({model_path})")
            except Exception as e:
                print(f"MLService: Error al cargar el modelo: {e}")
                self._model = None
        else:
            print(f"MLService: Archivo {model_path} no encontrado. Ejecute train_model.py.")
            self._model = None

    def predecir(self, data_recent: pd.DataFrame) -> Dict[str, Any]:
        """
        Realiza la predicción de señal (Buy/Hold/Sell) basada en los datos más recientes.
        """
        if self._model is None:
            return {
                "error": "Modelo no disponible",
                "señal": "N/A",
                "confianza": 0.0
            }

        try:
            # Asegurar que tenemos las features necesarias
            # data_recent debe contener indicadores como RSI, MACD, etc.
            # Tomamos la última fila (el presente)
            latest_features = data_recent.iloc[-1:].copy()
            
            # Si el modelo tiene guardadas las features, filtramos
            if self._features_names:
                latest_features = latest_features[self._features_names]

            pred_code = self._model.predict(latest_features)[0]
            probs = self._model.predict_proba(latest_features)[0]
            
            # Importancia de variables (si el modelo lo permite)
            feature_importance = {}
            if hasattr(self._model, "feature_importances_"):
                importances = self._model.feature_importances_
                feature_importance = {
                    name: float(imp) for name, imp in zip(self._features_names, importances)
                }
                # Ordenar por importancia y tomar las top 5
                feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5])

            # Mapeo de labels (0: Sell, 1: Hold, 2: Buy)
            mapa_señal = {0: "SELL (VENDER)", 1: "HOLD (MANTENER)", 2: "BUY (COMPRAR)"}
            label = mapa_señal.get(pred_code, "HOLD")
            confianza = float(np.max(probs))

            return {
                "señal": label,
                "confianza": confianza,
                "probabilidades": {mapa_señal[i]: float(probs[i]) for i in range(len(probs))},
                "importancia_variables": feature_importance,
                "modelo": "Random Forest Classifier (Scikit-Learn)"
            }

        except Exception as e:
            return {
                "error": f"Error en predicción: {str(e)}",
                "señal": "ERROR",
                "confianza": 0.0
            }
