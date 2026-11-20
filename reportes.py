import csv
import os
from typing import Dict, List


def guardar_registro_csv(registro: List[Dict], ruta: str) -> None:
    campos = ["indice", "orden", "estado_ap", "pila", "posicion", "carga"]
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registro)


def guardar_registro_txt(res: Dict, ruta: str) -> None:
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Resultado: {res['categoria']}\n")
        f.write(f"Detalle: {res['detalle']}\n\n")
        if res["metricas"]:
            m = res["metricas"]
            f.write("=== GRILLA INICIAL ===\n" + m["grilla_inicial"] + "\n\n")
            f.write("=== GRILLA FINAL ===\n" + m["grilla_final"] + "\n\n")
            f.write(f"Movimientos sin carga: {m['movimientos_sin_carga']}\n")
            f.write(f"Movimientos con carga: {m['movimientos_con_carga']}\n")
            f.write(f"Total de movimientos:  {m['total_movimientos']}\n")
            f.write(f"Altura máxima de pila (sin Z0): {m['altura_maxima_pila']}\n\n")
        f.write("=== REGISTRO POR TOKEN ===\n")
        f.write(f"{'IDX':>3} | {'ORDEN':<10} | {'AP':<3} | {'POS':<5} | {'CARGA':<8} | PILA\n")
        f.write("-" * 72 + "\n")
        for r in res["registro"]:
            f.write(
                f"{r['indice']:>3} | {r['orden']:<10} | {r['estado_ap']:<3} | "
                f"{r['posicion']:<5} | {r['carga']:<8} | {r['pila']}\n"
            )