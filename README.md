# Robot Recolector — Grupo 06 ("Dos pedidos")

**Asignatura:** Fundamentos Teóricos de la Informática — Trabajo Práctico de Promoción  
**Lenguaje / Stack:** Python 3.12.3 + `automata-lib` (`DPDA`)

---

## 1. ¿De qué trata el proyecto?

Este proyecto implementa el **modelado formal, reconocimiento sintáctico y simulación física** de un robot recolector que debe reorganizar cuatro cajas dentro de un depósito representado por una **grilla de 6×6 con obstáculos**.

El robot opera con seis órdenes de acción (`arriba`, `abajo`, `izquierda`, `derecha`, `agarrar`, `soltar`) y dos delimitadores de bloque (`viaje`, `finviaje`) siguiendo un protocolo estricto:
1. Fuera de un viaje solo puede desplazarse con la pinza vacía (sin apilar nada).
2. Al llegar a una celda destino, abre un bloque `viaje` y recorre un camino de ida hasta una caja.
3. Ejecuta exactamente una orden `agarrar`.
4. Debe regresar **obligatoriamente por el camino exactamente inverso** (mismas aristas en orden contrario y dirección opuesta).
5. Ejecuta `soltar` en el punto de partida del viaje y cierra el bloque con `finviaje`.

Dado que el trayecto de vuelta debe ser el espejo inverso del de ida para recorridos de longitud arbitraria, el lenguaje es **Libre de Contexto (Tipo 2 en la Jerarquía de Chomsky)** y requiere memoria LIFO. Por eso el reconocedor está implementado con un **Autómata a Pila Determinista (`DPDA`)** real mediante la librería `automata-lib`.

### Instancia asignada: Grupo 06 · Dos pedidos
* **Grilla:** 6 filas × 6 columnas (fila `1` arriba, columna `1` a la izquierda).
* **Robot inicial y final:** `(6, 1)` con pinza vacía.
* **Cajas iniciales (`C`):** `(1, 1)`, `(1, 5)`, `(2, 3)`, `(3, 6)`.
* **Obstáculos (`X`):** `(2, 2)`, `(2, 4)`, `(3, 4)`, `(5, 3)`.
* **Destinos finales (`T`):** `(4, 1)`, `(5, 1)`, `(4, 5)`, `(5, 5)`.

### Decisión sobre la entrada vacía
El lenguaje **exige al menos un bloque `viaje ... finviaje`** y rechaza la entrada vacía. Esta regla es consistente en la GLC, en el `DPDA` (`q0 ∉ F`) y en la implementación en Python.

---

## 2. Arquitectura del sistema y flujo de ejecución

El proyecto separa estrictamente la **validación formal del protocolo (AP)** de la **simulación física del mundo (grilla 6×6)**. El flujo se divide en tres etapas secuenciales:

```text
  Programa de entrada (.txt / string)
                  │
                  ▼
      [ 1. lexico.py ] ──────────► Error léxico
      Valida palabras reservadas     (informa índice, línea y columna del 1.º error)
                  │
                  ▼
      [ 2. automata_ap.py ] ─────► Rechazo del AP
      DPDA (automata-lib)            (regreso incorrecto, soltar temprano, sin finviaje,
      Valida protocolo y pila         doble agarrar, entrada vacía, etc.)
                  │
                  ▼
      [ 3. simulador.py ] ───────► Error físico
      Ejecuta física en grilla 6x6   (chocar obstáculo, salir de grilla, agarrar en vacío)
                  │
                  ├──────────────► Objetivo no alcanzado
                  │                  (programa válido que no deja cajas en destino o robot en fin)
                  │
                  └──────────────► Misión resuelta
                                     (4 cajas en destinos, robot en (6,1), pinza vacía)
                  │
                  ▼
      [ 4. reportes.py ] ────────► Genera registro_*.csv y registro_*.txt
```

### ¿Por qué validamos primero toda la sintaxis con el AP?
Siguiendo las pautas del trabajo práctico, `pipeline.py` ejecuta primero el análisis léxico y la validación completa del `DPDA` antes de simular los movimientos en la grilla. De esta manera:
* Se garantiza que el AP controla exclusivamente el protocolo y el simulador controla exclusivamente las reglas del mundo y la meta.
* Cualquier falla física (`Error físico`) o misión incompleta (`Objetivo no alcanzado`) queda aislada sobre programas 100% válidos sintácticamente.
* Para las entradas aceptadas por el AP, se genera el registro token por token acoplando las configuraciones del `DPDA` (`estado_ap`, `pila`) con el estado físico del simulador (`posicion`, `carga`).

---

## 3. Estructura del proyecto y qué hace cada archivo

```text
robot_recolector/
├── config.py        # Constantes del lenguaje, mapeo de símbolos e instancia Grupo 06
├── lexico.py        # Analizador léxico y clase Token
├── automata_ap.py   # Autómata a Pila Determinista (DPDA) en automata-lib
├── simulador.py     # Simulador físico de la grilla 6x6, métricas y verificación de meta
├── pipeline.py      # Orquestador de las 3 fases (Léxico -> APD -> Simulador)
├── reportes.py      # Exportación de registros en formato CSV y TXT
├── pruebas.py       # Batería de las 8 pruebas mínimas + 3 casos de borde
├── main.py          # Punto de entrada por línea de comandos (CLI)
└── README.md        # Documentación del proyecto
```

### Detalle de cada módulo

1. **`config.py`**
   * Define los desplazamientos `(df, dc)` para `arriba`, `abajo`, `izquierda`, `derecha`.
   * Define `TOKEN_A_SIMBOLO` y `SIMBOLO_A_TOKEN`: mapeo 1-a-1 entre las palabras reservadas y símbolos de 1 carácter (`U, D, L, R, G, S, V, F`), requerido por la clase `DPDA` de `automata-lib`.
   * Contiene `INSTANCIA_GRUPO_06` (coordenadas exactas del depósito) y `SOLUCION_GRUPO_06` (el programa completo de 56 tokens).

2. **`lexico.py`**
   * Define `Token` (`indice`, `valor`, `simbolo`, `linea`, `columna`).
   * `analizar_lexico(texto)` ignora espacios y saltos de línea, tokeniza las palabras y verifica que pertenezcan a `PALABRAS_RESERVADAS`. Ante el primer token desconocido detiene la ejecución devolviendo su ubicación exacta.

3. **`automata_ap.py`**
   * `construir_dpda()` arma el Autómata a Pila Determinista con sus 7 componentes formales:
     * `states = {"q0", "q1", "q2", "q3", "q4"}`
     * `initial_state = "q0"`, `initial_stack_symbol = "Z"` (representa `Z0`), `final_states = {"q4"}`
     * `acceptance_mode = "final_state"`
   * `validar_protocolo_ap(tokens)` ejecuta `dpda.read_input_stepwise(...)` sobre la secuencia de símbolos. Si ocurre `RejectionException`, identifica el token o condición de fin de entrada que causó el rechazo.
   * `formatear_pila(pda_stack)` convierte la pila interna de `automata-lib` al formato legible `[tope, ..., Z0]` y calcula la altura de pila sin contar `Z0`.

4. **`simulador.py`**
   * `renderizar_grilla(...)` dibuja en texto la grilla 6×6 con `R` (robot), `C` (caja), `X` (obstáculo) y `T` (destino).
   * `simular_mundo(tokens, configs_por_token, instancia)` recorre simultáneamente cada orden y su configuración resultante en el AP:
     * Verifica límites de la grilla (`1..6`) y colisiones contra obstáculos.
     * Valida precondiciones físicas de `agarrar` (pinza vacía y caja presente) y `soltar` (pinza cargada y celda sin caja).
     * Contabiliza movimientos con carga, sin carga y altura máxima de pila (sin `Z0`).
     * Construye el registro por token: `indice`, `orden`, `estado_ap`, `pila`, `posicion` y `carga`.
     * Comprueba si `cajas == destinos`, `robot == robot_final` y `pinza_cargada == False`.

5. **`pipeline.py`**
   * Expone `ejecutar_programa(texto_programa, instancia)`, conectando `lexico.py` → `automata_ap.py` → `simulador.py` y devolviendo un diccionario unificado con `categoria`, `detalle`, `registro` y `metricas`.

6. **`reportes.py`**
   * `guardar_registro_csv(...)`: genera un CSV con columnas `indice,orden,estado_ap,pila,posicion,carga`.
   * `guardar_registro_txt(...)`: genera un archivo de texto legible con el resultado, las grillas inicial y final, el resumen de métricas y la tabla de ejecución completa.

7. **`pruebas.py`**
   * Ejecuta `ejecutar_pruebas(instancia)` con los **11 casos exigidos** (8 pruebas mínimas + 3 casos de borde) y verifica automáticamente que el resultado obtenido coincida con el esperado (`PASS` / `FAIL`).

8. **`main.py`**
   * Punto de entrada por terminal. Permite correr toda la batería de pruebas + la solución del Grupo 06, o evaluar cualquier programa/instancia externos **sin editar el código del reconocedor**.

---

## 4. Requisitos e instalación (Anaconda / Python 3.12.3)

El proyecto requiere **Python 3.9 o superior** (probado en **Python 3.12.3**) y la librería **`automata-lib`**.

```bash
# 1. Crear el entorno en Conda con Python 3.12.3
conda create -n robot-ap python=3.12.3 pip -y

# 2. Activar el entorno
conda activate robot-ap

# 3. Instalar automata-lib
pip install automata-lib

# 4. Verificar la instalación
python --version
python -c "from automata.pda.dpda import DPDA; print('Todo OK!')"
```

---

## 5. Instrucciones para reproducir la ejecución

Ubicarse en la terminal dentro de la carpeta `robot_recolector/` con el entorno `robot-ap` activo:

### Modo 1: Ejecutar pruebas y generar los registros del Grupo 06
```bash
python main.py
```
**Qué hace:**
* Ejecuta las **11 pruebas** (solución correcta + errores del AP + errores físicos + objetivo no alcanzado + casos de borde) mostrando `[PASS]` o `[FAIL]` para cada una.
* Genera automáticamente en la carpeta actual:
  * `registro_grupo06.csv` (traza completa token por token en CSV).
  * `registro_grupo06.txt` (grillas inicial y final, métricas de la solución y tabla completa).

### Modo 2: Probar otro archivo de órdenes (sin editar el reconocedor)
```bash
python main.py ruta/a/mi_programa.txt
```
* Evalúa el archivo `.txt` usando la instancia del Grupo 06, imprime la categoría de resultado (`Error léxico`, `Rechazo del AP`, `Error físico`, `Objetivo no alcanzado` o `Misión resuelta`) y, si supera la fase del AP, guarda `registro_salida.csv` y `registro_salida.txt`.

### Modo 3: Probar otra instancia del depósito en formato JSON
```bash
python main.py ruta/a/mi_programa.txt ruta/a/otra_instancia.json
```
Formato esperado del archivo JSON:
```json
{
  "grupo": "Otra instancia",
  "filas": 6,
  "columnas": 6,
  "robot_inicial": [6, 1],
  "robot_final": [6, 1],
  "cajas": [[1, 1], [1, 5], [2, 3], [3, 6]],
  "obstaculos": [[2, 2], [2, 4], [3, 4], [5, 3]],
  "destinos": [[4, 1], [5, 1], [4, 5], [5, 5]]
}
```

---

## 6. Pruebas automatizadas incluidas (`pruebas.py`)

| # | Tipo | Descripción de la prueba | Resultado esperado |
| :-: | :--- | :--- | :--- |
| 1 | Mínima | Solución completa correcta (Grupo 06, 56 tokens) | `Misión resuelta` |
| 2 | Mínima | Regreso con orden que no corresponde al camino inverso | `Rechazo del AP` |
| 3 | Mínima | `soltar` antes de terminar el regreso | `Rechazo del AP` |
| 4 | Mínima | Viaje sin cierre `finviaje` | `Rechazo del AP` |
| 5 | Mínima | Segundo `agarrar` en el mismo viaje | `Rechazo del AP` |
| 6 | Mínima | Programa válido en AP que intenta atravesar un obstáculo `(5, 3)` | `Error físico` |
| 7 | Mínima | Programa válido en AP que intenta `agarrar` en celda vacía `(6, 1)` | `Error físico` |
| 8 | Mínima | Programa válido y físicamente ejecutable que no alcanza la meta | `Objetivo no alcanzado` |
| 9 | Borde | Token desconocido (`diagonal`) | `Error léxico` |
| 10 | Borde | Entrada vacía (`""`) | `Rechazo del AP` |
| 11 | Borde | Programa válido en AP que intenta salir de la grilla `(6, 0)` | `Error físico` |

---

## 7. Métricas de la solución del Grupo 06

Al ejecutar `python main.py`, la solución oficial del **Grupo 06 · Dos pedidos** arroja:
* **Resultado:** `Misión resuelta`
* **Total de tokens:** `56`
* **Movimientos sin carga:** `26` (`12` fuera de viajes + `14` de ida)
* **Movimientos con carga (regresos):** `14`
* **Total de desplazamientos:** `40`
* **Altura máxima de pila (sin contar `Z0`):** `4` (alcanzada en el Viaje 1 y en el Viaje 2)
