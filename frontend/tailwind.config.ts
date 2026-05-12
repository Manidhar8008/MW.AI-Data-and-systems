import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f2f8f6",
          100: "#dbeee8",
          500: "#1f8a70",
          600: "#176f5b",
          700: "#125748",
        },
        ink: {
          900: "#18201f",
          700: "#3f4d4a",
          500: "#66736f",
        },
      },
      boxShadow: {
        panel: "0 1px 2px rgba(24, 32, 31, 0.08)",
      },
    },
  },
  plugins: [],
} satisfies Config;

