# ♻️ Detección de Residuos con YOLO

Sistema de **detección de objetos** que identifica y localiza distintos tipos de
residuos (plástico, vidrio, metal, papel, orgánico, etc.) en imágenes y video,
con el objetivo de apoyar la **separación automática de basura** y el reciclaje.

Proyecto desarrollado con **YOLO (Ultralytics)** entrenado sobre un dataset
público de residuos. Es un proyecto final de Inteligencia Artificial.

---

## 🎯 Objetivo

Entrenar un modelo de visión por computadora capaz de **detectar y clasificar
residuos** dibujando una caja (bounding box) sobre cada objeto, indicando su
tipo y posición. Aplicaciones reales: plantas de reciclaje, contenedores
inteligentes, apps de educación ambiental.

## 🧰 Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Modelo | YOLO (Ultralytics) — detección de objetos |
| Lenguaje | Python 3.12 |
| Entrenamiento | Google Colab (GPU T4 gratuita) |
| Dataset | Dataset público de residuos en formato YOLO (Roboflow) |
| Visualización | OpenCV, Matplotlib |
| Demo | Inferencia sobre imágenes y webcam en vivo |

## 📁 Estructura del proyecto

```
deteccion-residuos-yolo/
├── data/                # Dataset (no se versiona, ver data/README.md)
│   └── raw/             # Dataset descargado en formato YOLO
├── notebooks/           # Notebooks de exploración y entrenamiento (Colab)
├── src/                 # Scripts de Python (descarga, inferencia, demo)
├── models/              # Pesos entrenados (.pt)
├── docs/                # Documentación, roadmap y material de la defensa
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

## 🗺️ Estado del proyecto

Ver el plan completo por fases en [`docs/roadmap.md`](docs/roadmap.md).

- [x] **Fase 0** — Setup del proyecto (estructura + entorno)
- [x] **Fase 1** — Dataset (6 clases, 6061 imágenes, formato YOLO) ✅
- [x] **Fase 2** — Exploración de datos (EDA + figuras) ✅
- [x] **Fase 3** — Entrenamiento YOLO11n en Colab (**mAP@0.5 = 0.934**) ✅
- [x] **Fase 4** — Evaluación del modelo (métricas + matriz de confusión) ✅
- [ ] **Fase 5** — Demo / aplicación
- [ ] **Fase 6** — Documentación y defensa

## 🚀 Puesta en marcha (se irá completando)

```bash
# 1. Crear entorno virtual
py -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

> El entrenamiento se realiza en Google Colab. El entorno local se usa para
> explorar datos y ejecutar la demo de inferencia.

---

_Proyecto académico — Inteligencia Artificial._
