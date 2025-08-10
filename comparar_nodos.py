"""Compara las coordenadas de nodos entre un Excel y el CSV generado."""

import csv
import zipfile
import xml.etree.ElementTree as ET

try:
    from tkinter import Tk, filedialog  # type: ignore
except Exception:  # pragma: no cover - Tk may not be available
    Tk = None
    filedialog = None


def read_export_nodes(xls_path):
    """Return dict {node: (x, y, z)} from sheet 'Export'."""
    ns = {
        'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }
    with zipfile.ZipFile(xls_path) as zf:
        wb_root = ET.fromstring(zf.read('xl/workbook.xml'))
        rId = None
        for sheet in wb_root.find('main:sheets', ns):
            if sheet.attrib.get('name') == 'Export':
                rId = sheet.attrib.get('{%s}id' % ns['r'])
                break
        if rId is None:
            raise ValueError("No se encontró la hoja 'Export'")

        rel_root = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        sheet_path = None
        for rel in rel_root:
            if rel.attrib.get('Id') == rId:
                sheet_path = 'xl/' + rel.attrib['Target']
                break
        if sheet_path is None:
            raise ValueError("No se encontró el archivo de la hoja 'Export'")

        # shared strings
        shared_strings = []
        try:
            sroot = ET.fromstring(zf.read('xl/sharedStrings.xml'))
            for si in sroot.findall('main:si', ns):
                text = ''.join(node.text or '' for node in si.iter() if node.text)
                shared_strings.append(text)
        except KeyError:
            pass

        sheet_root = ET.fromstring(zf.read(sheet_path))
        nodes = {}
        for row in sheet_root.findall('main:sheetData/main:row', ns):
            values = {}
            for c in row.findall('main:c', ns):
                ref = c.get('r')
                col = ''.join(filter(str.isalpha, ref))
                v_node = c.find('main:v', ns)
                if v_node is None:
                    continue
                val = v_node.text
                if c.get('t') == 's':
                    val = shared_strings[int(val)]
                values[col] = val
            if {'A', 'B', 'C', 'D'} <= values.keys():
                n = int(float(values['A']))
                x = float(values['B'])
                y = float(values['C'])
                z = float(values['D'])
                nodes[n] = (x, y, z)
        return nodes


def read_csv_nodes(csv_path='nodos_esquinas_evaluados.csv'):
    """Lee nodos desde el CSV evaluado y los devuelve como dict."""
    nodes = {}
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                n = int(row['N'])
                x = float(row['X'])
                y = float(row['Y'])
                z = float(row['Z'])
            except ValueError:
                # Ignorar filas que no tengan coordenadas válidas
                continue
            nodes[n] = (x, y, z)
    return nodes


def compare_nodes(excel_nodes, csv_nodes, tol=1e-6):
    """Compara coordenadas y devuelve diferencias mayores a `tol`."""
    diff = []
    for n, coords in excel_nodes.items():
        csv_coords = csv_nodes.get(n)
        if csv_coords is None:
            diff.append((n, coords, None))
            continue
        if any(abs(a - b) > tol for a, b in zip(coords, csv_coords)):
            diff.append((n, coords, csv_coords))
    return diff


def main():
    """Solicita el Excel y muestra las diferencias de nodos."""
    path = None
    if Tk and filedialog:
        try:
            root = Tk()
            root.withdraw()
            # Abrir diálogo gráfico para escoger el archivo
            path = filedialog.askopenfilename(title='Selecciona archivo Excel',
                                              filetypes=[('Excel files', '*.xlsx *.xlsm *.xls')])
            root.destroy()
        except Exception:
            path = None
    if not path:
        # Como alternativa, solicitar la ruta por consola
        path = input('Ruta del archivo Excel: ').strip()
    if not path:
        print('No se seleccionó ningún archivo.')
        return
    try:
        excel_nodes = read_export_nodes(path)
    except Exception as e:
        print('Error al leer hoja Export:', e)
        return
    # Cargar nodos evaluados y compararlos
    csv_nodes = read_csv_nodes()
    differences = compare_nodes(excel_nodes, csv_nodes)
    if not differences:
        print('Todos los nodos coinciden.')
    else:
        for n, exc, csvc in differences:
            if csvc is None:
                print(f'Nodo {n} no existe en nodos_esquinas_evaluados.csv (Export: {exc})')
            else:
                print(f'Nodo {n} distinto: Export {exc} vs CSV {csvc}')
        print(f'Total de diferencias: {len(differences)}')


if __name__ == '__main__':
    main()
