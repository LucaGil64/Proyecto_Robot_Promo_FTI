from typing import Dict

from config import SOLUCION_GRUPO_06
from pipeline import ejecutar_programa


def ejecutar_pruebas(instancia: Dict) -> None:
    pruebas = [
        ("1. Válido: Programa completo del grupo", SOLUCION_GRUPO_06, "Misión resuelta"),
        ("2. Error Léxico: Palabra no permitida", "arriba saltar viaje", "Error léxico"),
        ("3. Rechazo AP: Camino de regreso no inverso", "arriba viaje arriba agarrar arriba soltar finviaje", "Rechazo del AP"),
        ("4. Rechazo AP: Soltar antes de vaciar pila", "arriba viaje arriba arriba agarrar abajo soltar finviaje", "Rechazo del AP"),
        ("5. Rechazo AP: Segundo agarrar en el mismo viaje", "arriba viaje arriba agarrar agarrar abajo soltar finviaje", "Rechazo del AP"),
        ("6. Rechazo AP: Falta finviaje al cerrar viaje", "arriba viaje arriba agarrar abajo soltar", "Rechazo del AP"),
        ("7. Error Físico: Intentar agarrar en celda vacía", "arriba viaje arriba agarrar abajo soltar finviaje", "Error físico"),
        ("8. Error Físico: Choque contra obstáculo (5,3)", "arriba derecha derecha viaje arriba agarrar abajo soltar finviaje", "Error físico"),
        ("9. Error Físico: Salida de los límites de la grilla", "izquierda viaje agarrar soltar finviaje", "Error físico"),
        ("10. Incompleto: Programa válido sin completar cajas", "arriba viaje arriba arriba arriba arriba agarrar abajo abajo abajo abajo soltar finviaje", "Objetivo no alcanzado"),
        ("11. Borde: Entrada vacía", "", "Rechazo del AP"),
    ]

    print("=== BATERÍA DE PRUEBAS MÍNIMAS Y CASOS DE BORDE (automata-lib DPDA) ===")
    for nombre, entrada, esperado in pruebas:
        res = ejecutar_programa(entrada, instancia)
        ok = "PASS" if res["categoria"] == esperado else "FAIL"
        print(f"[{ok}] {nombre}")
        print(f"       Esperado : {esperado}")
        print(f"       Obtenido : {res['categoria']} -> {res['detalle']}")