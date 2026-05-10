"""
db_models.py — Modelos ORM de SQLAlchemy para persistencia.

Patrón del curso Python para APIs e IA (Semana 7):
  - Cada tabla se define como una clase Python tipada.
  - Las relaciones (1:N) se expresan con relationship().
  - Esto permite usar db.query(Asset).filter(...) en lugar de SQL raw.

Cuatro modelos mínimos requeridos por la rúbrica:
  1. Asset      — Activos del portafolio
  2. Price      — Precios históricos (cache de Yahoo Finance)
  3. Portfolio  — Portafolios guardados por el usuario
  4. PredictionLog — Log de predicciones del modelo ML
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    ForeignKey, JSON, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Asset(Base):
    """
    Activo financiero registrado en el sistema.

    Almacena metadata del ticker para no consultar Yahoo Finance
    en cada request. Se pre-popula con seed.py.
    """
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(120), default="")
    sector = Column(String(60), default="N/A")
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación 1:N → un activo tiene muchos precios
    prices = relationship("Price", back_populates="asset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Asset(ticker={self.ticker!r}, name={self.name!r})>"


class Price(Base):
    """
    Precio histórico de un activo (cache transparente).

    Cuando el frontend pide /precios/{ticker}, el DataService
    primero busca aquí. Si no existe o es viejo, llama a Yahoo
    Finance y persiste el resultado.
    """
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("asset_id", "date", name="uq_asset_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    # Relación inversa
    asset = relationship("Asset", back_populates="prices")

    def __repr__(self):
        return f"<Price(asset_id={self.asset_id}, date={self.date}, close={self.close})>"


class Portfolio(Base):
    """
    Portafolio guardado por el usuario.

    Permite CRUD básico: el usuario guarda una composición
    (tickers + pesos) y puede recuperarla después.
    """
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    tickers = Column(JSON, nullable=False)   # ["AAPL", "MSFT", ...]
    weights = Column(JSON, nullable=False)   # [0.2, 0.3, ...]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Portfolio(name={self.name!r}, tickers={self.tickers})>"


class PredictionLog(Base):
    """
    Log de predicciones del modelo de Machine Learning.

    Cada vez que el endpoint /predict genera una predicción,
    se registra aquí para monitoreo futuro (drift detection, auditoría).
    """
    __tablename__ = "predictions_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_version = Column(String(40), default="v1.0.0")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ticker = Column(String(10), nullable=False)
    input_features = Column(JSON)
    prediction = Column(Float)
    actual = Column(Float, nullable=True)  # Se llena después si se conoce el real

    def __repr__(self):
        return f"<PredictionLog(ticker={self.ticker!r}, prediction={self.prediction})>"


class SignalLog(Base):
    """
    Log de señales de trading disparadas.

    Requerimiento de la rúbrica: persistir cada señal en una tabla
    signals_log de SQLite (timestamp, ticker, regla, valor).
    """
    __tablename__ = "signals_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    rule = Column(String(60), nullable=False)     # "RSI_OVERSOLD", "MACD_CROSS_BUY", etc.
    value = Column(Float)                          # Valor del indicador al momento del disparo
    signal_type = Column(String(10))               # "BUY" o "SELL"
    description = Column(String(200), default="")

    def __repr__(self):
        return f"<SignalLog(ticker={self.ticker!r}, rule={self.rule!r})>"
