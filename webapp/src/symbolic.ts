import { FrameStructure, Node, Edge } from './types';

/** Entradas por defecto equivalentes a las del script Python. */
export const defaultInputs: Record<string, number> = {
  LENGTH_CELL: 2,
  WIDTH_CELL: 2,
};

/**
 * Evalúa una expresión aritmética utilizando las variables disponibles.
 * Se usa `Function` para generar una función segura sin exponer el ámbito global.
 */
function evalExpr(expr: string, vars: Record<string, number>): number {
  const args = Object.keys(vars);
  const vals = Object.values(vars);
  // eslint-disable-next-line no-new-func
  const fn = new Function(...args, `return ${expr};`);
  return fn(...vals);
}

/**
 * Parsea un CSV simple a una lista de registros clave→valor.
 * Se asume que los campos están separados por comas sin comillas.
 */
function parseCsv(text: string): Record<string, string>[] {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(',');
  return lines.slice(1).map(line => {
    const cols = line.split(',');
    const row: Record<string, string> = {};
    headers.forEach((h, i) => (row[h] = cols[i] ?? ''));
    return row;
  });
}

/**
 * Construye la estructura interpretando dos CSV con nodos y conexiones.
 * Las coordenadas admiten expresiones que se evaluarán con las variables
 * definidas en `inputs`.
 */
export function buildStructure(
  nodesCsv: string,
  beamsCsv: string,
  inputs: Record<string, number> = defaultInputs,
): FrameStructure {
  const vars = { ...inputs };

  const nodeRows = parseCsv(nodesCsv);
  const nodes: Node[] = nodeRows.map(row => [
    evalExpr(row.X, vars),
    evalExpr(row.Y, vars),
    evalExpr(row.Z, vars),
  ]);

  const beamRows = parseCsv(beamsCsv);
  const edges: Edge[] = beamRows.map(row => [
    parseInt(row.start_node, 10) - 1,
    parseInt(row.end_node, 10) - 1,
  ]);

  return { nodes, edges };
}
