"""
derivatives.py — Módulo de Derivados (Black-Scholes-Merton).

Implementación del modelo matemático para valorar opciones financieras.
Calcula el precio de opciones Call y Put europeas, sus letras Griegas,
y permite generar una superficie o matriz de simulación variando el
precio del activo subyacente y el tiempo al vencimiento.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm


def black_scholes_core(S, K, T, r, sigma, option_type='call'):
    """
    Función núcleo para el cálculo de Black-Scholes.
    Soporta escalares o arrays de numpy (para la superficie).
    """
    # Evitar divisiones por cero
    T = np.maximum(T, 1e-6)
    sigma = np.maximum(sigma, 1e-6)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type debe ser 'call' o 'put'")

    # Gamma y Vega son iguales para call y put
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega / 100,  # convención: cambio por 1% en vol
        "theta": theta / 365, # convención: decaimiento por 1 día
        "rho": rho / 100     # convención: cambio por 1% en tasa
    }


def valorar_opcion(S: float, K: float, T: float, r: float, sigma: float, tipo: str = 'call') -> dict:
    """
    Valora una opción usando el modelo Black-Scholes-Merton.
    """
    resultado = black_scholes_core(S, K, T, r, sigma, option_type=tipo.lower())
    
    return {
        "tipo": tipo.upper(),
        "precio": float(resultado["price"]),
        "griegas": {
            "delta": float(resultado["delta"]),
            "gamma": float(resultado["gamma"]),
            "vega": float(resultado["vega"]),
            "theta": float(resultado["theta"]),
            "rho": float(resultado["rho"]),
        }
    }


def generar_superficie_bsm(S_actual: float, K: float, T_max: float, r: float, sigma: float, tipo: str = 'call') -> dict:
    """
    Genera una matriz de precios variando el Precio del Subyacente (S) y el Tiempo al Vencimiento (T).
    S_range: ±20% del precio actual
    T_range: Desde cerca de cero hasta T_max
    """
    # 10 pasos para el precio y 10 para el tiempo (10x10 = 100 puntos)
    S_range = np.linspace(S_actual * 0.8, S_actual * 1.2, 10)
    T_range = np.linspace(1e-3, T_max, 10)
    
    S_grid, T_grid = np.meshgrid(S_range, T_range)
    
    resultados = black_scholes_core(S_grid, K, T_grid, r, sigma, option_type=tipo.lower())
    Z_precios = resultados["price"]
    
    return {
        "x_subyacente": S_range.tolist(),
        "y_tiempo": T_range.tolist(),
        "z_precios": Z_precios.tolist()
    }
