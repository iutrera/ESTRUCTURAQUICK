# ESTRUCTURAQUICK

Subida inicial de ficheros.

## Webapp

Se incorpora una demostración de aplicación web basada en TypeScript y WebGL
puro. El código representa una estructura en forma de marco cúbico mediante
segmentos de línea complementados con puntos para marcar los nodos. La escena
puede rotarse, desplazarse y hacer zoom con el ratón, ofreciendo una
visualización 3D fluida. Además muestra cómo invocar funciones de alto
rendimiento escritas en Rust y compiladas a WebAssembly, incluyendo un ejemplo
de suma numérica.

La geometría de la estructura se describe en `webapp/src/structure.json` y se
importa mediante el módulo `webapp/src/structure.ts`. Modificando el JSON se
pueden cargar marcos distintos sin tocar el motor de renderizado.

Al cargarse, la aplicación calcula el centro y el tamaño de la estructura para
encuadrarla automáticamente. La cámara orbital se inicializa a una distancia
adecuada, lo que evita ajustes manuales cuando se sustituyen los datos.

Las transformaciones de matrices empleadas por WebGL se encuentran en
`webapp/src/math.ts`, separando la lógica de álgebra lineal del punto de
entrada `main.ts` para favorecer la claridad y la reutilización.

El control de cámara (rotación y zoom con el ratón) se implementa en
`webapp/src/camera.ts`, manteniendo el archivo `main.ts` enfocado únicamente
en el ciclo de renderizado y la gestión de WebGL.

- `webapp/`: interfaz web con Vite + TypeScript.
- `rust-wasm/`: módulo Rust exportando funciones a WASM.

El módulo Rust no depende de crates externos para que las pruebas puedan
ejecutarse incluso sin acceso a internet. Para crear un paquete WebAssembly
real se deberá añadir `wasm-bindgen` y otras dependencias cuando se disponga
de conectividad.

### Desarrollo

```bash
cd webapp
npm install      # instala TypeScript y Vite
npm test         # comprobación de tipos
npm run dev
```

```bash
cd rust-wasm
cargo test
cargo build --target wasm32-unknown-unknown
```
