
/**
 * Punto de entrada de la aplicación web. Utiliza WebGL puro para renderizar
 * un marco estructural cúbico interactivo sin depender de bibliotecas
 * externas. La estructura puede rotarse y hacer zoom con el ratón, sirviendo
 * como demostración de visualización 3D de alto rendimiento.
 */
import { greetFromWasm, addFromWasm } from './wasm';

import { loadStructure, FrameStructure } from './structure';
import {
  perspectiva,
  identidad,
  multiplica,
  traslada,
  rotaX,
  rotaY,
} from './math';


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


  // Obtiene la estructura a visualizar (nodos y aristas).
  const estructura: FrameStructure = loadStructure();
  const vertices = new Float32Array(estructura.nodes.flat());
  const indices = new Uint16Array(estructura.edges.flat());


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


  // Funciones de álgebra lineal importadas desde `math.ts` para mantener el
  // punto de entrada enfocado en la lógica de renderizado.


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
