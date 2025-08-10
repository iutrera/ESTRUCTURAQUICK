"""Extrae información de vigas, grupos y cargas desde `Module1.bas`.

El archivo de entrada procede de SAP2000 y se analiza para generar archivos
CSV con las incidencias de las vigas, sus grupos, propiedades y las cargas
aplicadas.
"""

import re
import csv



def expand_tokens(tokens):
    """Expande secuencias con 'TO' en una lista de enteros."""
    numbers = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.upper() == "TO" and numbers:
            end = int(tokens[i + 1])
            start = numbers[-1] + 1
            numbers.extend(range(start, end + 1))
            i += 2
        else:
            numbers.append(int(tok))
            i += 1
    return numbers


def is_number(token: str) -> bool:
    """Devuelve True si el token puede interpretarse como número."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_load_tokens(tokens):
    """Intenta extraer IDs, dirección y valor de una secuencia de tokens.

    Se asume que los últimos tokens corresponden a la dirección (una o varias
    palabras) seguida por un único valor numérico.  Si no es posible interpretar
    la secuencia bajo estas reglas se devuelve ``None`` para indicar que se
    necesitan más tokens o que el formato no es compatible.
    """

    if len(tokens) < 3 or not is_number(tokens[-1]):
        return None

    value = tokens[-1]
    idx = len(tokens) - 2
    direction_tokens = []
    while idx >= 0 and not is_number(tokens[idx]) and tokens[idx].upper() != "TO":
        direction_tokens.insert(0, tokens[idx])
        idx -= 1

    if not direction_tokens:
        return None

    id_tokens = tokens[: idx + 1]
    if not id_tokens or any(
        not (t.isdigit() or t.upper() == "TO") for t in id_tokens
    ):
        return None

    ids = expand_tokens(id_tokens)
    direction = " ".join(direction_tokens)
    return ids, direction, value


# Cargar el contenido del archivo Module1.bas línea por línea
with open("Module1.bas", "r", encoding="latin-1") as f:
    lines = f.readlines()

# -----------------------------
# 1) MEMBER INCIDENCES
# -----------------------------

in_section = False
member_lines = []
for line in lines:
    upper = line.upper()
    if "MEMBER INCIDENCES" in upper:
        in_section = True
        continue
    if "START GROUP DEFINITION" in upper and in_section:
        break
    if in_section:
        member_lines.append(line)

if not member_lines:
    raise ValueError("No se encontró la sección 'MEMBER INCIDENCES' en Module1.bas")


member_text = " ".join(member_lines)
matches = re.findall(r"(\d+)\s+(\d+)\s+(\d+)", member_text)

# Conjuntos de nodos y barras de la malla base para filtrar las cargas
node_set = set()
member_set = set()
for mid, n1, n2 in matches:
    member_set.add(int(mid))
    node_set.add(int(n1))
    node_set.add(int(n2))

# -----------------------------
# 2) START GROUP DEFINITION → END GROUP DEFINITION
# -----------------------------
member_groups = {}
group_section = False
current_group = None
current_tokens = []

for line in lines:
    upper = line.upper()
    if "START GROUP DEFINITION" in upper:
        group_section = True
        continue
    if group_section:
        if "END GROUP DEFINITION" in upper:
            if current_group:
                nums = expand_tokens(current_tokens)
                for n in nums:
                    member_groups.setdefault(n, []).append(current_group)
            break
        content = line.split("\"", 1)[1].rsplit("\"", 1)[0]
        tokens = [t for t in content.split() if t != '-']
        if not tokens:
            continue
        if tokens[0] == "MEMBER":
            continue
        if tokens[0] == "JOINT":
            if current_group:
                nums = expand_tokens(current_tokens)
                for n in nums:
                    member_groups.setdefault(n, []).append(current_group)
            break
        if tokens[0].startswith('_'):
            if current_group:
                nums = expand_tokens(current_tokens)
                for n in nums:
                    member_groups.setdefault(n, []).append(current_group)
            current_group = tokens[0]
            current_tokens = tokens[1:]
        else:
            current_tokens.extend(tokens)

# -----------------------------
# 3) MEMBER PROPERTY EUROPEAN
# -----------------------------
member_props = {}
prop_section = False
current_tokens = []

for line in lines:
    upper = line.upper()
    if "MEMBER PROPERTY" in upper:
        prop_section = True
        continue
    if prop_section:
        if "MEMBER RELEASE" in upper:
            break
        content = line.split("\"", 1)[1].rsplit("\"", 1)[0]
        tokens = [t for t in content.split() if t != '-']
        if not tokens:
            continue
        tokens_upper = [t.upper() for t in tokens]
        if "TABLE" in tokens_upper:
            idx = tokens_upper.index("TABLE")
            number_tokens = current_tokens + tokens[:idx]
            prop_desc = " ".join(tokens[idx + 1:])
            numbers = expand_tokens(number_tokens)
            for n in numbers:
                member_props[n] = prop_desc
            current_tokens = []
        else:
            current_tokens.extend(tokens)

# -----------------------------
# 4) Cargas (JOINT/MEMBER)
# -----------------------------
load_entries = []
current_type = None
pending_tokens = []

for line in lines:
    upper = line.upper()

    if "JOINT LOAD" in upper:
        current_type = "JOINT"
        pending_tokens = []
        continue
    if "MEMBER LOAD" in upper:
        current_type = "MEMBER"
        pending_tokens = []
        continue
    if (
        "LOAD " in upper and "LOADTYPE" in upper
    ) or "TEMPERATURE LOAD" in upper or "SELFWEIGHT" in upper:
        current_type = None
        pending_tokens = []
        continue

    if current_type:
        try:
            content = line.split("\"", 1)[1].rsplit("\"", 1)[0]
        except IndexError:
            continue
        if not content.strip() or content.lstrip().startswith("*"):
            continue
        tokens = [t for t in content.split() if t != '-']
        pending_tokens.extend(tokens)
        parsed = parse_load_tokens(pending_tokens)
        if parsed:
            ids, direction, value = parsed
            if current_type == "JOINT":
                for nid in ids:
                    if nid in node_set:
                        load_entries.append(
                            ["JOINT", direction, value, nid, ""]
                        )
            else:
                for mid in ids:
                    if mid in member_set:
                        load_entries.append(
                            ["MEMBER", direction, value, "", mid]
                        )
            pending_tokens = []

# -----------------------------
# 5) Guardar resultados en CSV
# -----------------------------
with open("member_connections.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["member_id", "start_node", "end_node", "group", "type"])
    for member_id, start_node, end_node in matches:
        mid = int(member_id)
        group = " ".join(member_groups.get(mid, []))
        beam_type = member_props.get(mid, "")
        writer.writerow([mid, int(start_node), int(end_node), group, beam_type])

with open("cargas.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Type", "Direction", "Value", "BaseNode", "BaseMember"])
    for t, d, v, n, m in load_entries:
        writer.writerow([t, d, v, n, m])

print("Archivos CSV generados: member_connections.csv, cargas.csv")
