import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#10212b",
        brand: "#167c80",
        sand: "#f5efe6",
        ember: "#d95f3f"
      }
    }
  },
  plugins: []
} satisfies Config;

