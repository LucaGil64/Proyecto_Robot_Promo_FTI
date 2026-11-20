DIRECCIONES = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1),
}

# automata-lib exige símbolos de entrada de 1 carácter
TOKEN_A_SIMBOLO = {
    "arriba": "U",
    "abajo": "D",
    "izquierda": "L",
    "derecha": "R",
    "agarrar": "G",
    "soltar": "S",
    "viaje": "V",
    "finviaje": "F",
}

SIMBOLO_A_TOKEN = {v: k for k, v in TOKEN_A_SIMBOLO.items()}
PALABRAS_RESERVADAS = set(TOKEN_A_SIMBOLO.keys())

INSTANCIA_GRUPO_06 = {
    "grupo": "Grupo 06 - Dos pedidos",
    "filas": 6,
    "columnas": 6,
    "robot_inicial": [6, 1],
    "robot_final": [6, 1],
    "cajas": [[1, 1], [1, 5], [2, 3], [3, 6]],
    "obstaculos": [[2, 2], [2, 4], [3, 4], [5, 3]],
    "destinos": [[4, 1], [5, 1], [4, 5], [5, 5]],
}

SOLUCION_GRUPO_06 = """
arriba
viaje arriba arriba arriba arriba agarrar abajo abajo abajo abajo soltar finviaje
arriba
viaje arriba derecha derecha arriba agarrar abajo izquierda izquierda abajo soltar finviaje
derecha derecha derecha derecha
viaje arriba arriba arriba agarrar abajo abajo abajo soltar finviaje
abajo
viaje derecha arriba arriba agarrar abajo abajo izquierda soltar finviaje
abajo izquierda izquierda izquierda izquierda
""".strip()

