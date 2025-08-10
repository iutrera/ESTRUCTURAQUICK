# ESTRUCTURAQUICK

Subida inicial de ficheros.

## Webapp

Se añade un esqueleto de aplicación web basado en TypeScript y Three.js con soporte para
módulos de alto rendimiento en Rust compilados a WebAssembly.

- `webapp/`: interfaz web con Vite + TypeScript.
- `rust-wasm/`: módulo Rust exportando funciones a WASM.

Para desarrollar:

```bash
cd webapp
npm install   # actualmente falla por restricciones de red
npm run dev
```

```bash
cd rust-wasm
cargo build --target wasm32-unknown-unknown # puede fallar si no se puede descargar crates
```
