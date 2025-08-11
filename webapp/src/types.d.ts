/** Declaración de módulos para importar archivos CSV como texto bruto. */
declare module '*.csv?raw' {
  const content: string;
  export default content;
}
