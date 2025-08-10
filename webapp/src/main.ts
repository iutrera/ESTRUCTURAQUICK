/**
 * Punto de entrada de la aplicación web. Utiliza WebGL puro para renderizar
 * un marco estructural cúbico interactivo sin depender de bibliotecas
 * externas. La estructura puede rotarse y hacer zoom con el ratón, sirviendo
 * como demostración de visualización 3D de alto rendimiento.
 */
import { greetFromWasm, addFromWasm } from './wasm';
import {
  loadStructure,
  FrameStructure,
  computeBounds,
  StructureBounds,
} from './structure';
import { perspectiva, multiplica } from './math';
import { OrbitCamera } from './camera';

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

  // Shaders para colorear y dimensionar los elementos de la estructura.
  const program = createProgram(
    gl,
    `
    attribute vec3 position;
    uniform mat4 mvp;
    void main() {
      gl_Position = mvp * vec4(position, 1.0);
      gl_PointSize = 6.0; // Tamaño de los nodos renderizados como puntos
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

  // Obtiene la estructura a visualizar (nodos y aristas).
  const estructura: FrameStructure = loadStructure();

  // Analiza su volumen para centrarla en el origen y ajustar la cámara.
  const bounds: StructureBounds = computeBounds(estructura);
  const centeredNodes = estructura.nodes.map((n) => [
    n[0] - bounds.center[0],
    n[1] - bounds.center[1],
    n[2] - bounds.center[2],
  ]);

  // Transforma los nodos centrados en un arreglo contiguo de floats.
  const vertices = new Float32Array(centeredNodes.flat());
  const indices = new Uint16Array(estructura.edges.flat());
  const nodeCount = estructura.nodes.length; // cantidad de nodos para dibujar

  const vertexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

  const indexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);

  // Crea un conjunto de ejes XYZ para orientar la escena.
  const axisLength = bounds.radius * 1.5;
  const axisVertices = new Float32Array([
    0, 0, 0, axisLength, 0, 0, // Eje X en rojo
    0, 0, 0, 0, axisLength, 0, // Eje Y en verde
    0, 0, 0, 0, 0, axisLength, // Eje Z en azul
  ]);
  const axisBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, axisBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, axisVertices, gl.STATIC_DRAW);

  const posLoc = gl.getAttribLocation(program, 'position');
  gl.enableVertexAttribArray(posLoc);
  // Restablece el búfer de vértices principal tras preparar los ejes.
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
  gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);

  const colorLoc = gl.getUniformLocation(program, 'uColor');
  gl.uniform3f(colorLoc, 0.1, 0.4, 0.8);

  const mvpLoc = gl.getUniformLocation(program, 'mvp');
  gl.enable(gl.DEPTH_TEST);

  // Control de cámara orbital para rotación, desplazamiento y zoom.
  // La distancia inicial se calcula a partir del tamaño de la estructura.
  const camera = new OrbitCamera(bounds.radius * 2);
  camera.attach(canvas);
  // Permite restablecer la vista presionando la tecla 'r' y alternar
  // la visualización de aristas y nodos con 'e' y 'n' respectivamente.
  let showEdges = true;
  let showNodes = true;
  window.addEventListener('keydown', (e) => {
    if (e.key === 'r') {
      camera.reset();
    } else if (e.key === 'e') {
      showEdges = !showEdges;
    } else if (e.key === 'n') {
      showNodes = !showNodes;
    }
  });


  // Bucle de renderizado.
  function render(): void {
    gl.clearColor(0.95, 0.95, 0.95, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const proy = perspectiva(
      Math.PI / 4,
      canvas.width / canvas.height,
      0.1,
      bounds.radius * 10
    );
    const modelo = camera.getModelMatrix();
    const vista = camera.getViewMatrix();
    const mvp = multiplica(proy, multiplica(vista, modelo));

    gl.uniformMatrix4fv(mvpLoc, false, mvp);

    // Dibuja los ejes de referencia.
    gl.bindBuffer(gl.ARRAY_BUFFER, axisBuffer);
    gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);
    gl.uniform3f(colorLoc, 1.0, 0.0, 0.0); // X en rojo
    gl.drawArrays(gl.LINES, 0, 2);
    gl.uniform3f(colorLoc, 0.0, 1.0, 0.0); // Y en verde
    gl.drawArrays(gl.LINES, 2, 2);
    gl.uniform3f(colorLoc, 0.0, 0.0, 1.0); // Z en azul
    gl.drawArrays(gl.LINES, 4, 2);

    if (showEdges) {
      // Dibuja las aristas como segmentos azules.
      gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
      gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);
      gl.uniform3f(colorLoc, 0.1, 0.4, 0.8);
      gl.drawElements(gl.LINES, indices.length, gl.UNSIGNED_SHORT, 0);
    }

    if (showNodes) {
      // Dibuja los nodos como puntos rojos.
      gl.uniform3f(colorLoc, 0.8, 0.1, 0.1);
      gl.drawArrays(gl.POINTS, 0, nodeCount);
    }


    requestAnimationFrame(render);
  }

  greetFromWasm('ingeniero').then((msg) => console.log(msg));
  addFromWasm(2, 3).then((sum) => console.log('2 + 3 =', sum));
  render();
}

// Inicializa la escena al cargar el módulo.
init();
