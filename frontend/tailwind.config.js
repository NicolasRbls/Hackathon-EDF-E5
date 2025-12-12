/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'edf-orange': {
          DEFAULT: '#FF7900',
          50: '#FFE8D6',
          100: '#FFDEC2',
          200: '#FFCA99',
          300: '#FFB670',
          400: '#FFA247',
          500: '#FF7900',
          600: '#CC6100',
          700: '#994900',
          800: '#663100',
          900: '#331800',
        },
        'edf-blue': {
          DEFAULT: '#005EB8',
          50: '#D6E9F9',
          100: '#C2DFF7',
          200: '#99CCF2',
          300: '#70B8ED',
          400: '#47A5E8',
          500: '#0082D9',
          600: '#005EB8',
          700: '#00478A',
          800: '#002F5C',
          900: '#00182E',
        },
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
