/**
 * Conjunto de utilidades de álgebra lineal para operar con matrices 4x4.
 * Estas funciones se diseñan específicamente para transformaciones usadas
 * en gráficos 3D dentro del motor WebGL.
 */

/**
 * Crea una matriz de proyección en perspectiva.
 *
 * @param fovy   Ángulo vertical de visión en radianes.
 * @param aspect Relación de aspecto (ancho/alto).
 * @param near   Distancia al plano cercano de recorte.
 * @param far    Distancia al plano lejano de recorte.
 * @returns Matriz de proyección 4x4 como Float32Array.
 */
export function perspectiva(
  fovy: number,
  aspect: number,
  near: number,
  far: number
): Float32Array {
  const f = 1.0 / Math.tan(fovy / 2);
  const nf = 1 / (near - far);
  const out = new Float32Array(16);
  out[0] = f / aspect;
  out[5] = f;
  out[10] = (far + near) * nf;
  out[11] = -1;
  out[14] = (2 * far * near) * nf;
  return out;
}

/**
 * Crea una matriz de proyección ortográfica.
 *
 * @param left   Coordenada del plano izquierdo de recorte.
 * @param right  Coordenada del plano derecho de recorte.
 * @param bottom Coordenada del plano inferior de recorte.
 * @param top    Coordenada del plano superior de recorte.
 * @param near   Distancia al plano cercano de recorte.
 * @param far    Distancia al plano lejano de recorte.
 * @returns Matriz de proyección 4x4 como Float32Array.
 */
export function ortografica(
  left: number,
  right: number,
  bottom: number,
  top: number,
  near: number,
  far: number
): Float32Array {
  const lr = 1 / (left - right);
  const bt = 1 / (bottom - top);
  const nf = 1 / (near - far);
  const out = new Float32Array(16);
  out[0] = -2 * lr;
  out[5] = -2 * bt;
  out[10] = 2 * nf;
  out[12] = (left + right) * lr;
  out[13] = (top + bottom) * bt;
  out[14] = (far + near) * nf;
  out[15] = 1;
  return out;
}

/**
 * Devuelve una matriz identidad 4x4.
 */
export function identidad(): Float32Array {
  const out = new Float32Array(16);
  out[0] = out[5] = out[10] = out[15] = 1;
  return out;
}

/**
 * Multiplica dos matrices 4x4.
 *
 * @param a Primera matriz.
 * @param b Segunda matriz.
 * @returns Producto de `a` por `b`.
 */
export function multiplica(a: Float32Array, b: Float32Array): Float32Array {
  const out = new Float32Array(16);
  for (let i = 0; i < 4; i++) {
    const ai0 = a[i], ai1 = a[i + 4], ai2 = a[i + 8], ai3 = a[i + 12];
    out[i]      = ai0 * b[0] + ai1 * b[1] + ai2 * b[2] + ai3 * b[3];
    out[i + 4]  = ai0 * b[4] + ai1 * b[5] + ai2 * b[6] + ai3 * b[7];
    out[i + 8]  = ai0 * b[8] + ai1 * b[9] + ai2 * b[10] + ai3 * b[11];
    out[i + 12] = ai0 * b[12] + ai1 * b[13] + ai2 * b[14] + ai3 * b[15];
  }
  return out;
}

/**
 * Aplica una traslación a la matriz dada.
 *
 * @param m Matriz original.
 * @param v Vector de traslación `[x, y, z]`.
 * @returns Nueva matriz resultante de la traslación.
 */
export function traslada(
  m: Float32Array,
  v: [number, number, number]
): Float32Array {
  const out = m.slice(0);
  out[12] = m[0] * v[0] + m[4] * v[1] + m[8]  * v[2] + m[12];
  out[13] = m[1] * v[0] + m[5] * v[1] + m[9]  * v[2] + m[13];
  out[14] = m[2] * v[0] + m[6] * v[1] + m[10] * v[2] + m[14];
  out[15] = m[3] * v[0] + m[7] * v[1] + m[11] * v[2] + m[15];
  return out;
}

/**
 * Rota una matriz alrededor del eje X.
 *
 * @param m   Matriz a rotar.
 * @param rad Ángulo de rotación en radianes.
 * @returns Matriz rotada.
 */
export function rotaX(m: Float32Array, rad: number): Float32Array {
  const s = Math.sin(rad), c = Math.cos(rad);
  const out = m.slice(0);
  out[4] = m[4] * c + m[8] * s;
  out[5] = m[5] * c + m[9] * s;
  out[6] = m[6] * c + m[10] * s;
  out[7] = m[7] * c + m[11] * s;
  out[8] = m[8] * c - m[4] * s;
  out[9] = m[9] * c - m[5] * s;
  out[10] = m[10] * c - m[6] * s;
  out[11] = m[11] * c - m[7] * s;
  return out;
}

/**
 * Rota una matriz alrededor del eje Y.
 *
 * @param m   Matriz a rotar.
 * @param rad Ángulo de rotación en radianes.
 * @returns Matriz rotada.
 */
export function rotaY(m: Float32Array, rad: number): Float32Array {
  const s = Math.sin(rad), c = Math.cos(rad);
  const out = m.slice(0);
  out[0] = m[0] * c - m[8] * s;
  out[1] = m[1] * c - m[9] * s;
  out[2] = m[2] * c - m[10] * s;
  out[3] = m[3] * c - m[11] * s;
  out[8] = m[0] * s + m[8] * c;
  out[9] = m[1] * s + m[9] * c;
  out[10] = m[2] * s + m[10] * c;
  out[11] = m[3] * s + m[11] * c;
  return out;
}
