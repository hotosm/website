/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "media",
  theme: {
    spacing: {
      1: "10px",
      1.2: "12px",
      1.5: "15px",
      2: "20px",
      2.6: "26px",
      3: "30px",
      4: "40px",
      6: "60px",
      6.6: "66px",
      8: "80px",
      10: "100px",
      12: "120px",
    },
    extend: {
      fontFamily: {
        barlow: ['"Barlow Condensed"', "sans-serif"],
        archivo: ["Archivo", "sans-serif"],
      },
      fontSize: {
        h1: ["56pt", "auto"],
        h2: ["48pt", "auto"],
        h3: ["38pt", "auto"],
        h4: ["32pt", "auto"],
        h5: ["28pt", "auto"],
        intro: ["22pt", "auto"],
        "base-18": ["18pt", "auto"],
        "base-16": ["16pt", "auto"],
      },
      colors: {
        "hot-red": "#D73F3F",
        "hot-navy": "#20365B",
        "hot-dark-grey": "#68707F",
        "hot-slate-grey": "#929D83",
        "hot-light-grey": "#E1E0E0",
        "hot-off-white": "#F0EFEF",
        "hot-white": "#FFFFFF",
        "hot-black": "#000000",
      },
      borderRadius: {
        8: "8px",
      },
      borderWidth: {
        "2pt": "2.66667px",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
