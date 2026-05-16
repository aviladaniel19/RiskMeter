#!/usr/bin/env python3
"""
test_supabase_connection.py - Validar conexión a Supabase antes de desplegar

Uso:
    python test_supabase_connection.py
"""

import sys
import os
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_connection():
    """Prueba la conexión a la BD configurada"""
    try:
        from app.config import get_settings
        from app.database import engine, Base
        from sqlalchemy import text
        
        print("✅ Importaciones exitosas")
        
        settings = get_settings()
        print(f"✅ DATABASE_URL configurada: {settings.DATABASE_URL[:50]}...")
        
        # Intentar conectarse
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión a la BD exitosa!")
            
        # Crear tablas si no existen
        print("\n📝 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/verificadas")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️  Consejos:")
        print("  1. ¿DATABASE_URL está configurada en .env.local o variables de entorno?")
        print("  2. ¿La contraseña de Supabase es correcta?")
        print("  3. ¿Tienes acceso a internet?")
        return False

if __name__ == "__main__":
    print("🔍 Verificando conexión a Supabase...\n")
    success = test_connection()
    sys.exit(0 if success else 1)
