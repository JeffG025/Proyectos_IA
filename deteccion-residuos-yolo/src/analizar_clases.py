"""
Análisis de distribución de clases del dataset de residuos (Fase 2 - EDA).

Lee las etiquetas YOLO (.txt) y cuenta cuántos objetos (cajas) hay de cada clase
en cada partición (train/valid/test). Sirve para detectar desbalance de clases.

No requiere dependencias externas (solo librería estándar):

    py src/analizar_clases.py
"""
import sys
import ast
from pathlib import Path
from collections import Counter

# Acentos correctos en consolas de Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
SPLITS = ("train", "valid", "test")


def cargar_nombres_clases():
    """Lee la lista de nombres de clase desde data.yaml (sin librería de YAML)."""
    yaml_path = next(RAW.rglob("data.yaml"), None)
    if not yaml_path:
        return None
    for linea in yaml_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        linea = linea.strip()
        if linea.startswith("names:"):
            valor = linea.split(":", 1)[1].strip()
            try:
                return ast.literal_eval(valor)  # ej: ['Trash', 'cardboard', ...]
            except Exception:
                return None
    return None


def contar_split(split: str):
    """Devuelve (conteo_por_clase, num_imagenes, num_objetos) de un split."""
    conteo = Counter()
    n_labels = 0
    n_objetos = 0
    for labels_dir in RAW.rglob(f"{split}/labels"):
        for txt in labels_dir.glob("*.txt"):
            n_labels += 1
            for linea in txt.read_text(errors="ignore").splitlines():
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    cls_id = int(linea.split()[0])
                except (ValueError, IndexError):
                    continue
                conteo[cls_id] += 1
                n_objetos += 1
    return conteo, n_labels, n_objetos


def barra(valor, maximo, ancho=40):
    if maximo <= 0:
        return ""
    return "#" * max(1, round(ancho * valor / maximo))


def main():
    print("=" * 64)
    print(" ANÁLISIS DE DISTRIBUCIÓN DE CLASES (EDA)")
    print("=" * 64)

    nombres = cargar_nombres_clases()
    if not nombres:
        print("[X] No pude leer los nombres de clase de data.yaml.")
        return
    print(f"Clases ({len(nombres)}): {nombres}\n")

    total_global = Counter()
    por_split = {}
    imgs_split = {}
    objs_split = {}
    for split in SPLITS:
        conteo, n_img, n_obj = contar_split(split)
        por_split[split] = conteo
        imgs_split[split] = n_img
        objs_split[split] = n_obj
        total_global.update(conteo)

    # --- Tabla: objetos por clase y partición ---
    print(f"{'Clase':<12}{'train':>8}{'valid':>8}{'test':>8}{'TOTAL':>9}")
    print("-" * 64)
    for i, nombre in enumerate(nombres):
        tr = por_split['train'].get(i, 0)
        va = por_split['valid'].get(i, 0)
        te = por_split['test'].get(i, 0)
        print(f"{nombre:<12}{tr:>8}{va:>8}{te:>8}{tr+va+te:>9}")
    print("-" * 64)
    gtr, gva, gte = (objs_split['train'], objs_split['valid'], objs_split['test'])
    print(f"{'TOTAL objetos':<12}{gtr:>8}{gva:>8}{gte:>8}{gtr+gva+gte:>9}")

    # --- Objetos por imagen ---
    print("\nObjetos por imagen (promedio):")
    for split in SPLITS:
        n_img = imgs_split[split]
        prom = (objs_split[split] / n_img) if n_img else 0
        print(f"  {split:6}: {objs_split[split]:>6} objetos / {n_img:>5} imágenes = {prom:.2f} obj/img")

    # --- Histograma del total por clase ---
    print("\nDistribución total de objetos por clase:")
    maximo = max(total_global.values()) if total_global else 0
    for i, nombre in enumerate(nombres):
        v = total_global.get(i, 0)
        print(f"  {nombre:<11}{v:>6}  {barra(v, maximo)}")

    # --- Diagnóstico de balance ---
    valores = [total_global.get(i, 0) for i in range(len(nombres))]
    if valores and min(valores) > 0:
        mx, mn = max(valores), min(valores)
        ratio = mx / mn
        print(f"\nClase más frecuente : {nombres[valores.index(mx)]} ({mx} objetos)")
        print(f"Clase menos frecuente: {nombres[valores.index(mn)]} ({mn} objetos)")
        print(f"Ratio de desbalance (máx/mín): {ratio:.1f}x")
        if ratio >= 3:
            print("[!] Desbalance notable -> conviene vigilar el recall de las clases minoritarias.")
        else:
            print("[OK] El dataset está razonablemente balanceado.")


if __name__ == "__main__":
    main()
