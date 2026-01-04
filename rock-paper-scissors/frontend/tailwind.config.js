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
          DEFAULT: '#8B5CF6',
          hover: '#7C3AED',
          glow: '#A78BFA'
        },
        secondary: {
          DEFAULT: '#EC4899',
          hover: '#DB2777',
          glow: '#F472B6'
        },
        dark: {
          DEFAULT: '#0F172A',
          lighter: '#1E293B',
          card: 'rgba(30, 41, 59, 0.7)'
        },
        neon: {
          blue: '#00F0FF',
          pink: '#FF00FF',
          purple: '#BD00FF'
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      },
      boxShadow: {
        'neon-blue': '0 0 10px #00F0FF, 0 0 20px #00F0FF',
        'neon-pink': '0 0 10px #FF00FF, 0 0 20px #FF00FF',
        'neon-purple': '0 0 10px #BD00FF, 0 0 20px #BD00FF',
      }
    },
  },
  plugins: [],
}
