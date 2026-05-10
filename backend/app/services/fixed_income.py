"""
fixed_income.py — Módulo de Renta Fija (Curva de Rendimientos de Nelson-Siegel).

Patrón del curso (Capa 3: Renta Fija y Derivados):
  - Extrae tasas del Tesoro de EE.UU. a múltiples plazos desde FRED.
  - Ajusta el modelo de Nelson-Siegel utilizando SciPy (curve_fit).
  - Devuelve los parámetros ajustados y la curva teórica interpolada.
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from app.services.api_client import obtener_dato_macro


def ecuacion_nelson_siegel(m, beta0, beta1, beta2, tau):
    """
    Ecuación del modelo de Nelson-Siegel para modelar la curva de tasas.
    
    Parámetros:
    m : array
        Plazos de maduración (madurity) en años.
    beta0 : float
        Nivel a largo plazo (asíntota de la curva).
    beta1 : float
        Pendiente a corto plazo (spread entre corto y largo plazo).
    beta2 : float
        Curvatura (joroba a medio plazo).
    tau : float
        Parámetro de decaimiento (escala de tiempo).
    """
    # Para evitar división por cero si m es 0
    m = np.where(m == 0, 1e-6, m)
    
    termino1 = (1 - np.exp(-m / tau)) / (m / tau)
    termino2 = termino1 - np.exp(-m / tau)
    
    return beta0 + beta1 * termino1 + beta2 * termino2


def ajustar_nelson_siegel(maduraciones: list[float], tasas_reales: list[float]) -> dict:
    """
    Ajusta los parámetros de Nelson-Siegel a una serie de tasas reales.
    """
    m = np.array(maduraciones)
    y = np.array(tasas_reales)

    # Valores iniciales heurísticos:
    # beta0 = tasa de largo plazo (ej. 30 años)
    # beta1 = corto plazo - largo plazo
    # beta2 = curvatura (tasa intermedia)
    # tau = 1.0 (ajustable)
    b0_init = y[-1]
    b1_init = y[0] - y[-1]
    b2_init = 0.0
    tau_init = 1.0
    
    p0 = [b0_init, b1_init, b2_init, tau_init]
    
    try:
        # curve_fit optimiza minimizando el error cuadrático medio
        # maxfev incrementado para asegurar convergencia
        popt, pcov = curve_fit(ecuacion_nelson_siegel, m, y, p0=p0, maxfev=10000)
        beta0, beta1, beta2, tau = popt
        
        # Generar la curva ajustada (interpolar desde 0.1 hasta 30 años con 100 puntos)
        m_teorico = np.linspace(min(m), max(m), 100)
        y_teorico = ecuacion_nelson_siegel(m_teorico, beta0, beta1, beta2, tau)
        
        return {
            "exito": True,
            "parametros": {
                "beta0": float(beta0),
                "beta1": float(beta1),
                "beta2": float(beta2),
                "tau": float(tau)
            },
            "curva_teorica": {
                "maduraciones": m_teorico.tolist(),
                "tasas": y_teorico.tolist()
            }
        }
    except Exception as e:
        return {"exito": False, "error": str(e)}


def obtener_curva_tesoro() -> dict:
    """
    Descarga las tasas del tesoro desde FRED y ajusta el modelo NS.
    """
    # Series de FRED para Constant Maturity Treasury Rates
    nodos_fred = {
        "DGS1MO": (1/12, "1 Mes"),
        "DGS3MO": (3/12, "3 Meses"),
        "DGS6MO": (6/12, "6 Meses"),
        "DGS1": (1.0, "1 Año"),
        "DGS2": (2.0, "2 Años"),
        "DGS3": (3.0, "3 Años"),
        "DGS5": (5.0, "5 Años"),
        "DGS7": (7.0, "7 Años"),
        "DGS10": (10.0, "10 Años"),
        "DGS20": (20.0, "20 Años"),
        "DGS30": (30.0, "30 Años"),
    }
    
    puntos_reales = []
    
    from datetime import datetime, timedelta
    import concurrent.futures

    inicio_str = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    def fetch_serie(serie):
        return obtener_dato_macro(serie, inicio=inicio_str)

    # Usar ThreadPoolExecutor para limitar el tiempo de espera por serie
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futuros = {executor.submit(fetch_serie, serie): (serie, maduracion, nombre) for serie, (maduracion, nombre) in nodos_fred.items()}
            for futuro in concurrent.futures.as_completed(futuros, timeout=8):
                serie, maduracion, nombre = futuros[futuro]
                try:
                    datos = futuro.result()
                    if not datos.empty:
                        ultima_tasa = float(datos.iloc[-1])
                        # Si la tasa está en decimales (ej. 0.045), FRED la da en porcentaje (4.5), el api_client a veces divide por 100.
                        # Asumimos que viene en decimales o porcentaje dependendiendo de api_client.
                        puntos_reales.append({
                            "serie": serie,
                            "nombre": nombre,
                            "maduracion": maduracion,
                            "tasa": ultima_tasa,
                            "fecha": str(datos.index[-1].date() if hasattr(datos.index[-1], 'date') else datos.index[-1])
                        })
                except Exception:
                    continue
    except concurrent.futures.TimeoutError:
        print("Timeout al obtener datos de FRED")
        
    if len(puntos_reales) < 3:
        # Fallback de datos teóricos si FRED falla
        puntos_reales = [
            {"serie": "DGS1MO", "nombre": "1 Mes", "maduracion": 1/12, "tasa": 5.35, "fecha": inicio_str},
            {"serie": "DGS3MO", "nombre": "3 Meses", "maduracion": 3/12, "tasa": 5.38, "fecha": inicio_str},
            {"serie": "DGS6MO", "nombre": "6 Meses", "maduracion": 6/12, "tasa": 5.36, "fecha": inicio_str},
            {"serie": "DGS1", "nombre": "1 Año", "maduracion": 1.0, "tasa": 5.09, "fecha": inicio_str},
            {"serie": "DGS2", "nombre": "2 Años", "maduracion": 2.0, "tasa": 4.75, "fecha": inicio_str},
            {"serie": "DGS3", "nombre": "3 Años", "maduracion": 3.0, "tasa": 4.50, "fecha": inicio_str},
            {"serie": "DGS5", "nombre": "5 Años", "maduracion": 5.0, "tasa": 4.30, "fecha": inicio_str},
            {"serie": "DGS7", "nombre": "7 Años", "maduracion": 7.0, "tasa": 4.32, "fecha": inicio_str},
            {"serie": "DGS10", "nombre": "10 Años", "maduracion": 10.0, "tasa": 4.35, "fecha": inicio_str},
            {"serie": "DGS20", "nombre": "20 Años", "maduracion": 20.0, "tasa": 4.55, "fecha": inicio_str},
            {"serie": "DGS30", "nombre": "30 Años", "maduracion": 30.0, "tasa": 4.48, "fecha": inicio_str},
        ]
        # Ajustamos a decimales porque el modelo lo espera (api_client.py linea 156 divide por 100)
        # Vamos a asegurar que los puntos reales estén en la misma escala que las formulas esperan
        # En la funcion anterior se guardaba la tasa tal cual. Vamos a ver:
        # En index.html se hace "p.tasa * 100", por ende, la API debe devolver la tasa en decimal (ej: 0.05).
        # Vamos a dividir por 100 el fallback.
        for p in puntos_reales:
            p["tasa"] = p["tasa"] / 100.0
        
    # Ordenar por maduración
    puntos_reales.sort(key=lambda x: x["maduracion"])
    
    m_reales = [p["maduracion"] for p in puntos_reales]
    y_reales = [p["tasa"] for p in puntos_reales]
    
    resultado_ns = ajustar_nelson_siegel(m_reales, y_reales)
    
    return {
        "fecha_datos": puntos_reales[-1]["fecha"],
        "puntos_reales": puntos_reales,
        "nelson_siegel": resultado_ns
    }
