"""
Verifica que el dataset de residuos esté correctamente descargado en data/raw/.

No requiere dependencias externas: usa solo la librería estándar de Python,
así que puedes ejecutarlo sin instalar nada:

    py src/verificar_dataset.py
"""
import sys
from pathlib import Path

# Asegura que los acentos y la ñ se muestren bien en consolas de Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
EXTS_IMG = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def contar(carpeta: Path, exts: set) -> int:
    """Cuenta archivos con ciertas extensiones dentro de una carpeta (recursivo)."""
    if not carpeta.exists():
        return 0
    return sum(1 for p in carpeta.rglob("*") if p.suffix.lower() in exts)


def buscar_split(nombre: str):
    """Localiza la carpeta de imágenes de un split (train/valid/test)."""
    for patron in (f"{nombre}/images", nombre):
        for c in RAW.rglob(patron):
            if c.is_dir() and contar(c, EXTS_IMG) > 0:
                return c
    return None


def main():
    print("=" * 60)
    print(" VERIFICACIÓN DEL DATASET DE RESIDUOS")
    print("=" * 60)
    print(f"Carpeta: {RAW}\n")

    if not RAW.exists():
        print("[X] La carpeta data/raw/ no existe todavía.")
        return

    # --- data.yaml ---
    yamls = list(RAW.rglob("data.yaml"))
    if yamls:
        print(f"[OK] data.yaml encontrado:\n     {yamls[0]}")
        print("-" * 60)
        print(yamls[0].read_text(encoding="utf-8", errors="ignore").strip())
        print("-" * 60)
    else:
        print("[!] No se encontró data.yaml. ¿Descomprimiste el ZIP dentro de data/raw/?")

    # --- conteo de imágenes y etiquetas por split ---
    print("\nConteo por partición:")
    total_img = 0
    for split in ("train", "valid", "test"):
        carpeta_img = buscar_split(split)
        n_img = contar(carpeta_img, EXTS_IMG) if carpeta_img else 0
        # las etiquetas suelen estar en ../labels respecto a images
        n_lbl = 0
        if carpeta_img:
            labels = carpeta_img.parent / "labels"
            n_lbl = contar(labels, {".txt"})
        total_img += n_img
        estado = "OK" if n_img > 0 else "--"
        print(f"  [{estado}] {split:6}: {n_img:5} imágenes / {n_lbl:5} etiquetas")

    print(f"\nTotal de imágenes: {total_img}")
    if total_img > 0:
        print("\n[LISTO] Dataset detectado correctamente.")
        print("        Siguiente paso -> Fase 2: exploración de datos (EDA).")
    else:
        print("\n[PENDIENTE] Aún no hay imágenes.")
        print("            Descarga y descomprime el dataset en data/raw/")
        print("            (ver instrucciones en data/README.md).")


if __name__ == "__main__":
    main()
