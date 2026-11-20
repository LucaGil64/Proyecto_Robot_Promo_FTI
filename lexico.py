from dataclasses import dataclass
from typing import List, Optional, Tuple

from config import PALABRAS_RESERVADAS, TOKEN_A_SIMBOLO


@dataclass
class Token:
    indice: int
    valor: str
    simbolo: str
    linea: int
    columna: int


def analizar_lexico(texto: str) -> Tuple[Optional[List[Token]], Optional[str]]:
    tokens: List[Token] = []
    idx = 0

    for num_linea, linea in enumerate(texto.splitlines(), start=1):
        i = 0
        n = len(linea)
        while i < n:
            if linea[i].isspace():
                i += 1
                continue
            inicio = i
            while i < n and not linea[i].isspace():
                i += 1
            palabra = linea[inicio:i]
            col = inicio + 1

            if palabra not in PALABRAS_RESERVADAS:
                return None, (
                    f"Token desconocido '{palabra}' en índice {idx}, "
                    f"línea {num_linea}, columna {col}."
                )

            tokens.append(
                Token(
                    indice=idx,
                    valor=palabra,
                    simbolo=TOKEN_A_SIMBOLO[palabra],
                    linea=num_linea,
                    columna=col,
                )
            )
            idx += 1

    return tokens, None