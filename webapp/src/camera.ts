/**
 * Implementa una cámara orbital sencilla para escenas 3D.
 *
 * La cámara permite rotar alrededor del origen de coordenadas, desplazarse
 * lateralmente y acercarse o alejarse mediante eventos de ratón. Está
 * pensada para ser utilizada en conjunto con WebGL y las utilidades
 * matriciales del módulo `math`.
 */
import { identidad, traslada, rotaX, rotaY } from './math';

/** Controlador de cámara orbital basado en interacción con el ratón. */
export class OrbitCamera {
  private rotX = 0;
  private rotY = 0;
  private distance: number;

  private readonly initialDistance: number;
  private dragging = false;
  private button = 0;
  private last = { x: 0, y: 0 };
  private offsetX = 0;
  private offsetY = 0;

  /**
   * Crea una nueva cámara orbital.
   *
   * @param distance Distancia inicial del ojo al origen.
   */
  constructor(distance = 5) {
    this.distance = distance;
    this.initialDistance = distance;
  }

  /**
   * Atacha los manejadores de eventos de ratón al canvas especificado.
   * Permite rotar la cámara con arrastre, desplazar el encuadre con el
   * botón derecho y hacer zoom con la rueda.
   */
  attach(canvas: HTMLCanvasElement): void {
    canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    canvas.addEventListener('mousedown', (e) => {
      this.dragging = true;
      this.button = e.button;
      this.last.x = e.clientX;
      this.last.y = e.clientY;
    });
    canvas.addEventListener('mouseup', () => {
      this.dragging = false;
    });
    canvas.addEventListener('mousemove', (e) => {
      if (!this.dragging) return;
      const dx = e.clientX - this.last.x;
      const dy = e.clientY - this.last.y;
      if (this.button === 2) {
        const scale = this.distance * 0.005;
        this.offsetX -= dx * scale;
        this.offsetY += dy * scale;
      } else {
        this.rotY += dx * 0.01;
        this.rotX += dy * 0.01;
      }
      this.last.x = e.clientX;
      this.last.y = e.clientY;
    });
    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.distance += e.deltaY * 0.01;
      if (this.distance < 0.1) this.distance = 0.1;
    });
  }

  /**
   * Restablece la cámara a su estado inicial, eliminando rotaciones,
   * desplazamientos y zoom acumulados.
   */
  reset(): void {
    this.rotX = 0;
    this.rotY = 0;
    this.offsetX = 0;
    this.offsetY = 0;
    this.distance = this.initialDistance;
  }

  /** Devuelve la matriz de vista calculada a partir del estado actual. */
  getViewMatrix(): Float32Array {
    let view = identidad();
    view = traslada(view, [this.offsetX, this.offsetY, -this.distance]);
    return view;
  }

  /** Devuelve la matriz de modelo que aplica las rotaciones de la cámara. */
  getModelMatrix(): Float32Array {
    let model = identidad();
    model = rotaX(model, this.rotX);
    model = rotaY(model, this.rotY);
    return model;
  }
}
