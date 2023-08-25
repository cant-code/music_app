import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from "vite-plugin-vuetify";

// https://vitejs.dev/config/
const path = require("path");
export default defineConfig({
  plugins: [vue(),
  vuetify({ autoImport: true })],
  resolve: {
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
    alias: {
      "@": path.resolve(__dirname, "./src")
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
