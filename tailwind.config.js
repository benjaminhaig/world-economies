/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      borderColor: {
        DEFAULT: '#334155',  // slate-800 color
      },
      boxShadowColor: {
        DEFAULT: '#1e293b',  // slate-900 color
      },
      fontFamily: {
        handjet: ['Handjet', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

