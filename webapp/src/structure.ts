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
 * Devuelve la estructura definida en `structure.json`.
 * Cambiando el contenido de dicho archivo pueden renderizarse
 * diferentes marcos sin modificar el código TypeScript.
 */
export function loadStructure(): FrameStructure {
  return structureData as FrameStructure;
}
