"""
Verificación rápida: Importaciones principales del proyecto

Ejecuta esto para asegurar que todas las dependencias están instaladas
antes de desplegar a Vercel.
"""

def test_imports():
    errors = []
    
    imports_to_test = [
        ("FastAPI", "fastapi"),
        ("SQLAlchemy", "sqlalchemy"),
        ("Pydantic", "pydantic"),
        ("Pandas", "pandas"),
        ("NumPy", "numpy"),
        ("yfinance", "yfinance"),
        ("FRED API", "fredapi"),
        ("psycopg2", "psycopg2"),  # PostgreSQL driver
    ]
    
    print("🔍 Verificando dependencias...\n")
    
    for name, module in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {name:<20} OK")
        except ImportError as e:
            print(f"❌ {name:<20} FALTA")
            errors.append((name, module, str(e)))
    
    if errors:
        print(f"\n⚠️  Faltan {len(errors)} dependencia(s). Instala con:")
        print("  pip install -r backend/requirements.txt")
        return False
    else:
        print("\n✅ ¡Todas las dependencias están instaladas!")
        return True

if __name__ == "__main__":
    import sys
    success = test_imports()
    sys.exit(0 if success else 1)
