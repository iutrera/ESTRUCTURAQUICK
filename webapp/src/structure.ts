/**
 * Tipos y utilidades para describir una estructura en nodos y aristas.
 * Esta capa permite separar los datos del código de renderizado.
 */

/** Coordenada tridimensional de un nodo. */
export type Node = [number, number, number];

/** Arista que conecta dos nodos referenciados por su índice. */
export type Edge = [number, number];

/**
 * Conjunto completo de nodos y aristas que definen una estructura.
 */
export interface FrameStructure {
  nodes: Node[];
  edges: Edge[];
}

/** Datos de la estructura cargados desde un archivo JSON. */
import structureData from './structure.json';

/**
 * Resultados del análisis geométrico de una estructura.
 * Incluye el centro del conjunto de nodos y un radio que abarque toda
 * la estructura para facilitar el encuadre de la cámara.
 */
export interface StructureBounds {
  center: Node;
  radius: number;
}

/**
 * Devuelve la estructura definida en `structure.json`.
 * Cambiando el contenido de dicho archivo pueden renderizarse
 * diferentes marcos sin modificar el código TypeScript.
 */
export function loadStructure(): FrameStructure {
  return structureData as FrameStructure;
}

/**
 * Calcula el centroide y el radio que engloba todos los nodos de la
 * estructura proporcionada. El radio corresponde a la distancia máxima
 * desde el centro a cualquiera de los nodos.
 */
export function computeBounds(structure: FrameStructure): StructureBounds {
  let min: Node = [Infinity, Infinity, Infinity];
  let max: Node = [-Infinity, -Infinity, -Infinity];

  for (const [x, y, z] of structure.nodes) {
    if (x < min[0]) min[0] = x;
    if (y < min[1]) min[1] = y;
    if (z < min[2]) min[2] = z;
    if (x > max[0]) max[0] = x;
    if (y > max[1]) max[1] = y;
    if (z > max[2]) max[2] = z;
  }

  const center: Node = [
    (min[0] + max[0]) / 2,
    (min[1] + max[1]) / 2,
    (min[2] + max[2]) / 2,
  ];

  let radius = 0;
  for (const [x, y, z] of structure.nodes) {
    const dx = x - center[0];
    const dy = y - center[1];
    const dz = z - center[2];
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
    if (dist > radius) radius = dist;
  }

  return { center, radius };
}
