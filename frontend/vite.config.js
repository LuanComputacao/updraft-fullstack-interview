import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import vue from '@vitejs/plugin-vue';
import { defineConfig, loadEnv } from 'vite';
import eslint from 'vite-plugin-eslint';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const port = Number(env.VITE_APP_PORT || 5180);
  return {
    plugins: [vue(), eslint()],
    build: { minify: false, target: 'es2021' },
    resolve: {
      alias: [{ find: '@', replacement: resolve(__dirname, './src') }],
    },
    server: {
      host: '0.0.0.0',
      port,
    },
  };
});
