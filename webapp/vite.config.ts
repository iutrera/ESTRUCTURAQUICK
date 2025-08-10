/**
 * Basic Vite configuration for the RepresentaTodo web application.
 * Outputs the production build to `dist/`.
 */
import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  build: {
    outDir: 'dist'
  }
});
