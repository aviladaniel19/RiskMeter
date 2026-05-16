"""
database.py — Configuración de SQLAlchemy ORM + SQLite/PostgreSQL.

Patrón del curso Python para APIs e IA (Semana 7):
  - Motor SQLite embebido (cero configuración, ideal para desarrollo).
  - Motor PostgreSQL (Supabase) para producción.
  - SessionLocal crea sesiones por request, cerradas automáticamente.
  - get_db() como generador inyectable con Depends().

Soporta ambos motores automáticamente:
  - SQLite: desarrollo local
  - PostgreSQL (Supabase): producción
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# ── Motor SQLAlchemy ──────────────────────────────────
# Detecta automáticamente si es SQLite o PostgreSQL
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Cambiar a True para ver SQL en consola (debug)
    # Pool de conexiones para PostgreSQL
    pool_pre_ping=True if not is_sqlite else False,
    pool_size=5 if not is_sqlite else None,
    max_overflow=10 if not is_sqlite else None,
)

# ── Session factory ───────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── Base declarativa para modelos ORM ─────────────────
Base = declarative_base()


def get_db():
    """
    Generador que provee una sesión de BD por request.

    El bloque try/finally garantiza que la sesión se cierra
    incluso si el endpoint lanza una excepción.

    Uso con FastAPI:
        @app.get("/ejemplo")
        async def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
