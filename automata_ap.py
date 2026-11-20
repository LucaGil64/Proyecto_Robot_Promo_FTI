from typing import Dict, List, Optional, Tuple

from automata.base.exceptions import RejectionException
from automata.pda.dpda import DPDA

from config import SIMBOLO_A_TOKEN, TOKEN_A_SIMBOLO
from lexico import Token


def construir_dpda() -> DPDA:
    """Construye el Autómata a Pila Determinista (APD) usando automata-lib."""
    stack_symbols = {"Z", "U", "D", "L", "R"}
    dirs = ("U", "D", "L", "R")

    transiciones_q1: Dict[str, Dict[str, Tuple]] = {
        d: {x: ("q1", (d, x)) for x in stack_symbols} for d in dirs
    }
    transiciones_q1["G"] = {x: ("q2", (x,)) for x in stack_symbols}

    return DPDA(
        states={"q0", "q1", "q2", "q3", "q4"},
        input_symbols=set(TOKEN_A_SIMBOLO.values()),
        stack_symbols=stack_symbols,
        transitions={
            "q0": {
                **{d: {"Z": ("q0", ("Z",))} for d in dirs},
                "V": {"Z": ("q1", ("Z",))},
            },
            "q1": transiciones_q1,
            "q2": {
                "D": {"U": ("q2", "")},
                "U": {"D": ("q2", "")},
                "R": {"L": ("q2", "")},
                "L": {"R": ("q2", "")},
                "S": {"Z": ("q3", ("Z",))},
            },
            "q3": {
                "F": {"Z": ("q4", ("Z",))},
            },
            "q4": {
                **{d: {"Z": ("q4", ("Z",))} for d in dirs},
                "V": {"Z": ("q1", ("Z",))},
            },
        },
        initial_state="q0",
        initial_stack_symbol="Z",
        final_states={"q4"},
        acceptance_mode="final_state",
    )


def formatear_pila(pda_stack) -> Tuple[str, int]:
    """Convierte el PDAStack de automata-lib a [tope, ..., Z0] legible."""
    elementos = list(getattr(pda_stack, "stack", tuple(pda_stack)))
    legibles = [
        "Z0" if s == "Z" else SIMBOLO_A_TOKEN.get(s, s)
        for s in reversed(elementos)
    ]
    altura_sin_fondo = max(0, len(elementos) - 1)
    return "[" + ", ".join(legibles) + "]", altura_sin_fondo


def validar_protocolo_ap(tokens: List[Token]) -> Tuple[bool, Optional[List], str]:
    """Ejecuta el DPDA sobre los tokens y devuelve las configuraciones paso a paso."""
    dpda = construir_dpda()
    cadena_simbolos = "".join(t.simbolo for t in tokens)
    configs = []
    paso_actual = 0

    try:
        for cfg in dpda.read_input_stepwise(cadena_simbolos):
            configs.append(cfg)
            paso_actual += 1
    except RejectionException as exc:
        idx_consumidos = max(0, paso_actual - 1)
        if not tokens:
            detalle = "Entrada vacía o sin ningún bloque 'viaje ... finviaje'."
        elif idx_consumidos < len(tokens):
            tok = tokens[idx_consumidos]
            detalle = (
                f"Token #{tok.indice} ('{tok.valor}', línea {tok.linea}, "
                f"col {tok.columna}): {exc}"
            )
        else:
            ultimo_estado = configs[-1].state if configs else dpda.initial_state
            detalle = (
                f"Fin de entrada inesperado en estado {ultimo_estado} "
                f"(viaje sin cierre 'finviaje')."
            )
        return False, None, detalle

    # Sin transiciones epsilon, configs[1:] corresponde 1-a-1 con cada token
    return True, configs[1:], ""