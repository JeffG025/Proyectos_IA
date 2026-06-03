"""
Visualización del dataset de residuos (Fase 2 - EDA).

Genera dos figuras en docs/figuras/:
  1. distribucion_clases.png  -> gráfico de barras de objetos por clase
  2. muestras.png             -> mosaico de imágenes reales con sus cajas

Requiere matplotlib y pillow (instalados en el .venv del proyecto). Ejecutar con
el Python del entorno virtual:

    .venv\\Scripts\\python.exe src\\visualizar_muestras.py
"""
import ast
import random
from pathlib import Path
from collections import Counter

import matplotlib
matplotlib.use("Agg")  # backend sin ventana: solo guarda archivos
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
FIGURAS = RAIZ / "docs" / "figuras"
FIGURAS.mkdir(parents=True, exist_ok=True)

# Un color por clase (consistente entre figuras)
COLORES = ["#e6194B", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#42d4f4"]


def cargar_nombres():
    """Nombres de clase desde data.yaml."""
    yaml_path = next(RAW.rglob("data.yaml"), None)
    for linea in yaml_path.read_text(encoding="utf-8").splitlines():
        if linea.strip().startswith("names:"):
            return ast.literal_eval(linea.split(":", 1)[1].strip())
    return None


def contar_por_clase(n_clases):
    """Total de objetos por id de clase, sumando todas las particiones."""
    conteo = Counter()
    for split in ("train", "valid", "test"):
        for labels_dir in RAW.rglob(f"{split}/labels"):
            for txt in labels_dir.glob("*.txt"):
                for linea in txt.read_text().splitlines():
                    if linea.strip():
                        conteo[int(linea.split()[0])] += 1
    return [conteo.get(i, 0) for i in range(n_clases)]


def grafico_distribucion(nombres, valores):
    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.bar(nombres, valores, color=COLORES)
    ax.set_title("Distribución de clases — Dataset de residuos",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("Nº de objetos (cajas)")
    ax.set_xlabel("Clase")
    ax.bar_label(barras, padding=3)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    salida = FIGURAS / "distribucion_clases.png"
    plt.savefig(salida, dpi=120)
    plt.close(fig)
    return salida


def leer_cajas(txt_path):
    """Cajas de un .txt YOLO: lista de (cls, x_centro, y_centro, ancho, alto)."""
    cajas = []
    if txt_path.exists():
        for linea in txt_path.read_text().splitlines():
            p = linea.split()
            if len(p) == 5:
                cajas.append((int(p[0]), *map(float, p[1:])))
    return cajas


def mosaico_muestras(nombres, n=9):
    img_dir = next((d for d in RAW.rglob("train/images") if d.is_dir()), None)
    lbl_dir = img_dir.parent / "labels"
    imagenes = list(img_dir.glob("*.jpg"))
    random.seed(42)
    seleccion = random.sample(imagenes, min(n, len(imagenes)))

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    for ax, img_path in zip(axes.flat, seleccion):
        img = Image.open(img_path)
        W, H = img.size
        ax.imshow(img)
        for (cls, xc, yc, w, h) in leer_cajas(lbl_dir / (img_path.stem + ".txt")):
            x, y = (xc - w / 2) * W, (yc - h / 2) * H
            color = COLORES[cls % len(COLORES)]
            ax.add_patch(patches.Rectangle((x, y), w * W, h * H,
                                           linewidth=2, edgecolor=color, facecolor="none"))
            ax.text(x, max(y - 6, 0), nombres[cls], color="white", fontsize=10,
                    bbox=dict(facecolor=color, edgecolor="none", pad=1))
        ax.axis("off")
    for ax in axes.flat[len(seleccion):]:
        ax.axis("off")
    fig.suptitle("Muestras del dataset con sus anotaciones (cajas reales)",
                 fontsize=15, fontweight="bold")
    plt.tight_layout()
    salida = FIGURAS / "muestras.png"
    plt.savefig(salida, dpi=110)
    plt.close(fig)
    return salida


def main():
    nombres = cargar_nombres()
    print("Clases:", nombres)

    valores = contar_por_clase(len(nombres))
    print("[OK] Guardado:", grafico_distribucion(nombres, valores))
    print("[OK] Guardado:", mosaico_muestras(nombres))
    print("\nListo. Revisa la carpeta docs/figuras/")


if __name__ == "__main__":
    main()
