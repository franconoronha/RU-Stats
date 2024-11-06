/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,vue}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#7743DB',
        'secondary': '#C3ACD0'
      },
    },
  },
  plugins: [],
}

