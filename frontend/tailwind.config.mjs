/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#0bda50",
        "background-light": "#f5f8f6",
        "background-dark": "#102216",
      },
      fontFamily: {
        display: ["Spline Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
