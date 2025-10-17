import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const config = {
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:5000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };

  // --- CORRECTION ---
  // Apply the '/static/' base path ONLY for production builds.
  if (command === 'build') {
    config.base = '/static/';
  }
  // For the 'serve' command (development), 'base' defaults to '/', which is correct.
  // --- END CORRECTION ---

  return config;
});