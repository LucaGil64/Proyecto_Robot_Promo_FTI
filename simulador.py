from typing import Dict, List, Set, Tuple

from automata_ap import formatear_pila
from config import DIRECCIONES
from lexico import Token


def renderizar_grilla(
    filas: int,
    columnas: int,
    robot: Tuple[int, int],
    cajas: Set[Tuple[int, int]],
    obstaculos: Set[Tuple[int, int]],
    destinos: Set[Tuple[int, int]],
) -> str:
    encabezado = "    " + "   ".join(str(c) for c in range(1, columnas + 1))
    sep = "  +" + "---+" * columnas
    lineas = [encabezado, sep]

    for f in range(1, filas + 1):
        celdas = []
        for c in range(1, columnas + 1):
            pos = (f, c)
            if pos in obstaculos:
                sim = "X"
            elif pos == robot and pos in cajas:
                sim = "*"
            elif pos == robot:
                sim = "R"
            elif pos in cajas:
                sim = "C"
            elif pos in destinos:
                sim = "T"
            else:
                sim = " "
            celdas.append(f" {sim} ")
        lineas.append(f"{f} |" + "|".join(celdas) + "|")
        lineas.append(sep)

    return "\n".join(lineas)


def simular_mundo(tokens: List[Token], configs_por_token: List, instancia: Dict) -> Dict:
    filas = instancia["filas"]
    columnas = instancia["columnas"]
    robot = tuple(instancia["robot_inicial"])
    robot_final = tuple(instancia["robot_final"])
    cajas = {tuple(p) for p in instancia["cajas"]}
    obstaculos = {tuple(p) for p in instancia["obstaculos"]}
    destinos = {tuple(p) for p in instancia["destinos"]}
    pinza_cargada = False

    registro = []
    mov_sin_carga = 0
    mov_con_carga = 0
    max_altura_pila = 0

    for tok, cfg in zip(tokens, configs_por_token):
        orden = tok.valor

        if orden in DIRECCIONES:
            df, dc = DIRECCIONES[orden]
            nueva_pos = (robot[0] + df, robot[1] + dc)

            if not (1 <= nueva_pos[0] <= filas and 1 <= nueva_pos[1] <= columnas):
                return {
                    "categoria": "Error físico",
                    "detalle": (
                        f"Token #{tok.indice} ('{orden}'): el robot intenta salir de "
                        f"la grilla desde {robot} hacia {nueva_pos}."
                    ),
                    "registro": registro,
                    "metricas": {},
                }

            if nueva_pos in obstaculos:
                return {
                    "categoria": "Error físico",
                    "detalle": (
                        f"Token #{tok.indice} ('{orden}'): el robot intenta atravesar "
                        f"un obstáculo en {nueva_pos}."
                    ),
                    "registro": registro,
                    "metricas": {},
                }

            robot = nueva_pos
            if pinza_cargada:
                mov_con_carga += 1
            else:
                mov_sin_carga += 1

        elif orden == "agarrar":
            if pinza_cargada:
                return {
                    "categoria": "Error físico",
                    "detalle": f"Token #{tok.indice} ('agarrar'): la pinza ya transporta una caja.",
                    "registro": registro,
                    "metricas": {},
                }
            if robot not in cajas:
                return {
                    "categoria": "Error físico",
                    "detalle": f"Token #{tok.indice} ('agarrar'): no hay ninguna caja en la celda {robot}.",
                    "registro": registro,
                    "metricas": {},
                }
            cajas.remove(robot)
            pinza_cargada = True

        elif orden == "soltar":
            if not pinza_cargada:
                return {
                    "categoria": "Error físico",
                    "detalle": f"Token #{tok.indice} ('soltar'): la pinza está vacía.",
                    "registro": registro,
                    "metricas": {},
                }
            if robot in cajas:
                return {
                    "categoria": "Error físico",
                    "detalle": f"Token #{tok.indice} ('soltar'): ya existe una caja en {robot} (no se apilan).",
                    "registro": registro,
                    "metricas": {},
                }
            cajas.add(robot)
            pinza_cargada = False

        pila_txt, altura = formatear_pila(cfg.stack)
        if altura > max_altura_pila:
            max_altura_pila = altura

        registro.append(
            {
                "indice": tok.indice,
                "orden": orden,
                "estado_ap": cfg.state,
                "pila": pila_txt,
                "posicion": f"({robot[0]},{robot[1]})",
                "carga": "con_caja" if pinza_cargada else "vacia",
            }
        )

    metricas = {
        "movimientos_sin_carga": mov_sin_carga,
        "movimientos_con_carga": mov_con_carga,
        "total_movimientos": mov_sin_carga + mov_con_carga,
        "altura_maxima_pila": max_altura_pila,
        "grilla_inicial": renderizar_grilla(
            filas,
            columnas,
            tuple(instancia["robot_inicial"]),
            {tuple(p) for p in instancia["cajas"]},
            obstaculos,
            destinos,
        ),
        "grilla_final": renderizar_grilla(
            filas, columnas, robot, cajas, obstaculos, destinos
        ),
    }

    if cajas == destinos and robot == robot_final and not pinza_cargada:
        return {
            "categoria": "Misión resuelta",
            "detalle": "Todas las cajas están en los destinos, el robot volvió a la posición final y la pinza está vacía.",
            "registro": registro,
            "metricas": metricas,
        }

    faltantes = sorted(destinos - cajas)
    return {
        "categoria": "Objetivo no alcanzado",
        "detalle": (
            f"Ejecución válida pero incompleta. Posición final: {robot} (esperada {robot_final}), "
            f"pinza cargada: {pinza_cargada}, destinos sin caja: {faltantes}."
        ),
        "registro": registro,
        "metricas": metricas,
    }