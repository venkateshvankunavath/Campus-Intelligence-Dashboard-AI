import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#245FFF",
          50: "#eef3ff",
          600: "#1e4fd6",
          700: "#1840ad",
        },
      },
    },
  },
  plugins: [],
};
export default config;
