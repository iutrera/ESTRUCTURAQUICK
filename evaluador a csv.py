"""Evalúa nodos simbólicos y exporta sus coordenadas numéricas a CSV."""

import math
import pandas as pd

# ======================
# ENTRADAS POR DEFECTO
# ======================

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

def radians(x):
    """Convierte grados a radianes para usar en expresiones."""
    return math.radians(x)

def eval_expr(expr, context):
    """Evalúa una expresión con el contexto de variables indicado."""
    return eval(expr, {
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }, context)

def eval_infix(expr_str, vars_map):
    """Evalúa una cadena con variables ya sustituidas."""
    context = {
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }
    return eval(expr_str, context | vars_map)

# ======================
# ENTRADA DE USUARIO
# ======================

print("📥 Introduce valores (ENTER para usar por defecto):")
inputs = {}
for key, default in default_inputs.items():
    raw = input(f"{key} [{default}]: ").strip()
    try:
        inputs[key] = float(raw) if raw else default
    except:
        print("  → Valor inválido. Usando por defecto.")
        inputs[key] = default

# ======================
# EVALUACIÓN DE VARIABLES
# ======================

vars_map = inputs.copy()
pending = var_formulas.copy()
while pending:
    for k in list(pending):
        try:
            vars_map[k] = eval_expr(pending[k], vars_map)
            del pending[k]
        except:
            continue

# ✅ Agregar desplazamientos para cuadrantes
vars_map["X_OFFSET"] = vars_map["WIDTH_CELL"] * vars_map["NBR_CELL_WIDTH"]
vars_map["Y_OFFSET"] = vars_map["LENGTH_CELL"] * vars_map["NBR_CELL_LENGTH"]

# ======================
# EVALUACIÓN DE NODOS
# ======================

print("📄 Cargando nodos_esquinas_simbolico.csv...")
try:
    df = pd.read_csv("nodos_esquinas_simbolico.csv")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print(f"✅ {len(df)} nodos leídos. Evaluando...")

evaluated = []

def eval_node(n, x_expr, y_expr, z_expr):
    """Evalúa las expresiones de un nodo y devuelve sus coordenadas."""
    try:
        return {
            "N": n,
            "X": eval_infix(str(x_expr).upper(), vars_map),
            "Y": eval_infix(str(y_expr).upper(), vars_map),
            "Z": eval_infix(str(z_expr).upper(), vars_map)
        }
    except Exception as e:
        print(f"❌ Nodo {n}: Error → {e}")
        return {"N": n, "X": "ERR", "Y": "ERR", "Z": "ERR"}

for _, row in df.iterrows():
    nid = row["N"]
    x_expr = str(row["X"]).upper()
    y_expr = str(row["Y"]).upper()
    z_expr = str(row["Z"]).upper()

    if "+ X_OFFSET" in x_expr or "X_OFFSET" in x_expr:
        result = eval_node(nid, x_expr, y_expr, z_expr)
        evaluated.append(result)
    elif "+ Y_OFFSET" in y_expr or "Y_OFFSET" in y_expr:
        result = eval_node(nid, x_expr, y_expr, z_expr)
        evaluated.append(result)
    else:
        result = eval_node(nid, x_expr, y_expr, z_expr)
        evaluated.append(result)

# ======================
# EXPORTACIÓN
# ======================

pd.DataFrame(evaluated).to_csv("nodos_esquinas_evaluados.csv", index=False)
print("✅ Archivo generado: nodos_esquinas_evaluados.csv")
