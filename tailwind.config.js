/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"],
  theme: {
    extend: {
      colors: {
        pallete: {
          1: '#E1A36F',
          2: '#DEC484',
          3: '#E2D8A5',
          4: '#6F9F9C',
          5: '#577E89',
        }
      }
    },
  },
  plugins: [],
}

