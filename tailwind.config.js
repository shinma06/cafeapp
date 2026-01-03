/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './pages/templates/**/*.html',
    './accounts/templates/**/*.html',
    './pages/**/*.py',
    './accounts/**/*.py',
    './cafeapp/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        'cafe-brown': '#432',
        'cafe-cyan': '#0bd',
        'cafe-cyan-dark': '#0090aa',
        'cafe-bg': '#FAF7F0',
      },
      fontFamily: {
        'philosopher': ['Philosopher', 'serif'],
        'yugothic': ['"Yu Gothic Medium"', '"游ゴシック Medium"', 'YuGothic', '"游ゴシック体"', '"ヒラギノ角ゴ Pro W3"', 'sans-serif'],
        'yumincho': ['"Yu Mincho"', 'YuMincho', 'serif'],
      },
      maxWidth: {
        'container': '1100px',
      },
    },
  },
  plugins: [],
}

