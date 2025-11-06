import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";
import path from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, "../backend/ssl/key.pem")),
      cert: fs.readFileSync(path.resolve(__dirname, "../backend/ssl/cert.pem")),
    },
    proxy: {
      "/api": {
        target: "https://localhost:8000",
        changeOrigin: true,
      },
    },
    // Указываем базовый путь для ресурсов. Если приложение развернуто в корне, то оставляем '/'
    base: "/",
  },
  build: {
    // Убеждаемся, что пути к ресурсам относительные
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name]-[hash][extname]'
      }
    }
  }
});
