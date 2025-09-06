/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#F9F1E8',
          100: '#F9F1E8',
          200: '#F7D7AD',
          300: '#F7D7AD',
          400: '#DEA8A2',
          500: '#DEA8A2',
          600: '#DEA8A2',
          700: '#DEA8A2',
          800: '#3D3833',
          900: '#3D3833',
        },
        secondary: {
          50: '#F9F1E8',
          100: '#F9F1E8',
          200: '#F7D7AD',
          300: '#F7D7AD',
          400: '#F7D7AD',
          500: '#F7D7AD',
          600: '#DEA8A2',
          700: '#DEA8A2',
          800: '#3D3833',
          900: '#3D3833',
        },
        accent: {
          50: '#F9F1E8',
          100: '#F9F1E8',
          200: '#F7D7AD',
          300: '#F7D7AD',
          400: '#DEA8A2',
          500: '#DEA8A2',
          600: '#DEA8A2',
          700: '#DEA8A2',
          800: '#3D3833',
          900: '#3D3833',
        },
        background: 'transparent',
        foreground: '#3D3833',
        border: '#DEA8A2',
      },
      fontFamily: {
        sans: ['"Libertinus Sans"', 'system-ui', 'sans-serif'],
        mono: ['"Libertinus Sans"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
