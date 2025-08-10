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


La geometría de la estructura se define en `webapp/src/structure.ts`, donde
se describen nodos y aristas de forma modular para poder cargar o generar
otras configuraciones en el futuro.


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
