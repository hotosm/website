/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./**/*.html', './**/*.js',],
  content: ["*/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        "hot-red": "#D73F3F",
        "hot-navy": "#20365B",
        "hot-dark-grey": "#68707F",
        "hot-slate-grey": "#929D83",
        "hot-light-grey": "#E1E0E0",
        "hot-off-white": "#F0EFEF",
        "hot-white": "#FFFFFF",
        "hot-black": "#000000",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
