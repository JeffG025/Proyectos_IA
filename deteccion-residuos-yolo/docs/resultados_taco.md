# 📈 Resultados — Iteración 2 (TACO multi-objeto)

Modelo **YOLO11n** entrenado sobre **TACO** (18 clases, basura en escenas reales),
**60 épocas** en GPU T4. Objetivo: **detectar varios residuos por imagen**.

## 🎯 Métricas globales (validación)

| Métrica | Iteración 1 (fácil) | **Iteración 2 (TACO)** |
|---------|--------------------|------------------------|
| mAP@0.5 | 0.934 | **0.379** |
| mAP@0.5:0.95 | 0.846 | **0.289** |
| Precisión | 0.901 | **0.651** |
| Recall | 0.889 | **0.347** |
| Objetos/imagen | 1.01 | **2.79** ✅ |

> ⚠️ **La bajada de mAP es esperada y correcta.** TACO es basura real (objetos
> pequeños, amontonados, con sombras, 18 clases). El logro es que **ahora detecta
> múltiples objetos por imagen**, que era el objetivo.

## 📊 Métricas por clase

| Clase | Precisión | Recall | mAP@0.5 |
|-------|-----------|--------|---------|
| **Bottle** | 0.681 | 0.645 | **0.670** |
| **Can** | 0.709 | 0.637 | **0.664** |
| **Cup** | 0.589 | 0.597 | **0.606** |
| Plastic bag - wrapper | 0.650 | 0.509 | 0.540 |
| Carton | 0.585 | 0.506 | 0.510 |
| Bottle cap | 0.781 | 0.367 | 0.481 |
| Aluminium foil | 0.894 | 0.452 | 0.471 |
| Lid | 0.670 | 0.409 | 0.418 |
| Paper | 0.732 | 0.360 | 0.395 |
| Straw | 0.637 | 0.342 | 0.380 |
| Plastic container | 0.616 | 0.300 | 0.324 |
| Other litter | 0.629 | 0.258 | 0.298 |
| Styrofoam piece | 0.675 | 0.239 | 0.272 |
| Other plastic | 0.805 | 0.211 | 0.240 |
| Unlabeled litter | 0.711 | 0.144 | 0.235 |
| Cigarette | 0.688 | 0.117 | 0.172 |
| Pop tab | 0.496 | 0.080 | 0.086 |
| Broken glass | 0.165 | 0.065 | 0.051 |

- **Mejor:** `Bottle`, `Can`, `Cup` (objetos grandes y frecuentes).
- **Peor:** `Broken glass`, `Pop tab`, `Cigarette` (objetos **muy pequeños** y/o
  con pocos ejemplos).

## 📈 Curvas (`results.png`)
- Todas las **pérdidas bajan** (train y val) → aprende bien, **sin overfitting**.
- `mAP50` y `mAP50-95` **siguen subiendo levemente al final** → con más épocas
  (80) podría mejorar un poco más.
- Precisión decente (~0.65) pero **recall bajo (~0.35)**: el modelo es "cauto",
  acierta cuando detecta pero **se le escapan muchos objetos**.

## 🔢 Matriz de confusión — el hallazgo clave
La fila **`background`** tiene valores enormes (Cigarette 464, Plastic bag 272,
Other plastic 170…). Esto significa **muchos objetos reales NO detectados** (los
toma como fondo) → es la causa del **recall bajo**.

**Por qué:** TACO tiene objetos diminutos (colillas, tapas, trozos de vidrio) en
escenas complejas; detectarlos es muy difícil para un modelo nano a 640 px.

## ✅ Conclusiones
1. **Objetivo cumplido:** el modelo **detecta varios residuos por imagen**.
2. Funciona bien con **objetos grandes y comunes** (botellas, latas, vasos, cartones).
3. Le cuestan los **objetos pequeños** (colillas, vidrio roto) → se pierden.
4. El **trade-off es claro y defendible**: pasamos de un detector "de laboratorio"
   (mAP 0.93, 1 objeto) a uno **realista multi-objeto** (mAP 0.38, escenas reales).

## 🔼 Mejora aplicada: YOLO11n → YOLO11s

Se re-entrenó con **`yolo11s`** (9.4 M parámetros, ~4x el nano), a 640 px y 60
épocas (~1.8 h). Resultado:

| Métrica | yolo11n | **yolo11s** | Cambio |
|---------|---------|-------------|--------|
| mAP@0.5 | 0.379 | **0.419** | +0.040 |
| mAP@0.5:0.95 | 0.289 | **0.320** | +0.031 |
| Precisión | 0.651 | **0.667** | +0.016 |
| Recall | 0.347 | **0.393** | +0.046 |

Mejoraron sobre todo clases difíciles: `Cigarette` (0.17→0.26), `Lid` (0.42→0.53),
`Bottle cap` (0.48→0.56), `Can` (0.66→0.72). Modelo en Drive:
`taco_runs/residuos_taco_s/weights/best.pt`.

> ⚠️ **Lección aprendida:** al evaluar/inferir, **cargar siempre `best.pt`
> explícitamente** (`YOLO("best.pt")`). Si se reutiliza una variable que quedó
> apuntando al modelo base de fábrica, aparecen clases COCO (person, car…) en vez
> de las de residuos.

## 🚀 Mejoras futuras (para la defensa)
- Entrenar más épocas (80+) — las curvas aún subían.
- Usar un modelo mayor (`yolo11s`/`yolo11m`) o mayor resolución (`imgsz=1280`)
  para los objetos pequeños.
- Agrupar las 18 clases en super-categorías (plástico, metal, vidrio…) para subir
  el mAP por clase.
- Aumentar ejemplos de las clases minoritarias (`Broken glass`, `Pop tab`).
