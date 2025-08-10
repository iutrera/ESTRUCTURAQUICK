# ESTRUCTURAQUICK

Subida inicial de ficheros.

## Webapp

Se incorpora una demostración de aplicación web basada en TypeScript y WebGL
puro. El código renderiza un cubo 3D interactivo que puede rotarse y hacer
zoom con el ratón, y muestra cómo invocar funciones de alto rendimiento
escritas en Rust y compiladas a WebAssembly.

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
