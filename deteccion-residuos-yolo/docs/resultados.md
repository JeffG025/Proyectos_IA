# 📈 Resultados del entrenamiento

Resultados del modelo **YOLO11n** entrenado para detección de residuos (6 clases).

## ⚙️ Configuración

| Parámetro | Valor |
|-----------|-------|
| Modelo | YOLO11n (nano) — 2.58 M parámetros, 6.3 GFLOPs |
| Épocas | 50 |
| Tamaño de imagen | 640×640 |
| Batch | 16 |
| Hardware | GPU Tesla T4 (Google Colab) |
| Tiempo de entrenamiento | ~1 h 20 min (1.325 h) |
| Framework | Ultralytics 8.4.60 · PyTorch 2.11 · CUDA |

## 🎯 Métricas globales (conjunto de validación)

| Métrica | Valor | Lectura |
|---------|-------|---------|
| **mAP@0.5** | **0.934** | Excelente (93.4 %) |
| **mAP@0.5:0.95** | **0.846** | Muy bueno (criterio estricto) |
| **Precisión** | **0.901** | 90 % de las detecciones son correctas |
| **Recall** | **0.889** | Encuentra ~89 % de los objetos reales |

> Para un proyecto académico, una mAP@0.5 ≈ 0.93 es un **resultado sobresaliente**.

## 📊 Métricas por clase

| Clase | Precisión | Recall | mAP@0.5 | mAP@0.5:0.95 |
|-------|-----------|--------|---------|--------------|
| Trash | 0.728 | 0.824 | 0.913 | 0.876 |
| cardboard | 0.971 | 0.918 | 0.938 | 0.791 |
| glass | 0.908 | 0.920 | 0.930 | 0.881 |
| **metal** | 0.936 | 0.929 | **0.966** | **0.941** |
| paper | 0.971 | 0.809 | 0.902 | 0.672 |
| plastic | 0.892 | 0.935 | 0.956 | 0.912 |

- **Mejor clase:** `metal` (mAP@0.5 = 0.966).
- **Clase más difícil:** `Trash` — menor precisión (0.728). Es la **minoritaria**
  (solo 316 ejemplos), lo que confirma el desbalance detectado en el EDA. Aun así
  su mAP@0.5 es alto (0.913).
- `paper` tiene el mAP@0.5:0.95 más bajo (0.672) y el recall más bajo (0.809):
  se le escapan algunos (los confunde con el fondo).

## 📈 Curvas de entrenamiento (`results.png`)

- Las **pérdidas (losses)** de train y val **bajan de forma sostenida** → el
  modelo aprende correctamente.
- Las **val losses se estabilizan sin volver a subir** → **no hay overfitting**.
- `precision`, `recall`, `mAP50` y `mAP50-95` **suben y se aplanan** hacia las
  épocas 40-50 → el entrenamiento **convergió**.
- **Escalón en la época ~40:** caída brusca de las train losses. Es **normal y
  buscado**: Ultralytics **desactiva la augmentation de mosaico** en las últimas
  10 épocas (`close_mosaic`) para afinar el modelo con imágenes limpias.

## 🔢 Matriz de confusión (`confusion_matrix.png`)

- **Diagonal dominante** = muchos aciertos (Trash 14, cardboard 46, glass 60,
  metal 53, paper 76, plastic 59).
- **Errores principales con `background`:**
  - *Falsos positivos:* a veces detecta un residuo donde solo hay fondo (3-5 casos por clase).
  - *Falsos negativos:* algunos objetos reales se le escapan (sobre todo `paper`: 6 casos).
- Confusiones entre clases muy bajas (p. ej. algún `paper`→`Trash`).

## ✅ Conclusiones

1. El modelo **detecta y clasifica residuos con alta fiabilidad** (mAP@0.5 = 0.93).
2. El principal margen de mejora está en la clase **`Trash`** (desbalanceada) y en
   reducir confusiones con el **fondo**.
3. Posibles mejoras futuras: más ejemplos de `Trash`, más épocas, o un modelo más
   grande (`yolo11s`).

## ⚠️ Nota sobre el warning de "segments"

Durante la validación aparece:
*"Box and segment counts should be equal..."*. Significa que el dataset trae unas
pocas anotaciones de segmentación mezcladas con las cajas. Ultralytics **usa solo
las cajas** (lo correcto para detección). **No afecta los resultados.**
