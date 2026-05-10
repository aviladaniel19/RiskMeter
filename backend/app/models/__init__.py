"""
models/__init__.py — Re-exporta todos los schemas Pydantic y modelos ORM.

Esto mantiene la compatibilidad con los imports existentes:
    from app.models import ActivosResponse, PortafolioRequest, ...

Al mismo tiempo, la lógica está organizada en sub-módulos:
    - models/schemas.py     → Pydantic (request/response)
    - models/db_models.py   → SQLAlchemy ORM (tablas)
"""

# ── Re-exportar schemas Pydantic (compatibilidad con main.py actual) ──
# El archivo schemas.py es el models.py original renombrado.
# Lo importamos con wildcard para no romper ningún import existente.
from app.models.schemas import *  # noqa: F401, F403

# ── Exportar modelos ORM ──
from app.models.db_models import (  # noqa: F401
    Asset,
    Price,
    Portfolio,
    PredictionLog,
    SignalLog,
)
