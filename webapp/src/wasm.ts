/**
 * Helper functions for interacting with the Rust-compiled WebAssembly module.
 * The WASM module exposes a simple `greet` function used here as proof of
 * concept for TypeScript ↔ WASM integration.
 */
// @ts-ignore: módulo generado por wasm-bindgen
import init, { greet, add } from '../../rust-wasm/pkg/representatodo_wasm';

/**
 * Calls the WASM `greet` function after ensuring the module is loaded.
 *
 * @param name - Name to include in the greeting message.
 * @returns Personalized greeting returned by the WASM module.
 */
export async function greetFromWasm(name: string): Promise<string> {
  await init();
  return greet(name);
}

/**
 * Adds two numbers using the WASM `add` function after the module has loaded.
 *
 * @param a - First operand.
 * @param b - Second operand.
 * @returns Sum computed within WebAssembly.
 */
export async function addFromWasm(a: number, b: number): Promise<number> {
  await init();
  return add(a, b);
}
