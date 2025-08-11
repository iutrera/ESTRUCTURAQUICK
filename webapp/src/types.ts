/**
 * Tipos comunes para describir una estructura formada por nodos y aristas.
 * Separarlos en un archivo independiente evita dependencias cíclicas entre
 * los módulos que construyen la geometría y los que la renderizan.
 */

/** Coordenada tridimensional de un nodo. */
export type Node = [number, number, number];

/** Arista que conecta dos nodos referenciados por su índice (basado en 0). */
export type Edge = [number, number];

/** Conjunto completo de nodos y aristas que definen una estructura. */
export interface FrameStructure {
  nodes: Node[];
  edges: Edge[];
}
