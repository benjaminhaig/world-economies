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
        pixelify: ['Pixelify Sans', 'sans-serif'],
        handjet: ['Handjet', 'sans-serif'],
        raleway: ['Raleway', 'sans-serif'],
        playfair: ['Playfair', 'serif']
      },
    },
  },
  plugins: [],
}

