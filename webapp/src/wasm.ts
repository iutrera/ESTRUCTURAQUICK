import init, { greet } from '../../rust-wasm/pkg/representatodo_wasm';

export async function greetFromWasm(name: string): Promise<string> {
  await init();
  return greet(name);
}
