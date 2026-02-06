/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./App.tsx", "./index.tsx"],
  theme: {
    extend: {
      colors: {
        twitter: "#1DA1F2",
      },
    },
  },
  plugins: [],
};

