/** @type {import('tailwindcss').Config} */

module.exports = {
  future: {},
  content: ["../*/templates/*.{html,js}", "../*/templates/**/*.{html,js}"],
  darkMode: "media",
  theme: {
    extend: {
      screens: {
          "nav-breakpoint": "1050px", // prevents nav  links from wrapping into two lines
        },
        spacing: {
          "hot-1": "0.625rem", // 10px
          "hot-1.2": "0.75rem", // 12px
          "hot-1.5": "0.9375rem", // 15px
          "hot-2": "1.25rem", // 20px
          "hot-2.6": "1.625rem", // 26px
          "hot-3": "1.875rem", // 30px
          "hot-3.4": "2.125rem", // 34px
          "hot-4": "2.5rem", // 40px
          "hot-6": "3.75rem", // 60px
          "hot-6.6": "4.125rem", // 66px
          "hot-8": "5rem", // 80px
          "hot-10": "6.25rem", // 100px
          "hot-12": "7.5rem", // 120px
        },
        fontFamily: {
          barlow: ['"Barlow Condensed"', "sans-serif"],
          archivo: ["Archivo", "sans-serif"],
        },
        fontSize: {
          h1: ["3.5rem", "auto"], // 56pt
          h2: ["3rem", "auto"], // 48pt
          h3: ["2.375rem", "auto"], // 38pt
          h4: ["2rem", "auto"], // 32pt
          h5: ["1.75rem", "auto"], // 28pt
          intro: ["1.375rem", "auto"], // 22pt
          "base-20": ["1.25rem", "auto"], // 20pt
          "base-18": ["1.125rem", "auto"], // 18pt
          "base-16": ["1rem", "auto"], // 16pt
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
    },
  },
  variants: {},
  plugins: [
    require("@tailwindcss/forms"),
  ],
};
