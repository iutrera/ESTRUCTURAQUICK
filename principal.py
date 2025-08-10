"""Visualiza nodos 3D evaluando fórmulas paramétricas del modelo."""

import math
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

default_inputs = {
    'LENGTH_CELL': 16.16,
    'WIDTH_CELL': 13.605,
    'LEVEL_FAN_DECK': 26.56,
    'FIRST_LEVEL': 8.85,
    'FAN_DIAMETER': 11.7,
    'NBR_CELL_LENGTH': 6,
    'NBR_CELL_WIDTH': 5,
    'ALFA': 60
}

var_formulas = {
    'Z0': '0.0',
    'Z5': '1.19',
    'Z6': '1.58',
    'Z11': '0.15',
    'X1': '-1.4',
    'X2': '0',
    'X5': '1.23',
    'Y1': '-1.6',
    'Y2': '-0.35',
    'Y3': '0',
    'Y5': '64.1',
    'M1': '1.7',
    'M2': '0.9',
    'M3': '0.4',
    'M4': '6.075',
    'M5': '0.9',
    'M6': '0.3',
    'F11': '0.315',
    'Z1': 'FIRST_LEVEL',
    'Z2': 'FIRST_LEVEL * 2',
    'Z4': 'LEVEL_FAN_DECK - 0.2',
    'Z3': 'Z4 + X1',
    'Z10': '(WIDTH_CELL / 2) / TAN(RADIANS(ALFA) / 2.0)',
    'Z8': 'Z5 + 2.2',
    'Z9': '(Z10 - Z11) / 2',
    'Z7': 'Z9 / 2.0',
    'X3': 'Z9 * TAN(RADIANS(ALFA / 2.0))',
    'X7': 'X3',
    'X4': '(WIDTH_CELL - X3 - X7 - X5) / 2.0',
    'X6': 'X4',
    'X9': 'X5',
    'X8': 'X7 - X9 / 2.0',
    'Y4': 'LENGTH_CELL',
    'R1': 'FAN_DIAMETER / 2.0',
    'F1': '(((LENGTH_CELL - WIDTH_CELL) / 2 + 2 * ((WIDTH_CELL / 2) - ((R1 + F11) / 1.414214))) / 3.0)',
    'F2': 'F1',
    'F3': 'F2',
    'F5': 'F1',
    'F6': 'F2',
    'F4': 'WIDTH_CELL / 2 - F1 - F2 - F3',
    'F7': 'F3',
    'F8': 'LENGTH_CELL / 2 - F5 - F6 - F7',
    'F9': '(LENGTH_CELL - FAN_DIAMETER) / 2 - F11',
    'F10': 'F1 + F2 + F3 - F12',
    'F12': '(WIDTH_CELL - FAN_DIAMETER) / 2 - F11',
    'F13': 'F1 + F2 + F3 - F9',
    'R2': 'R1 + F11',
    'R3': 'R2 + F3 / 1.41421'
}


def radians(x: float) -> float:
    """Convierte grados a radianes (wrapper de `math.radians`)."""
    return math.radians(x)

def eval_expr(expr: str, context: dict) -> float:
    """Evalúa una expresión usando sólo las funciones permitidas."""
    return eval(expr, {
        "math": math,
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }, context)

def eval_infix(expr_str: str, vars_map: dict) -> float:
    """Evalúa una cadena de texto con las variables ya sustituidas."""
    context = {
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }
    return eval(expr_str, context | vars_map)

def main() -> None:
    """Solicita datos, evalúa fórmulas y muestra una nube de puntos."""

    # --- Entrada de parámetros ---
    print("📥 1. Solicitando datos de entrada...")
    inputs = {}
    for key, default in default_inputs.items():
        raw = input(f"{key.replace('_', ' ')} [{default}]: ").strip()
        try:
            inputs[key] = float(raw) if raw else default
        except:
            # Capturamos errores de conversión para mantener el flujo
            print("  → Valor inválido. Usando por defecto.")
            inputs[key] = default

    # --- Cálculo de variables derivadas ---
    print("🧮 2. Calculando variables derivadas...")
    vars_map = inputs.copy()
    pending = var_formulas.copy()
    while pending:
        for name in list(pending):
            try:
                vars_map[name] = eval_expr(pending[name], vars_map)
                del pending[name]
            except:
                # Algunas expresiones dependen de otras aún no evaluadas
                continue
    print("✅ Variables calculadas.")

    # --- Lectura del CSV con fórmulas de nodos ---
    print("📄 3. Leyendo coin1.csv...")
    try:
        df = pd.read_csv("coin1.csv")
    except Exception as e:
        print(f"❌ Error leyendo coin1.csv: {e}")
        return
    print(f"✅ Leído {len(df)} nodos.")

    # --- Evaluación de cada expresión para obtener coordenadas ---
    print("🔍 4. Evaluando coordenadas...")
    xs, ys, zs, nodos_validos = [], [], [], []
    for _, row in df.iterrows():
        n = row["N"]
        try:
            x = eval_infix(str(row["X"]).upper(), vars_map)
            y = eval_infix(str(row["Y"]).upper(), vars_map)
            z = eval_infix(str(row["Z"]).upper(), vars_map)
            xs.append(x)
            ys.append(y)
            zs.append(z)
            nodos_validos.append(n)
        except Exception as e:
            print(f"❌ Nodo {n} → Error: {e}")

    print("📊 5. Mostrando gráfica 3D interactiva...")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(xs, ys, zs, picker=True)
    highlight, = ax.plot([], [], [], 'ro', markersize=8)  # punto resaltado
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("Nodos 3D")
    plt.tight_layout()

    coords = list(zip(xs, ys, zs))
    ids = nodos_validos
    annot = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, color="blue")

    def on_click(event):
        """Resalta el nodo más cercano a la posición del click."""
        if event.inaxes != ax:
            return

        min_dist = float("inf")
        nearest_index = None

        for i, (x, y, z) in enumerate(coords):
            if x is None or y is None or z is None:
                continue
            x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
            dx, dy = event.x - x2, event.y - y2
            dist = dx**2 + dy**2
            if dist < min_dist:
                min_dist = dist
                nearest_index = i

        if nearest_index is not None:
            node_id = ids[nearest_index]
            x, y, z = coords[nearest_index]
            annot.set_text(f"Nodo {node_id}\nX={x:.2f}, Y={y:.2f}, Z={z:.2f}")
            highlight.set_data([x], [y])
            highlight.set_3d_properties([z])
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
    print("✅ Visualización terminada.")

if __name__ == "__main__":
    main()
