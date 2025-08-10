/**
 * Implementa una cámara orbital sencilla para escenas 3D.
 *
 * La cámara permite rotar alrededor del origen de coordenadas y acercarse o
 * alejarse mediante eventos de ratón. Está pensada para ser utilizada en
 * conjunto con WebGL y las utilidades matriciales del módulo `math`.
 */
import { identidad, traslada, rotaX, rotaY } from './math';

/** Controlador de cámara orbital basado en interacción con el ratón. */
export class OrbitCamera {
  private rotX = 0;
  private rotY = 0;
  private distance: number;
  private dragging = false;
  private last = { x: 0, y: 0 };

  /**
   * Crea una nueva cámara orbital.
   *
   * @param distance Distancia inicial del ojo al origen.
   */
  constructor(distance = 5) {
    this.distance = distance;
  }

  /**
   * Atacha los manejadores de eventos de ratón al canvas especificado.
   * Permite rotar la cámara con arrastre y hacer zoom con la rueda.
   */
  attach(canvas: HTMLCanvasElement): void {
    canvas.addEventListener('mousedown', (e) => {
      this.dragging = true;
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
      this.rotY += dx * 0.01;
      this.rotX += dy * 0.01;
      this.last.x = e.clientX;
      this.last.y = e.clientY;
    });
    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.distance += e.deltaY * 0.01;
      if (this.distance < 0.1) this.distance = 0.1;
    });
  }

  /** Devuelve la matriz de vista calculada a partir del estado actual. */
  getViewMatrix(): Float32Array {
    let view = identidad();
    view = traslada(view, [0, 0, -this.distance]);
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
