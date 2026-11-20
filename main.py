import json
import sys

from config import INSTANCIA_GRUPO_06, SOLUCION_GRUPO_06
from pipeline import ejecutar_programa
from pruebas import ejecutar_pruebas
from reportes import guardar_registro_csv, guardar_registro_txt


def main() -> None:
    if len(sys.argv) == 1:
        ejecutar_pruebas(INSTANCIA_GRUPO_06)
        res = ejecutar_programa(SOLUCION_GRUPO_06, INSTANCIA_GRUPO_06)
        guardar_registro_csv(res["registro"], "registros/registro_grupo06.csv")
        guardar_registro_txt(res, "registros/registro_grupo06.txt")
        print("\nArchivos generados y guardados en la carpeta registros: registro_grupo06.csv y registro_grupo06.txt")
        return

    ruta_prog = sys.argv[1]
    with open(ruta_prog, "r", encoding="utf-8") as fp:
        texto = fp.read()

    instancia = INSTANCIA_GRUPO_06
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "r", encoding="utf-8") as fi:
            instancia = json.load(fi)

    res = ejecutar_programa(texto, instancia)
    print(f"Resultado: {res['categoria']}")
    print(f"Detalle:   {res['detalle']}")
    if res["registro"]:
        guardar_registro_csv(res["registro"], "registros/registro_salida.csv")
        guardar_registro_txt(res, "registros/registro_salida.txt")
        print("Registro guardado en registros/registro_salida.csv y registros/registro_salida.txt")


if __name__ == "__main__":
    main()