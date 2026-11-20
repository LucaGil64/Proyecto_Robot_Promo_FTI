from typing import Dict

from automata_ap import validar_protocolo_ap
from lexico import analizar_lexico
from simulador import simular_mundo


def ejecutar_programa(texto_programa: str, instancia: Dict) -> Dict:
    # Fase 1: Análisis léxico
    tokens, error_lexico = analizar_lexico(texto_programa)
    if error_lexico is not None or tokens is None:
        return {
            "categoria": "Error léxico",
            "detalle": error_lexico,
            "registro": [],
            "metricas": {},
        }

    # Fase 2: Validación del protocolo con el Autómata a Pila (APD)
    ok_ap, configs_por_token, detalle_ap = validar_protocolo_ap(tokens)
    if not ok_ap or configs_por_token is None:
        return {
            "categoria": "Rechazo del AP",
            "detalle": detalle_ap,
            "registro": [],
            "metricas": {},
        }

    # Fase 3: Simulación física del mundo y verificación de meta
    return simular_mundo(tokens, configs_por_token, instancia)