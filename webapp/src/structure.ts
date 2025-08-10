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

/**
 * Devuelve una estructura de ejemplo con forma de cubo.
 * En una aplicación real, este método podría cargar datos externos.
 */
export function loadStructure(): FrameStructure {
  return {
    nodes: [
      [-1, -1, -1],
      [1, -1, -1],
      [1, 1, -1],
      [-1, 1, -1],
      [-1, -1, 1],
      [1, -1, 1],
      [1, 1, 1],
      [-1, 1, 1]
    ],
    edges: [
      [0, 1], [1, 2], [2, 3], [3, 0],
      [4, 5], [5, 6], [6, 7], [7, 4],
      [0, 4], [1, 5], [2, 6], [3, 7]
    ]
  };
}
