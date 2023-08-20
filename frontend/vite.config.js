import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
import { createVuePlugin as vue } from "vite-plugin-vue2";
import { VuetifyResolver } from 'unplugin-vue-components/resolvers';
import Components from 'unplugin-vue-components/vite';

// https://vitejs.dev/config/
const path = require("path");
export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
          VuetifyResolver()
      ]
    })
  ],
  resolve: {
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  },
  server: {
    proxy: {
      "/dj-rest-auth": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/spotify": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
})
