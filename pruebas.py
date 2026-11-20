from typing import Dict

from config import SOLUCION_GRUPO_06
from pipeline import ejecutar_programa


def ejecutar_pruebas(instancia: Dict) -> None:
    pruebas = [
        ("1. Solución completa correcta (Grupo 06)", SOLUCION_GRUPO_06, "Misión resuelta"),
        ("2. Regreso con orden no inverso", "viaje arriba derecha agarrar abajo abajo soltar finviaje", "Rechazo del AP"),
        ("3. soltar antes de terminar el regreso", "viaje arriba derecha agarrar izquierda soltar abajo finviaje", "Rechazo del AP"),
        ("4. Viaje sin cierre finviaje", "viaje arriba agarrar abajo soltar", "Rechazo del AP"),
        ("5. Segundo agarrar en el mismo viaje", "viaje arriba agarrar agarrar abajo soltar finviaje", "Rechazo del AP"),
        ("6. Programa válido en AP que atraviesa obstáculo (5,3)", "derecha derecha arriba viaje arriba agarrar abajo soltar finviaje", "Error físico"),
        ("7. Programa válido en AP que agarra en celda vacía (6,1)", "viaje agarrar soltar finviaje", "Error físico"),
        ("8. Programa válido ejecutable que no alcanza la meta", "arriba viaje arriba arriba arriba arriba agarrar abajo abajo abajo abajo soltar finviaje abajo", "Objetivo no alcanzado"),
        ("9. Borde: Token desconocido", "arriba diagonal viaje agarrar soltar finviaje", "Error léxico"),
        ("10. Borde: Entrada vacía", "", "Rechazo del AP"),
        ("11. Borde: Salida de la grilla", "izquierda viaje arriba agarrar abajo soltar finviaje", "Error físico"),
    ]

    print("=== BATERÍA DE PRUEBAS MÍNIMAS Y CASOS DE BORDE (automata-lib DPDA) ===")
    for nombre, entrada, esperado in pruebas:
        res = ejecutar_programa(entrada, instancia)
        ok = "PASS" if res["categoria"] == esperado else "FAIL"
        print(f"[{ok}] {nombre}")
        print(f"       Esperado : {esperado}")
        print(f"       Obtenido : {res['categoria']} -> {res['detalle']}")