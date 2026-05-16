#!/usr/bin/env python3
"""
init_db.py - Inicializa la base de datos Supabase con las tablas necesarias

Este script debe ejecutarse UNA SOLA VEZ después de cambiar a Supabase.

Uso:
    python init_db.py

Qué hace:
    ✅ Crea todas las tablas definidas en los modelos ORM
    ✅ Verifica la conexión a Supabase
    ✅ Inicializa datos de referencia si es necesario
"""

import sys
import os
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def main():
    try:
        print("=" * 60)
        print("🚀 INICIALIZADOR DE BASE DE DATOS - RiskLabUSTA")
        print("=" * 60 + "\n")
        
        # Importar después de ajustar el path
        from app.config import get_settings
        from app.database import engine, Base
        from app.models.db_models import (
            Usuario, Transaccion, PortafolioHistorico, Alerta
        )
        from sqlalchemy import text
        
        settings = get_settings()
        
        # Mostrar configuración
        is_postgres = "postgresql" in settings.DATABASE_URL
        print(f"📊 Tipo de BD: {'PostgreSQL (Supabase) 🌐' if is_postgres else 'SQLite 📁'}")
        print(f"📍 URL: {settings.DATABASE_URL[:60]}...")
        print()
        
        # Prueba de conexión
        print("🔗 Probando conexión...")
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT NOW() as timestamp"))
                row = result.fetchone()
                print(f"✅ Conexión exitosa: {row[0]}\n" if is_postgres else "✅ Conexión exitosa\n")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("\n⚠️  Soluciones:")
            print("  • Verifica DATABASE_URL en .env.local")
            print("  • Asegúrate de que Supabase está activo")
            print("  • Comprueba tu conexión a internet\n")
            return False
        
        # Crear tablas
        print("📝 Creando tablas...")
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Tablas creadas exitosamente\n")
        except Exception as e:
            print(f"❌ Error al crear tablas: {e}\n")
            return False
        
        # Verificar tablas
        print("✔️  Verificando tablas creadas...")
        with engine.connect() as connection:
            if is_postgres:
                query = """
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """
            else:
                query = "SELECT name FROM sqlite_master WHERE type='table'"
            
            result = connection.execute(text(query))
            tables = [row[0] for row in result.fetchall()]
            
            for table in tables:
                print(f"   ✅ {table}")
        
        print("\n" + "=" * 60)
        print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("=" * 60)
        print("\n🚀 Próximos pasos:")
        print("   1. Verifica la conexión: python test_supabase_connection.py")
        print("   2. Inicia el servidor: uvicorn backend/app/main:app --reload")
        print("   3. Abre http://localhost:8000/docs en tu navegador")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\nAsegúrate de ejecutar: pip install -r backend/requirements.txt")
        return False
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
