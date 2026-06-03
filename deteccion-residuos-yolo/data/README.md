# 📦 Datos

Dataset de **detección de residuos** (6 clases) en formato YOLO.

- **Clases (6):** `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`
- **Imágenes:** ~2,500
- **Formato:** YOLOv8 (cajas / bounding boxes)
- **Fuente:** [YOLOv8 Trash Detection — Roboflow Universe](https://universe.roboflow.com/yolov8-trash-detection/yolo-v8-trash-detection-ee4016)

> ⚠️ El dataset **no se versiona en Git** (es pesado). `data/raw/` está en `.gitignore`.

---

## ⬇️ Cómo descargarlo (método manual — recomendado para empezar)

1. Crea una cuenta **gratuita** en 👉 https://roboflow.com (botón *Sign Up*).
2. Abre la página del dataset:
   https://universe.roboflow.com/yolov8-trash-detection/yolo-v8-trash-detection-ee4016
   - Si esa no estuviera disponible, busca en https://universe.roboflow.com
     `trash detection 6 classes` y elige uno con las clases de arriba.
3. Clic en el botón **`Download Dataset`**.
4. En **Format** elige **`YOLOv8`** *(o `YOLOv11` si aparece: el formato de
   dataset es idéntico entre versiones de YOLO; lo que cambia es el modelo que
   entrenamos, y eso se decide en el código, no aquí).*
5. Marca la opción **`Download zip to computer`** y descarga el `.zip`.
6. **Descomprime** el contenido dentro de esta carpeta `data/raw/`, de modo que
   quede así:

   ```
   data/raw/
   ├── data.yaml
   ├── train/   (images/ + labels/)
   ├── valid/   (images/ + labels/)
   └── test/    (images/ + labels/)
   ```

7. Verifica que todo quedó bien ejecutando (desde la raíz del proyecto):

   ```bash
   py src/verificar_dataset.py
   ```

   Debe mostrar el `data.yaml`, las 6 clases y el conteo de imágenes. ✅

---

## ⬇️ Método por código (lo usaremos en Google Colab — Fase 3)

En el notebook de entrenamiento descargaremos el dataset directo con la API de
Roboflow (mismo dataset). Necesitarás tu **API key** (en Roboflow:
`Settings → API Keys`). El snippet se genera en la misma página de descarga al
elegir **`Show download code`**. Lo integraremos cuando lleguemos a Colab.

> 💡 Cuando tengas la página de descarga abierta, si me pasas el bloque de
> **`Show download code`** (sin tu API key), dejo el script `src/descargar_dataset.py`
> exacto para tu dataset.
