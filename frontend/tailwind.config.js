/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'], // Update as per your project structure
  theme: {
    extend: {
      keyframes: {
        progress: {
          '0%': { left: '-100%', width: '0%' },
          '50%': { left: '0%', width: '100%' },
          '100%': { left: '100%', width: '0%' },
        },
      },
      animation: {
        'progress-bar': 'progress 2s infinite ease-in-out',
      },
    },
  },
  plugins: [],
};
