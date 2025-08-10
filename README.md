# ESTRUCTURAQUICK

Subida inicial de ficheros.

## Webapp

Se añade un esqueleto de aplicación web basado en TypeScript y Three.js con soporte para
módulos de alto rendimiento en Rust compilados a WebAssembly.

- `webapp/`: interfaz web con Vite + TypeScript.
- `rust-wasm/`: módulo Rust exportando funciones a WASM.

La aplicación de ejemplo renderiza un cubo 3D con controles básicos de ratón
(rotación y zoom) que sirven como punto de partida para una visualización
interactiva de estructuras. También se demuestra la llamada a una función
de WebAssembly generada a partir de Rust.

El módulo Rust no depende de crates externos para que las pruebas puedan
ejecutarse incluso sin acceso a internet. Para crear un paquete WebAssembly
real se deberá añadir `wasm-bindgen` y otras dependencias cuando se disponga
de conectividad.

Para desarrollar:

```bash
cd webapp
npm install
npm test      # ejecuta comprobación de tipos
npm run dev
```

```bash
cd rust-wasm
cargo test
cargo build --target wasm32-unknown-unknown
```
