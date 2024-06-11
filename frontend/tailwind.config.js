/** @type {import('tailwindcss').Config} */

module.exports = {
  future: {},
  content: [
    "../*/templates/*.{html,js}",
    "../*/templates/**/*.{html,js}",
    "../app/*/templates/*.{html,js}",
    "../app/*/templates/**/*.{html,js}",
  ],
  darkMode: "media",
  theme: {
    extend: {
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
        barlow: "var(--font-barlow)",
        archivo: "var(--font-archivo)",
      },
      fontSize: {
        h1: "var(--font-size-h1)", // 56pt
        h2: "var(--font-size-h2)", // 48pt
        h3: "var(--font-size-h3)", // 38pt
        h4: "var(--font-size-h4)", // 32pt
        h5: "var(--font-size-h5)", // 28pt
        intro: "var(--font-size-intro)", // 22pt
        base: "var(--font-size-base)", // 20pt
        small: "var(--font-size-small)",
        mini: "var(--font-size-mini)",
      },
      colors: {
        "hot-red": "var(--hot-red)",
        "hot-navy": "var(--hot-navy)",
        "hot-navy-grey": "var(--hot-navy-grey)",
        "hot-dark-grey": "var(--hot-dark-grey)",
        "hot-slate-grey": "var(--hot-slate-grey)",
        "hot-light-grey": "var(--hot-light-grey)",
        "hot-off-white": "var(--hot-off-white)",
        "hot-white": "var(--hot-white)",
        "hot-black": "var(--hot-black)",
        "hot-barely-not-white": "var(--hot-barely-not-white)",
      },
    },
  },
  variants: {},
  plugins: [require("@tailwindcss/forms")],
};
