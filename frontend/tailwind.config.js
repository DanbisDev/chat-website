/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      maxHeight: {
        '3/4': '75vh',
      }
    },
  },
  plugins: [],
}

