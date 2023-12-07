/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    spacing: {
      '1': '10px',
      '1.2': '12px',
      '1.5': '15px',
      '2': '20px',
      '2.6': '26px',
      '3': '30px',
      '4': '40px',
      '6': '60px',
      '6.6': '66px',
      '8': '80px',
      '10': '100px',
      '12': '120px',
    },
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
