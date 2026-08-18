import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

/** Le serveur de jeu tient le socket ; en dev, Vite lui passe la main. */
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/socket.io": { target: "http://localhost:8000", ws: true },
    },
  },
  test: {
    environment: "node",
    include: ["tests/**/*.test.{ts,tsx}"],
  },
});
