# 🎓 Guía de defensa — Detección de Residuos con YOLO

Documento de estudio para explicar y defender el proyecto. Cubre qué es, qué se
usó, cómo funciona y las preguntas típicas de un jurado.

---

## 1. ¿Qué es el proyecto y para qué sirve?

Es un sistema de **inteligencia artificial que detecta y clasifica residuos**
(basura) en imágenes y video. Dada una foto, el modelo **dibuja una caja**
alrededor de cada objeto e indica de qué tipo de residuo se trata:
`cartón, vidrio, metal, papel, plástico` o `basura general (Trash)`.

**Utilidad real:** automatizar la **separación de residuos** para reciclaje
(plantas de reciclaje, contenedores inteligentes, apps de educación ambiental).
Hoy esa separación se hace mucho a mano; un sistema así la acelera y reduce errores.

---

## 2. ¿Qué es YOLO?

**YOLO = "You Only Look Once"** (*"solo miras una vez"*). Es un modelo de
**detección de objetos** basado en redes neuronales. Su nombre viene de que
analiza **toda la imagen de una sola pasada** para encontrar todos los objetos a
la vez, lo que lo hace **muy rápido** (sirve para tiempo real, hasta en video).

Usamos **YOLO11**, la versión de la librería **Ultralytics** (2024), una de las
más modernas y precisas.

### Detección ≠ Clasificación (¡pregunta típica!)
- **Clasificación:** dice *"en esta foto hay un plástico"* (etiqueta global).
- **Detección (lo nuestro):** dice *"hay un plástico AQUÍ (caja x,y) y un vidrio
  ALLÁ (otra caja)"*. Localiza **y** clasifica cada objeto. Es más potente.

### ¿Por qué YOLO y no otro?
- **Velocidad:** detecta en una sola pasada (los métodos antiguos como R-CNN
  necesitaban dos etapas y eran lentos).
- **Precisión** alta con poco hardware.
- **Fácil de entrenar** con la librería Ultralytics (pocas líneas).
- Funciona en **tiempo real** (ideal para la demo con webcam).

---

## 3. Tecnologías y herramientas utilizadas

| Herramienta | Para qué se usó |
|-------------|-----------------|
| **Python** | Lenguaje de todo el proyecto |
| **YOLO11 (Ultralytics)** | Modelo de detección de objetos |
| **PyTorch** | Motor de deep learning por debajo de YOLO (entrena la red) |
| **Google Colab** | Entrenar en la nube con **GPU T4 gratis** |
| **GPU (T4)** | Acelera el entrenamiento (de horas en CPU a minutos) |
| **Roboflow** | De donde sacamos y descargamos el dataset etiquetado |
| **OpenCV / Pillow / Matplotlib** | Leer imágenes, dibujar cajas y graficar |

---

## 4. El dataset (los datos)

- **Origen:** Roboflow Universe (dataset público, licencia **CC BY 4.0**).
- **6 clases:** `Trash`, `cardboard`, `glass`, `metal`, `paper`, `plastic`.
- **6,061 imágenes** divididas en 3 grupos:
  - **train (5,301)** → para que el modelo **aprenda**.
  - **valid (328)** → para **ajustar y vigilar** que aprende bien.
  - **test (432)** → para la **evaluación final** con datos que nunca vio.
- **Formato YOLO:** cada imagen tiene un archivo `.txt` con una línea por objeto:
  `clase  x_centro  y_centro  ancho  alto` (coordenadas **normalizadas** 0–1).

**¿Por qué se divide en train/valid/test?** (pregunta típica)
Como estudiar: **train** es el libro con el que estudias, **valid** son los
exámenes de práctica para ver cómo vas, y **test** es el examen final con
preguntas nuevas. Si evaluáramos con las mismas imágenes de entrenamiento, el
modelo "se las sabría de memoria" y no mediríamos su capacidad real.

**Data augmentation:** el set de train viene **aumentado** (por eso hay 5,301).
Son copias de las imágenes con pequeñas variaciones (giros, brillo, recortes)
para que el modelo aprenda a reconocer el objeto en distintas condiciones y
**generalice mejor**.

**Desbalance de clases:** detectamos que `paper` (1414) tiene ~4.5x más ejemplos
que `Trash` (316). Esto puede hacer que el modelo detecte peor la clase
minoritaria; lo vigilamos en la matriz de confusión.

---

## 5. Cómo funciona el notebook (celda por celda)

1. **Verificar GPU (`!nvidia-smi`):** confirma que Colab nos dio una GPU.
2. **Instalar Ultralytics:** descarga la librería de YOLO.
3. **Montar Google Drive:** conecta tu Drive para leer el ZIP del dataset.
4. **Descomprimir el dataset:** extrae las imágenes y etiquetas a Colab y cuenta
   cuántas hay por grupo (control de que todo llegó bien).
5. **Reescribir `data.yaml`:** archivo de configuración que le dice a YOLO **dónde
   están** las imágenes y **cuáles son las clases**. Lo ponemos con rutas
   absolutas para evitar errores.
6. **Entrenar (`model.train`):** el paso central, aquí la red aprende.
7. **Evaluar (`model.val`):** calcula las métricas de qué tan bien quedó.
8. **Ver resultados:** curvas de entrenamiento, matriz de confusión y ejemplos.
9. **Guardar `best.pt`:** los "pesos" del modelo entrenado (su cerebro), que
   luego usamos en la PC para la demo.

---

## 6. Cómo APRENDE YOLO por dentro (nivel conceptual)

YOLO es una **red neuronal convolucional (CNN)** con 3 partes:
- **Backbone:** extrae características de la imagen (bordes, texturas, formas).
- **Neck:** combina información de distintos tamaños para detectar objetos
  grandes y pequeños.
- **Head:** produce la salida final: las **cajas**, la **clase** de cada una y un
  valor de **confianza**.

**El entrenamiento (en simple):**
1. El modelo mira una imagen y **predice** cajas y clases.
2. Compara su predicción con la **respuesta correcta** (las etiquetas reales).
3. Mide el error con una **función de pérdida (loss)**.
4. Ajusta sus parámetros internos (**pesos**) para equivocarse menos
   (*backpropagation*).
5. Repite con todas las imágenes, muchas veces (**épocas**), mejorando poco a poco.

**Transfer learning (¡clave!):** no entrenamos desde cero. Partimos de
`yolo11n.pt`, un modelo **ya preentrenado** con millones de imágenes (dataset
COCO, 80 objetos). Es como alguien que **ya sabe ver** formas y objetos, y solo
le enseñamos **nuestras 6 clases de basura**. Por eso entrena rápido y con pocos datos.

---

## 7. Parámetros de entrenamiento que usamos

| Parámetro | Valor | Qué significa |
|-----------|-------|---------------|
| `model` | `yolo11n.pt` | YOLO11 **nano**: el más pequeño y rápido |
| `epochs` | 50 | Veces que el modelo repasa **todo** el train |
| `imgsz` | 640 | Las imágenes se redimensionan a 640×640 px |
| `batch` | 16 | Imágenes que procesa juntas antes de ajustar pesos |
| `patience` | 15 | **Early stopping:** si no mejora en 15 épocas, se detiene |

**Época:** una pasada completa por todas las imágenes de entrenamiento.
**Batch:** como el modelo no puede ver las 5,301 a la vez, las procesa en grupos de 16.
**Early stopping:** evita perder tiempo (y *overfitting*) si ya no mejora.

---

## 8. Métricas de evaluación (¡las preguntarán seguro!)

- **IoU (Intersection over Union):** mide cuánto se **solapa** la caja predicha
  con la real (0 = nada, 1 = perfecta). Es la base de las demás métricas.
- **Precisión (Precision):** de todo lo que el modelo **dijo que era X**, ¿cuánto
  acertó? (penaliza falsos positivos).
- **Recall (Sensibilidad):** de todos los **X que realmente había**, ¿cuántos
  encontró? (penaliza los que se le escapan).
- **mAP@0.5 (mean Average Precision):** la métrica estrella. Promedia el
  rendimiento en todas las clases usando IoU ≥ 0.5. **Más alto = mejor.**
- **mAP@0.5:0.95:** versión más estricta, promedia con IoU de 0.5 a 0.95.
- **Matriz de confusión:** tabla que muestra en qué acierta y en qué **confunde**
  el modelo (p. ej., si confunde `glass` con `plastic`).

> Para detección de objetos, una **mAP@0.5 por encima de ~0.6–0.7** ya es un
> resultado sólido para un proyecto académico.

---

## 9. Conceptos extra que pueden preguntar

- **Overfitting (sobreajuste):** el modelo "memoriza" el train pero falla con
  datos nuevos. Se combate con augmentation, early stopping y el set de validación.
- **Underfitting:** el modelo es demasiado simple y ni siquiera aprende el train.
- **Pesos (`best.pt` / `last.pt`):** `best.pt` es el mejor modelo (mejor mAP en
  validación); `last.pt` es el de la última época.
- **¿Por qué Colab y no tu PC?** No tenemos GPU local y el disco es limitado;
  Colab da GPU gratis y entrena en minutos en vez de horas.

---

## 10. Preguntas frecuentes de defensa (Q&A rápido)

**P: ¿Qué hace tu proyecto?**
R: Detecta y clasifica 6 tipos de residuos en imágenes, dibujando una caja sobre
cada uno, para apoyar el reciclaje automático.

**P: ¿Por qué usaste YOLO?**
R: Porque es un detector de objetos rápido y preciso que funciona en tiempo real
y es fácil de entrenar con Ultralytics.

**P: ¿Detección o clasificación?**
R: Detección: además de decir *qué* es, dice *dónde* está (con coordenadas).

**P: ¿De dónde salieron los datos?**
R: De Roboflow Universe, un dataset público con licencia CC BY 4.0, ya etiquetado
en formato YOLO, con 6,061 imágenes.

**P: ¿Entrenaste desde cero?**
R: No, usé *transfer learning* desde un modelo preentrenado (COCO) y lo ajusté a
mis 6 clases. Es más rápido y necesita menos datos.

**P: ¿Cómo sabes que funciona bien?**
R: Por las métricas (mAP, precisión, recall) sobre datos que el modelo nunca vio
(validación/test) y por la matriz de confusión.

**P: ¿Limitaciones?**
R: Hay desbalance de clases (Trash es minoritaria) y los objetos del dataset son
grandes y centrados, así que en la demo conviene acercar el residuo a la cámara.
