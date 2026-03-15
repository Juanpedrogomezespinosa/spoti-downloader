// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import tailwindcss from "@tailwindcss/vite";

// https://astro.build/config
export default defineConfig({
  // Cargamos React como integración de Astro
  integrations: [react()],
  // Cargamos Tailwind v4 como plugin de Vite
  vite: {
    plugins: [tailwindcss()],
  },
});
