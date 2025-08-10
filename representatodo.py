"""Evalúa nodos, repite geometría y muestra un visor 3D interactivo."""

import math
import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from matplotlib.widgets import CheckButtons, Button




# ------------------------
# Valores por defecto de entrada
# ------------------------
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

# ------------------------
# Formulaciones simbólicas que se evaluarán
# ------------------------
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

# ------------------------
# Funciones auxiliares
# ------------------------
def radians(x):
    """Convierte grados a radianes para su uso en las fórmulas."""
    return math.radians(x)

def eval_expr(expr, context):
    """Evalúa una expresión con funciones matemáticas seguras."""
    return eval(expr, {
        "math": math,
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }, context)

def eval_infix(expr_str, vars_map):
    """Evalúa una cadena con variables reemplazadas."""
    context = {
        "COS": math.cos,
        "SIN": math.sin,
        "TAN": math.tan,
        "PI": math.pi,
        "RADIANS": radians
    }
    return eval(expr_str, context | vars_map)



def translational_repeat(coords_map, beams, groups, axis, spacing, times, offset_tracker=None):
    """Replica nodos y vigas en una dirección dada.

    Si se proporciona ``offset_tracker`` se almacenarán en él los offsets de
    nodos y elementos generados por una sola repetición.  Esto es útil para
    posteriormente replicar las cargas con el mismo desplazamiento de IDs.
    """

    group_set = {g.upper() for g in groups}
    to_copy = [b for b in beams if group_set & {g.upper() for g in b.get("group", "").split()}]
    if not to_copy:
        return 0, 0

    max_node = max(coords_map.keys(), default=0)
    max_member = max((b.get("id", 0) for b in beams), default=0)
    coord_index = {
        (round(x, 3), round(y, 3), round(z, 3)): nid
        for nid, (x, y, z) in coords_map.items()
    }
    beam_index = {(b["start_node"], b["end_node"]) for b in beams}

    before_node = max_node
    before_member = max_member
    dup_nodes = 0
    dup_beams = 0

    for i in range(1, times + 1):
        offset = [0.0, 0.0, 0.0]
        offset[axis] = spacing * i
        node_map = {}
        for b in to_copy:
            n1, n2 = b["start_node"], b["end_node"]
            for n in (n1, n2):
                if n not in node_map:
                    x, y, z = coords_map[n]
                    nx = x + offset[0]
                    ny = y + offset[1]
                    nz = z + offset[2]
                    key = (round(nx, 3), round(ny, 3), round(nz, 3))
                    if key in coord_index:
                        node_map[n] = coord_index[key]
                        dup_nodes += 1
                    else:
                        max_node += 1
                        coords_map[max_node] = (nx, ny, nz)
                        coord_index[key] = max_node
                        node_map[n] = max_node
            start_id = node_map[n1]
            end_id = node_map[n2]
            beam_key = (start_id, end_id)
            if beam_key not in beam_index:
                beam_index.add(beam_key)
                max_member += 1
                new_beam = b.copy()
                new_beam["start_node"] = start_id
                new_beam["end_node"] = end_id
                new_beam["id"] = max_member
                beams.append(new_beam)
            else:
                dup_beams += 1

    if offset_tracker is not None and times > 0:
        offset_tracker["node"] = (max_node - before_node) // times
        offset_tracker["member"] = (max_member - before_member) // times

    return dup_nodes, dup_beams

def apply_translational_repeats(coords_map, beams, inputs):
    """Aplica las repeticiones definidas en Module2."""
    len_reps = int(inputs["NBR_CELL_LENGTH"]) - 2
    wid_reps = int(inputs["NBR_CELL_WIDTH"]) - 2

    translational_repeat(
        coords_map, beams, {"_EXTERNAL-LL"}, 1, inputs["LENGTH_CELL"], len_reps
    )
    translational_repeat(
        coords_map,
        beams,
        {"_EXTERNAL-W1", "_EXTERNAL-W2"},
        0,
        inputs["WIDTH_CELL"],
        wid_reps,
    )
    translational_repeat(
        coords_map, beams, {"_EXTERNAL-LR"}, 1, inputs["LENGTH_CELL"], len_reps
    )
    translational_repeat(
        coords_map, beams, {"_WINDWALL1"}, 0, -inputs["WIDTH_CELL"], wid_reps
    )
    translational_repeat(
        coords_map, beams, {"_WINDWALL2"}, 0, inputs["WIDTH_CELL"], wid_reps
    )


def apply_loads(load_rows, node_off_len, node_off_wid, mem_off_len, mem_off_wid, rep_len, rep_wid):
    """Genera las líneas de carga replicadas según los offsets calculados."""
    lines = []
    for row in load_rows:
        t = row.get("Type", "").upper()
        direction = row.get("Direction", "")
        try:
            value = float(row.get("Value", 0))
        except Exception:
            value = 0.0
        base_node = row.get("BaseNode")
        base_member = row.get("BaseMember")
        base_node = int(base_node) if base_node else None
        base_member = int(base_member) if base_member else None
        for i in range(rep_len + 1):
            for j in range(rep_wid + 1):
                if t == "JOINT" and base_node is not None:
                    nid = base_node + i * node_off_len + j * node_off_wid
                    lines.append(f"JOINT LOAD {nid} {direction} {value}")
                elif t == "MEMBER" and base_member is not None:
                    mid = base_member + i * mem_off_len + j * mem_off_wid
                    lines.append(f"MEMBER LOAD {mid} {direction} {value}")
    return lines


def export_sap2000(filename, coords_map, beams, load_lines):
    """Exporta un fichero de texto con nodos, vigas, tipos de vigas y cargas."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("JOINT COORDINATES\n")
        for nid, (x, y, z) in sorted(coords_map.items()):
            f.write(f" {nid} {x:.3f} {y:.3f} {z:.3f}\n")
        f.write("MEMBER INCIDENCES\n")
        for b in beams:
            f.write(f" {b['id']} {b['start_node']} {b['end_node']}\n")
        f.write("MEMBER TYPES\n")
        for b in beams:
            f.write(f" {b['id']} {b.get('type', '?')}\n")
        if load_lines:
            f.write("LOADS\n")
            for line in load_lines:
                f.write(line + "\n")


# ------------------------
# Función principal
# ------------------------
def main():
    """Punto de entrada para generar la estructura completa y visualizarla."""
    # --- Entrada de datos del usuario ---
    print("📥 1. Solicitando datos de entrada...")
    inputs = {}
    for key, default in default_inputs.items():
        raw = input(f"{key.replace('_', ' ')} [{default}]: ").strip()
        try:
            inputs[key] = float(raw) if raw else default
        except:
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
                continue
    print("✅ Variables calculadas.")


    # --- Lectura de nodos simbólicos ---
    print("📄 3. Leyendo nodos desde CSV...")
    try:
        with open("nodos_esquinas_simbolico.csv", newline="") as f:
            nodes = list(csv.DictReader(f))
    except Exception as e:
        print(f"❌ Error leyendo nodos: {e}")
        return
    print(f"✅ Leído {len(nodes)} nodos.")

    print("📄 4. Leyendo vigas desde member_connections.csv...")
    try:
        with open("member_connections.csv", newline="") as f:
            beam_rows = list(csv.DictReader(f))
    except Exception as e:
        print(f"❌ Error leyendo vigas: {e}")
        beam_rows = None
    # Mantener compatibilidad con versiones antiguas que usaban 'df_beams'
    df_beams = beam_rows

    print("🔍 5. Evaluando coordenadas...")
    coords_map = {}
    for row in nodes:
        n = int(row["N"])
        try:
            x = eval_infix(str(row["X"]).upper(), vars_map)
            y = eval_infix(str(row["Y"]).upper(), vars_map)
            z = eval_infix(str(row["Z"]).upper(), vars_map)
            coords_map[n] = (x, y, z)
        except Exception as e:
            print(f"❌ Nodo {n} → Error: {e}")

    # Construir lista inicial de vigas
    beams_raw = []

    if beam_rows:
        for row in beam_rows:
            try:
                n1, n2 = int(row["start_node"]), int(row["end_node"])
                mid = int(row.get("member_id", 0))
            except Exception:
                continue
            beam_type = row.get("type", "?")
            group = row.get("group", "")
            if n1 in coords_map and n2 in coords_map:
                beams_raw.append({
                    "id": mid,
                    "start_node": n1,
                    "end_node": n2,
                    "type": beam_type,
                    "group": group,
                })

    print("📄 4b. Leyendo cargas desde cargas.csv...")
    try:
        with open("cargas.csv", newline="") as f:
            load_rows = list(csv.DictReader(f))
    except Exception as e:
        print(f"❌ Error leyendo cargas: {e}")
        load_rows = []

    len_reps = int(inputs["NBR_CELL_LENGTH"]) - 2
    wid_reps = int(inputs["NBR_CELL_WIDTH"]) - 2

    # Lista de repeticiones a aplicar paso a paso
    len_tracker = {}
    wid_tracker = {}
    repeat_ops = [
        lambda: translational_repeat(
            coords_map,
            beams_raw,
            {"_EXTERNAL-LL"},
            1,
            inputs["LENGTH_CELL"],
            len_reps,
            len_tracker if not len_tracker else None,
        ),
        lambda: translational_repeat(
            coords_map,
            beams_raw,
            {"_EXTERNAL-W1", "_EXTERNAL-W2"},
            0,
            inputs["WIDTH_CELL"],
            wid_reps,
            wid_tracker if not wid_tracker else None,
        ),
        lambda: translational_repeat(
            coords_map,
            beams_raw,
            {"_EXTERNAL-LR"},
            1,
            inputs["LENGTH_CELL"],
            len_reps,
        ),
        lambda: translational_repeat(
            coords_map,
            beams_raw,
            {"_WINDWALL1"},
            0,
            -inputs["WIDTH_CELL"],
            wid_reps,
        ),
        lambda: translational_repeat(
            coords_map,
            beams_raw,
            {"_WINDWALL2"},
            0,
            inputs["WIDTH_CELL"],
            wid_reps,
        ),
    ]

    dup_nodes_total = 0
    dup_beams_total = 0
    for op in repeat_ops:
        dn, db = op()
        dup_nodes_total += dn
        dup_beams_total += db

    node_off_len = len_tracker.get("node", 0)
    node_off_wid = wid_tracker.get("node", 0)
    mem_off_len = len_tracker.get("member", 0)
    mem_off_wid = wid_tracker.get("member", 0)

    load_lines = apply_loads(
        load_rows,
        node_off_len,
        node_off_wid,
        mem_off_len,
        mem_off_wid,
        len_reps,
        wid_reps,
    )

    print(f"♻️ Eliminados {dup_nodes_total} nodos duplicados y {dup_beams_total} miembros duplicados.")

    xs, ys, zs, nodos_validos = [], [], [], []
    for nid, (x, y, z) in coords_map.items():
        xs.append(x)
        ys.append(y)
        zs.append(z)
        nodos_validos.append(nid)

    print("📊 6. Mostrando gráfica 3D interactiva...")


    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # maximize figure to take full screen when possible
    try:
        plt.get_current_fig_manager().window.state('zoomed')
    except Exception:
        try:
            plt.get_current_fig_manager().window.showMaximized()
        except Exception:
            try:
                plt.get_current_fig_manager().full_screen_toggle()
            except Exception:
                pass
    sc = ax.scatter(xs, ys, zs, picker=True)
    highlight_node, = ax.plot([], [], [], 'ro', markersize=8)
    highlight_beam, = ax.plot([], [], [], color='red', linewidth=3)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("Nodos y vigas")
    plt.tight_layout()


    from itertools import cycle
    color_cycle = cycle(plt.cm.tab20.colors)
    beams = []
    group_lines = {}
    group_colors = {}
    group_visibility = {}

    coords = list(zip(xs, ys, zs))
    ids = nodos_validos
    annot = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, color="blue")

    def refresh_plot():
        xs_local, ys_local, zs_local, nodos_local = [], [], [], []
        for nid, (x, y, z) in coords_map.items():
            xs_local.append(x)
            ys_local.append(y)
            zs_local.append(z)
            nodos_local.append(nid)
        coords[:] = list(zip(xs_local, ys_local, zs_local))
        ids[:] = nodos_local
        sc._offsets3d = (xs_local, ys_local, zs_local)
        for lines in group_lines.values():
            for line in lines:
                line.remove()
        group_lines.clear()
        beams.clear()
        for b in beams_raw:
            n1, n2 = b["start_node"], b["end_node"]
            x1, y1, z1 = coords_map[n1]
            x2, y2, z2 = coords_map[n2]
            grp = b.get("group", "?")
            if grp not in group_colors:
                group_colors[grp] = next(color_cycle)
            line, = ax.plot([x1, x2], [y1, y2], [z1, z2], color=group_colors[grp], linewidth=1)
            line.set_visible(group_visibility.get(grp, True))
            group_lines.setdefault(grp, []).append(line)

            beams.append({
                **b,
                "coords": (x1, y1, z1, x2, y2, z2),
                "line": line,
            })

        fig.canvas.draw_idle()

    refresh_plot()

    if group_lines:
        plt.subplots_adjust(left=0.25)
        rax = plt.axes([0.02, 0.4, 0.18, 0.5])
        labels = list(group_lines.keys())
        visibility = [group_visibility.get(g, True) for g in labels]

        checks = CheckButtons(rax, labels, visibility)
        for lbl, g in zip(checks.labels, labels):
            lbl.set_color(group_colors[g])

        def toggle_group(label):

            group_visibility[label] = not group_visibility.get(label, True)

            for line in group_lines[label]:
                line.set_visible(group_visibility[label])
            fig.canvas.draw_idle()


        checks.on_clicked(toggle_group)



    export_ax = plt.axes([0.8, 0.02, 0.15, 0.06])
    export_btn = Button(export_ax, "Exportar")

    def on_export(event):
        try:
            from tkinter import Tk
            from tkinter.filedialog import asksaveasfilename
            root = Tk()
            root.withdraw()
            fname = asksaveasfilename(
                defaultextension=".s2k",
                filetypes=[("SAP2000", "*.s2k"), ("Todos", "*.*")],
                title="Guardar como"
            )
            root.destroy()
        except Exception:
            fname = "estructura.s2k"
        if fname:
            export_sap2000(fname, coords_map, beams_raw, load_lines)
            print(f"📤 Fichero SAP2000 generado: {fname}")

    export_btn.on_clicked(on_export)


    def distance_to_segment(px, py, x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return (px - x1) ** 2 + (py - y1) ** 2
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        nx, ny = x1 + t * dx, y1 + t * dy
        return (px - nx) ** 2 + (py - ny) ** 2


    def on_click(event):
        if event.inaxes != ax:
            return

        # distancia a nodos
        min_dist_node = float("inf")
        nearest_node_index = None
        for i, (x, y, z) in enumerate(coords):
            x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
            x_disp, y_disp = ax.transData.transform((x2, y2))
            dist = (event.x - x_disp) ** 2 + (event.y - y_disp) ** 2
            if dist < min_dist_node:
                min_dist_node = dist
                nearest_node_index = i

        # distancia a vigas
        min_dist_beam = float("inf")
        nearest_beam = None
        for beam in beams:
            if not beam["line"].get_visible():
                continue
            x1, y1, z1, x2, y2, z2 = beam["coords"]
            a1, b1, _ = proj3d.proj_transform(x1, y1, z1, ax.get_proj())
            a2, b2, _ = proj3d.proj_transform(x2, y2, z2, ax.get_proj())
            a1, b1 = ax.transData.transform((a1, b1))
            a2, b2 = ax.transData.transform((a2, b2))
            dist = distance_to_segment(event.x, event.y, a1, b1, a2, b2)
            if dist < min_dist_beam:
                min_dist_beam = dist
                nearest_beam = beam

        # comparar cual esta mas cerca
        if min_dist_node <= min_dist_beam:
            if nearest_node_index is not None:
                node_id = ids[nearest_node_index]
                x, y, z = coords[nearest_node_index]
                annot.set_text(f"Nodo {node_id}\nX={x:.2f}, Y={y:.2f}, Z={z:.2f}")
                highlight_node.set_data([x], [y])
                highlight_node.set_3d_properties([z])
                highlight_beam.set_data([], [])
                highlight_beam.set_3d_properties([])
        else:
            highlight_node.set_data([], [])
            highlight_node.set_3d_properties([])
            if nearest_beam is not None:
                x1, y1, z1, x2, y2, z2 = nearest_beam["coords"]
                annot.set_text(
                    f"Elemento {nearest_beam['start_node']} - {nearest_beam['end_node']}\n"
                    f"Tipo: {nearest_beam['type']}\nGrupo: {nearest_beam.get('group', '?')}"
                )
                highlight_beam.set_data([x1, x2], [y1, y2])
                highlight_beam.set_3d_properties([z1, z2])
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('button_press_event', on_click)


    plt.show()
    print("✅ Visualización terminada.")


# ------------------------
# Ejecución
# ------------------------
if __name__ == "__main__":
    main()
