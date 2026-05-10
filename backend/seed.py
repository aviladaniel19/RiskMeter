"""
seed.py — Script para inicializar la base de datos con datos semilla.

Patrón del curso Python para APIs e IA (Semana 7):
  - Pre-popula la tabla `assets` con los tickers seleccionados por el equipo.
  - Crea un portafolio de prueba inicial.
  - Se ejecuta una sola vez durante el despliegue o la configuración local.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio backend al path para poder importar la app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.db_models import Asset, Portfolio

def run_seed():
    print("[INFO] Iniciando proceso de seeding de la base de datos...")
    
    # Asegurar que las tablas existan
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Semilla de Activos (Assets)
        activos_semilla = [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "currency": "USD"},
            {"ticker": "MSFT", "name": "Microsoft Corp.", "sector": "Technology", "currency": "USD"},
            {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical", "currency": "USD"},
            {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "currency": "USD"},
            {"ticker": "GOOG", "name": "Alphabet Inc.", "sector": "Communication Services", "currency": "USD"},
        ]
        
        activos_agregados = 0
        for data in activos_semilla:
            # Comprobar si ya existe
            existe = db.query(Asset).filter(Asset.ticker == data["ticker"]).first()
            if not existe:
                nuevo_activo = Asset(**data)
                db.add(nuevo_activo)
                activos_agregados += 1
                
        if activos_agregados > 0:
            print(f"[OK] Se agregaron {activos_agregados} activos a la base de datos.")
        else:
            print("[INFO] Los activos semilla ya estaban en la base de datos.")

        # 2. Semilla de Portafolio de Prueba
        nombre_portafolio = "Portafolio Base (Igual Ponderacion)"
        existe_port = db.query(Portfolio).filter(Portfolio.name == nombre_portafolio).first()
        
        if not existe_port:
            tickers = [a["ticker"] for a in activos_semilla]
            peso_igual = round(1.0 / len(tickers), 4)
            # Asegurar que sumen exactamente 1.0 ajustando el último
            pesos = [peso_igual] * (len(tickers) - 1)
            pesos.append(round(1.0 - sum(pesos), 4))
            
            nuevo_portafolio = Portfolio(
                name=nombre_portafolio,
                tickers=tickers,
                weights=pesos
            )
            db.add(nuevo_portafolio)
            print(f"[OK] Se agrego el portafolio: '{nombre_portafolio}'")
        else:
            print("[INFO] El portafolio de prueba ya estaba en la base de datos.")

        # Confirmar los cambios
        db.commit()
        print("[OK] Seeding completado con exito.")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error durante el seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
