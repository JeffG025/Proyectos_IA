"""
Demo de detección de residuos sobre imágenes (Fase 5).

Usa el modelo entrenado (models/best.pt) para detectar residuos en imágenes,
dibuja las cajas con su clase y guarda el resultado en
docs/figuras/predicciones/.

Ejemplos de uso (con el Python del entorno virtual):

    # 1) Sobre una imagen concreta:
    .venv\\Scripts\\python.exe src\\predecir.py "C:\\ruta\\a\\imagen.jpg"

    # 2) Sobre una carpeta de imágenes:
    .venv\\Scripts\\python.exe src\\predecir.py "C:\\ruta\\a\\carpeta"

    # 3) Sin argumentos: toma una muestra del conjunto de test
    .venv\\Scripts\\python.exe src\\predecir.py
"""
import sys
import random
from pathlib import Path

# Acentos correctos en consolas de Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from ultralytics import YOLO
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "models" / "residuos_taco_s.pt"   # mejor modelo (multi-objeto)
TEST_IMAGES = RAIZ / "data" / "raw" / "test" / "images"
SALIDA = RAIZ / "docs" / "figuras" / "predicciones"
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
CONF = 0.20  # umbral de confianza (detecciones por debajo se descartan)


def obtener_imagenes(arg):
    """Decide qué imágenes procesar según el argumento recibido."""
    if arg:
        p = Path(arg)
        if p.is_dir():
            return sorted(x for x in p.glob("*") if x.suffix.lower() in EXTS)
        if p.is_file():
            return [p]
        print(f"[X] No existe la ruta: {p}")
        return []
    # Sin argumento -> muestra aleatoria del conjunto de test
    imgs = sorted(TEST_IMAGES.glob("*.jpg"))
    if not imgs:
        return []
    random.seed(7)
    return random.sample(imgs, min(6, len(imgs)))


def main():
    if not MODELO.exists():
        print(f"[X] No encuentro el modelo en {MODELO}")
        print("    Descarga best.pt de Colab y colócalo en la carpeta models/.")
        return

    arg = sys.argv[1] if len(sys.argv) > 1 else None
    imagenes = obtener_imagenes(arg)
    if not imagenes:
        print("[X] No hay imágenes para procesar.")
        return

    SALIDA.mkdir(parents=True, exist_ok=True)
    print(f"Modelo  : {MODELO}")
    print(f"Imágenes: {len(imagenes)}")
    print(f"Salida  : {SALIDA}\n")

    model = YOLO(str(MODELO))

    total_detecciones = 0
    for img in imagenes:
        resultados = model.predict(source=str(img), conf=CONF, verbose=False)
        r = resultados[0]

        # r.plot() devuelve la imagen con las cajas dibujadas (array BGR)
        anotada = r.plot()
        Image.fromarray(anotada[..., ::-1]).save(SALIDA / f"pred_{img.name}")

        n = len(r.boxes)
        total_detecciones += n
        clases = [model.names[int(c)] for c in r.boxes.cls.tolist()] if n else []
        print(f"  {img.name:42} -> {n} detección(es): {clases}")

    print(f"\n[LISTO] {total_detecciones} detecciones en {len(imagenes)} imágenes.")
    print(f"        Revisa los resultados en: {SALIDA}")


if __name__ == "__main__":
    main()
