# 📚 Documentación Completa — RiskLab USTA

## Guía de acceso a la documentación del proyecto

Este proyecto incluye **tres documentos principales** que explican cómo funciona, cómo se cumple la rúbrica y cómo usar el sistema.

---

## 📖 Documentos disponibles

### 1. **DOCUMENTACION.html** ⭐ *Comienza aquí*
**Propósito:** Índice central y guía de navegación  
**Para quién:** Usuarios nuevos que quieren entender qué documentos consultar  
**Contenido:**
- Resumen ejecutivo del proyecto
- Links a los otros documentos
- Estadísticas de cobertura
- Stack tecnológico
- Guía rápida

**👉 Abrir:** `DOCUMENTACION.html`

---

### 2. **documentacion_completa.html** 📘 *Guía técnica detallada*
**Propósito:** Explicación completa de todos los módulos, endpoints y algoritmos  
**Para quién:** Desarrolladores, profesores, estudiantes que quieren entender la teoría  
**Contenido:**
- 11 módulos de análisis financiero (Indicadores, Rendimientos, GARCH, CAPM, VaR, Markowitz, Señales, Macro, Renta Fija, Opciones, Stress Testing)
- 15 endpoints HTTP documentados
- Stack tecnológico completo
- Testing y DevOps
- Cumplimiento de rúbrica mapeado
- Referencias académicas

**Secciones principales:**
1. **Módulos 1–6:** Teoría clásica de riesgo (CAPM, VaR, Markowitz, etc.)
2. **Módulos 7–8:** Extensiones innovadoras (Señales automáticas, Contexto macro)
3. **Módulos 9–11:** Bonus (Renta fija, Opciones, Stress Testing)
4. **Stack Tecnológico:** FastAPI, Pydantic, Docker, GitHub Actions
5. **Endpoints:** Tabla con todos los 15 endpoints, parámetros y descripción
6. **Tests y Docker:** Guía de testing y despliegue
7. **Cumplimiento de Rúbrica:** Mapeo explícito de criterios de evaluación
8. **Referencias:** Links a documentación oficial

**👉 Abrir:** `documentacion_completa.html`

---

### 3. **cumplimiento_rubrica.html** ✅ *Matriz de evaluación*
**Propósito:** Tabla interactiva mostrando cómo cada criterio de la rúbrica está implementado  
**Para quién:** Evaluadores, profesores, estudiantes que necesitan verificar cumplimiento  
**Contenido:**
- Tabla de 17 filas con criterios vs. módulos implementados
- Código de colores: ★ nuevos, ★★ bonus, verde base
- Descripción de cada criterio
- Archivo(s) donde se implementa
- Peso en la rúbrica (%)
- Notas sobre diferenciales del proyecto

**Estructura de la tabla:**
| # | Criterio | Módulo(s) | Archivo(s) | Peso |
|---|----------|-----------|-----------|------|
| 1 | Análisis técnico | Módulo 1 | src/indicators.py | 10% |
| ... | ... | ... | ... | ... |
| 17 | Sustentación oral | − | − | 10% |

**Criterios base:** 16 (100% implementados)  
**Criterios bonus:** 3 (Módulos 9, 10, 11)  

**👉 Abrir:** `cumplimiento_rubrica.html`

---

## 📋 Estructura de carpetas

```
RiskLabUSTA/
├── DOCUMENTACION.html              ← Índice central (comienza aquí)
├── documentacion_completa.html      ← Documentación técnica detallada
├── cumplimiento_rubrica.html        ← Matriz de evaluación
├── README_DOCUMENTACION.md          ← Este archivo
├── README.md                        ← Guía de inicio rápido
├── requirements.txt                 ← Dependencias Python
├── docker-compose.yml               ← Orquestación Docker
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py                  ← API principal
│   │   ├── models/
│   │   │   ├── schemas.py           ← Validación Pydantic v2
│   │   │   └── db_models.py         ← SQLAlchemy ORM
│   │   ├── services/                ← Módulos 1-11
│   │   │   ├── indicators.py        ← Módulo 1
│   │   │   ├── returns.py           ← Módulo 2
│   │   │   ├── garch_models.py      ← Módulo 3
│   │   │   ├── capm.py              ← Módulo 4
│   │   │   ├── var_cvar.py          ← Módulo 5
│   │   │   ├── markowitz.py         ← Módulo 6
│   │   │   ├── signals.py           ← Módulo 7
│   │   │   ├── macro_benchmark.py   ← Módulo 8
│   │   │   ├── fixed_income.py      ← Módulo 9
│   │   │   ├── derivatives.py       ← Módulo 10
│   │   │   ├── risk_service.py      ← Módulo 11
│   │   │   └── ml_service.py        ← ML / Predicción
│   │   ├── static/
│   │   │   └── index.html           ← Frontend SPA
│   │   └── database.py              ← SQLAlchemy session
│   └── seed.py                      ← Carga de datos
├── src/                             ← Scripts de análisis
│   ├── indicators.py
│   ├── returns.py
│   ├── garch_models.py
│   ├── capm.py
│   ├── var_cvar.py
│   ├── markowitz.py
│   ├── signals.py
│   ├── macro_benchmark.py
│   ├── fixed_income.py
│   ├── derivatives.py
│   └── ml_service.py
├── tests/                           ← Test suite pytest
│   ├── conftest.py
│   └── test_*.py
└── data/
    ├── raw/
    └── processed/
```

---

## 🎯 Cómo usar esta documentación

### **Para estudiantes que defienden el proyecto:**
1. Lee **DOCUMENTACION.html** para entender la estructura general
2. Estudia **documentacion_completa.html** para profundizar en teoría
3. Consulta **cumplimiento_rubrica.html** antes de la sustentación oral

### **Para profesores evaluadores:**
1. Abre **cumplimiento_rubrica.html** para verificar cobertura de criterios
2. Referencia **documentacion_completa.html** para detalles técnicos
3. Usa los números de módulo y archivo para revisar código fuente

### **Para desarrolladores continuando el proyecto:**
1. Lee **documentacion_completa.html** para entender arquitectura
2. Consulta **cumplimiento_rubrica.html** para saber qué está cubierto
3. Revisa `backend/app/main.py` para endpoints disponibles

---

## 📊 Estadísticas del proyecto

| Métrica | Valor |
|---------|-------|
| **Módulos de análisis** | 11 |
| **Endpoints HTTP** | 15 |
| **Criterios de rúbrica** | 16 + 1 (sustentación) |
| **Criterios bonus** | 3 (Módulos 9–11) |
| **Cobertura de rúbrica** | 100% |
| **Líneas de documentación** | ~5,000+ |
| **Lenguaje principal** | Python 3.11.9 |
| **Framework API** | FastAPI 0.120+ |
| **Frontend** | HTML5/CSS3 SPA (Chart.js) |
| **Base de datos** | SQLite (SQLAlchemy ORM) |
| **DevOps** | Docker + GitHub Actions |

---

## 🚀 Guía rápida de inicio

### **1. Instalar dependencias**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### **2. Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
FRED_API_KEY=tu_clave_aqui
DATABASE_URL=sqlite:///./risklab.db
```

### **3. Ejecutar el servidor**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### **4. Acceder al dashboard**
- **Dashboard:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### **5. Ejecutar con Docker**
```bash
docker-compose up -d
```

---

## 📝 Criterios implementados

### ✅ Criterios base (100% cumplido)
1. ✅ Análisis técnico e indicadores (10%)
2. ✅ Rendimientos y propiedades empíricas (6%)
3. ✅ Volatilidad: EWMA + ARCH/GARCH (10%)
4. ✅ CAPM y riesgo sistemático (6%)
5. ✅ VaR, CVaR y backtesting Kupiec (10%)
6. ✅ Markowitz: Frontera eficiente (10%)
7. ✅ Señales automáticas ★ (7%)
8. ✅ Contexto macro y benchmark ★ (6%)
9. ✅ Renta fija: Nelson-Siegel ★★ (Bonus)
10. ✅ Opciones: Black-Scholes ★★ (Bonus)
11. ✅ Stress testing ★★ (Bonus)
12. ✅ Backend FastAPI + Pydantic (12%)
13. ✅ Tests pytest + TestClient (3%)
14. ✅ Docker + PaaS + CI (6%)
15. ✅ Tablero (frontend) (7%)
16. ✅ Buenas prácticas (6%)
17. ⚠️ Sustentación oral (10%) — Depende de presentación

---

## 🔗 Enlaces útiles

**FastAPI:**
- Docs: https://fastapi.tiangolo.com
- OpenAPI: http://localhost:8000/docs

**Librerías financieras:**
- ARCH/GARCH: https://arch.readthedocs.io
- statsmodels: https://www.statsmodels.org
- yfinance: https://github.com/ranaroussi/yfinance
- FRED API: https://fred.stlouisfed.org

**DevOps:**
- Docker: https://docs.docker.com
- GitHub Actions: https://docs.github.com/en/actions
- Render: https://render.com/docs

---

## 💡 Preguntas frecuentes

**P: ¿Dónde veo la lista completa de endpoints?**  
R: En `documentacion_completa.html`, sección "FastAPI y Endpoints"

**P: ¿Cómo verifico que el proyecto cumple la rúbrica?**  
R: Abre `cumplimiento_rubrica.html` — es una tabla interactiva con todos los criterios

**P: ¿Dónde está el código de cada módulo?**  
R: En `backend/app/services/` (ej: `indicators.py` = Módulo 1)

**P: ¿Cómo despliego el proyecto en producción?**  
R: Lee la sección "Docker + CI/CD" en `documentacion_completa.html`

**P: ¿Qué APIs externas necesito?**  
R: Solo `FRED_API_KEY` (Federal Reserve). Configurar en `.env`

---

## 📞 Información del proyecto

**Institución:** Pontificia Universidad Javeriana USTA  
**Curso:** Proyecto Integrador — Teoría del Riesgo  
**Asignatura:** Python, APIs e IA para Análisis de Riesgo Financiero  
**Período:** 2026 C-III  

**Autores (ejemplo):**
- Daniel Avila Otalora
- Jhon Alexander Ocampo Gómez

**Profesor:**  
- Javier Mauricio Sierra

---

## ✨ Últimas actualizaciones

- ✅ `2026-05-13` Documentación completa finalizada con 11 módulos
- ✅ `2026-05-13` Tabla de cumplimiento de rúbrica (100% cobertura)
- ✅ `2026-05-13` Índice central (DOCUMENTACION.html)
- ✅ `2026-05-13` Stack tecnológico documentado

---

**Last updated:** May 13, 2026  
**Version:** 1.0  
**Status:** ✅ Documentación completa y lista para sustentación
