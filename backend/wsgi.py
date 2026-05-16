"""
WSGI entry point para Vercel.

Vercel necesita un punto de entrada WSGI para ejecutar la aplicación FastAPI
en un entorno serverless.
"""

import sys
import os

# Agregar el backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Vercel detecta automáticamente esta variable
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
