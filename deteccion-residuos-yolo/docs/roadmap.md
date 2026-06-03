# 🗺️ Roadmap del proyecto

Plan de trabajo por fases. Avanzamos **paso a paso**, validando cada fase antes
de pasar a la siguiente.

---

## ✅ Fase 0 — Setup del proyecto
**Objetivo:** dejar el proyecto listo para trabajar.
- [x] Crear estructura de carpetas
- [x] `README.md`, `requirements.txt`, `.gitignore`
- [x] Inicializar repositorio Git
- [ ] Crear entorno virtual e instalar dependencias *(cuando lo necesitemos)*

## ✅ Fase 1 — Dataset
**Objetivo:** conseguir un buen dataset de residuos en formato YOLO.
- [x] Comparar datasets de residuos en Roboflow Universe (nº de clases, imágenes, calidad)
- [x] Elegir el definitivo y documentarlo
- [x] Descargar a `data/raw/` en formato YOLO
- [x] Verificar `data.yaml`, clases y particiones train/valid/test

**Dataset elegido:** YOLOv8 Trash Detection — [Roboflow Universe](https://universe.roboflow.com/yolov8-trash-detection/yolo-v8-trash-detection-ee4016) (v3, licencia CC BY 4.0)
- **6 clases:** `Trash`, `cardboard`, `glass`, `metal`, `paper`, `plastic`
- **Imágenes:** 5,301 train (con augmentation) · 328 valid · 432 test · **6,061 total**
- Verificar en cualquier momento con: `py src/verificar_dataset.py`

## ✅ Fase 2 — Exploración de datos (EDA)
**Objetivo:** entender el dataset antes de entrenar.
- [x] Contar imágenes por partición y por clase (`src/analizar_clases.py`)
- [x] Detectar desbalance de clases (ratio 4.5x; `Trash` es minoritaria)
- [x] Visualizar imágenes con sus cajas (`src/visualizar_muestras.py`)
- [x] Documentar hallazgos y figuras en [`docs/eda.md`](eda.md)

## ✅ Fase 3 — Entrenamiento (Google Colab)
**Objetivo:** entrenar el detector con GPU gratuita.
- [x] Notebook `notebooks/02_entrenamiento_colab.ipynb` (método Drive)
- [x] Subir el ZIP del dataset a Google Drive
- [x] Entrenar YOLO11n en Colab con GPU T4 (50 épocas, ~1h20)
- [x] Resultados: **mAP@0.5 = 0.934** · mAP@0.5:0.95 = 0.846 (ver [resultados.md](resultados.md))
- [ ] Descargar `best.pt` a la carpeta `models/` *(pendiente)*

## ✅ Fase 4 — Evaluación
**Objetivo:** medir qué tan bueno es el modelo.
- [x] Métricas: mAP@0.5 (0.934), mAP@0.5:0.95 (0.846), precisión (0.90), recall (0.89)
- [x] Matriz de confusión y curvas de entrenamiento analizadas
- [x] Análisis de aciertos y errores (ver [resultados.md](resultados.md))
- [ ] *(Opcional)* Inferencia sobre el conjunto de test (`split='test'`)

## 🎥 Fase 5 — Demo / aplicación
**Objetivo:** demostrar el modelo funcionando.
- [ ] `src/predecir.py` — detección sobre una imagen
- [ ] `src/demo_webcam.py` — detección en vivo con la cámara
- [ ] *(Opcional)* interfaz web sencilla con Streamlit

## 📝 Fase 6 — Documentación y defensa
**Objetivo:** preparar la entrega final.
- [ ] README final con resultados e imágenes
- [ ] Documento del proyecto (problema, metodología, resultados, conclusiones)
- [ ] Guion para la presentación / defensa

---

---

## 🔄 Iteración 2 — Detección multi-objeto (dataset TACO)

**Motivo:** el dataset de la iteración 1 tenía ~1 objeto/imagen, así que el modelo
solo detectaba el residuo dominante. Para detectar **varios residuos por imagen**
cambiamos al dataset **TACO** (escenas reales).

- **Dataset:** [TACO (Roboflow · Divya)](https://universe.roboflow.com/divya-lzcld/taco-mqclx/dataset/3) — 18 clases, ~6,004 imágenes, CC BY 4.0
- **Multi-objeto confirmado:** 2.79 objetos/imagen · 63 % de imágenes con 2+ objetos
- **Notebook:** `notebooks/04_entrenamiento_taco_colab.ipynb` (lee las clases solo)
- [x] Entrenar en Colab (YOLO11n, 60 épocas) — **mAP@0.5 = 0.379** (ver [resultados_taco.md](resultados_taco.md))
- [x] Evaluación + matriz de confusión analizadas
- [x] Demo multi-objeto ✅ — detecta varios residuos por imagen (¡hasta 19 en una foto!)
- [ ] *(Opcional)* Mejorar precisión (modelo mayor / más resolución / 80+ épocas)
- [ ] Descargar `residuos_taco_best.pt` a `models/`

> Se espera un mAP más bajo (~0.3–0.5) por la dificultad de las escenas reales:
> es el precio (y la gracia) de la detección multi-objeto realista.

---

### Decisiones tomadas
- **Enfoque:** Detección de objetos (bounding boxes), no clasificación simple.
- **Entrenamiento:** Google Colab (no hay GPU local; 11 GB libres en disco).
- **Modelo:** YOLO de Ultralytics (versión nano/small para empezar).
- **Iteración 1:** dataset de 6 clases (1 obj/img) → mAP@0.5 = 0.934 pero mono-objeto.
- **Iteración 2:** dataset TACO (18 clases, multi-objeto) para detectar varios a la vez.
