
/**
 * Punto de entrada de la aplicación web. Utiliza WebGL puro para renderizar
 * un marco estructural cúbico interactivo sin depender de bibliotecas
 * externas. La estructura puede rotarse y hacer zoom con el ratón, sirviendo
 * como demostración de visualización 3D de alto rendimiento.
 */
import { greetFromWasm, addFromWasm } from './wasm';


/** Compila un shader de WebGL a partir de su código fuente. */
function compileShader(
  gl: WebGLRenderingContext,
  type: number,
  source: string
): WebGLShader {
  const shader = gl.createShader(type);
  if (!shader) throw new Error('No se pudo crear el shader');
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const info = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(`Falló la compilación del shader: ${info}`);
  }
  return shader;
}

/** Enlaza un programa WebGL a partir de shaders de vértice y fragmento. */
function createProgram(
  gl: WebGLRenderingContext,
  vsSource: string,
  fsSource: string
): WebGLProgram {
  const vs = compileShader(gl, gl.VERTEX_SHADER, vsSource);
  const fs = compileShader(gl, gl.FRAGMENT_SHADER, fsSource);
  const program = gl.createProgram();
  if (!program) throw new Error('No se pudo crear el programa');
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const info = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(`Falló el enlace del programa: ${info}`);
  }
  return program;
}

function init(): void {
  const canvas = document.createElement('canvas');
  document.body.appendChild(canvas);
  const gl = canvas.getContext('webgl') as WebGLRenderingContext;
  if (!gl) {
    throw new Error('WebGL no soportado');
  }

  // Ajusta el tamaño del lienzo al de la ventana.
  function resize(): void {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  window.addEventListener('resize', resize);
  resize();

  // Shaders para colorear cada vértice del cubo.
  const program = createProgram(
    gl,
    `
    attribute vec3 position;

    uniform mat4 mvp;
    void main() {

      gl_Position = mvp * vec4(position, 1.0);
    }
    `,
    `
    precision mediump float;

    uniform vec3 uColor;
    void main() {
      gl_FragColor = vec4(uColor, 1.0);

    }
    `
  );
  gl.useProgram(program);


  // Structural nodes and edges forming a cube frame.
  const nodes = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
  ];
  const edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
  ];

  const vertices = new Float32Array(nodes.flat());
  const indices = new Uint16Array(edges.flat());


  const vertexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

  const indexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);

  const posLoc = gl.getAttribLocation(program, 'position');

  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);

  const colorLoc = gl.getUniformLocation(program, 'uColor');
  gl.uniform3f(colorLoc, 0.1, 0.4, 0.8);


  const mvpLoc = gl.getUniformLocation(program, 'mvp');
  gl.enable(gl.DEPTH_TEST);

  // Estado para la interacción.
  let rotX = 0;
  let rotY = 0;
  let distancia = 5;
  let arrastrando = false;
  const ultimo = { x: 0, y: 0 };

  canvas.addEventListener('mousedown', (e: MouseEvent) => {
    arrastrando = true;
    ultimo.x = e.clientX;
    ultimo.y = e.clientY;
  });
  window.addEventListener('mouseup', () => {
    arrastrando = false;
  });
  canvas.addEventListener('mousemove', (e: MouseEvent) => {
    if (!arrastrando) return;
    const dx = e.clientX - ultimo.x;
    const dy = e.clientY - ultimo.y;
    rotY += dx * 0.01;
    rotX += dy * 0.01;
    ultimo.x = e.clientX;
    ultimo.y = e.clientY;
  });
  canvas.addEventListener('wheel', (e: WheelEvent) => {
    e.preventDefault();
    distancia += e.deltaY * 0.01;
  });

  // Utilidades de matrices 4x4.
  function perspectiva(fovy: number, aspect: number, near: number, far: number): Float32Array {
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

  function identidad(): Float32Array {
    const out = new Float32Array(16);
    out[0] = out[5] = out[10] = out[15] = 1;
    return out;
  }

  function multiplica(a: Float32Array, b: Float32Array): Float32Array {
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

  function traslada(m: Float32Array, v: [number, number, number]): Float32Array {
    const out = m.slice(0);
    out[12] = m[0] * v[0] + m[4] * v[1] + m[8]  * v[2] + m[12];
    out[13] = m[1] * v[0] + m[5] * v[1] + m[9]  * v[2] + m[13];
    out[14] = m[2] * v[0] + m[6] * v[1] + m[10] * v[2] + m[14];
    out[15] = m[3] * v[0] + m[7] * v[1] + m[11] * v[2] + m[15];
    return out;
  }

  function rotaX(m: Float32Array, rad: number): Float32Array {
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

  function rotaY(m: Float32Array, rad: number): Float32Array {
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

  // Bucle de renderizado.
  function render(): void {
    gl.clearColor(0.95, 0.95, 0.95, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const proy = perspectiva(Math.PI / 4, canvas.width / canvas.height, 0.1, 100);
    let modelo = identidad();
    modelo = rotaX(modelo, rotX);
    modelo = rotaY(modelo, rotY);
    let vista = identidad();
    vista = traslada(vista, [0, 0, -distancia]);
    const mvp = multiplica(proy, multiplica(vista, modelo));

    gl.uniformMatrix4fv(mvpLoc, false, mvp);

    gl.drawElements(gl.LINES, indices.length, gl.UNSIGNED_SHORT, 0);


    requestAnimationFrame(render);
  }

  greetFromWasm('ingeniero').then((msg) => console.log(msg));

  addFromWasm(2, 3).then((sum) => console.log('2 + 3 =', sum));

  render();
}

// Inicializa la escena al cargar el módulo.

init();
