/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
    './static/**/*.js',
  ],
  darkMode: 'class',
  safelist: [
    // CSS-variable arbitrary-value classes used in Django templates
    'bg-[color:var(--accent)]',
    'bg-[color:var(--border)]',
    'bg-[color:var(--ok-soft)]',
    'bg-[color:var(--surface-2)]',
    'bg-[color:var(--surface-3)]',
    'bg-[color:var(--warn-soft)]',
    'text-[color:var(--accent-2)]',
    'text-[color:var(--ink)]',
    'text-[color:var(--ink-2)]',
    'text-[color:var(--muted)]',
    'text-[color:var(--muted-2)]',
    'text-[color:var(--ok)]',
    'text-[color:var(--warn)]',
    'hover:bg-[color:var(--surface-2)]',
    'hover:bg-[color:var(--surface-3)]',
    'hover:text-[color:var(--ink)]',
    // Hover shadow utilities
    'hover:shadow-card',
    'hover:shadow-card2',
    'hover:shadow-card3',
    // Transition utilities used in templates
    'hover:underline',
    // last/first variants
    'last:border-b-0',
    'first:border-t-0',
    // Responsive variants that might not scan from Django template conditionals
    'md:ml-60',
    'md:translate-x-0',
    '-translate-x-full',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Geist', 'ui-sans-serif', '-apple-system', 'Segoe UI', 'sans-serif'],
        serif: ['Newsreader', 'ui-serif', 'Georgia', 'serif'],
        mono: ['Geist Mono', 'ui-monospace', 'JetBrains Mono', 'monospace'],
      },
      colors: {
        cream: {
          50: '#FDFBF5',
          100: '#FAF6EC',
          200: '#F7F2E4',
          300: '#F0E9D2',
          400: '#EFE7CE',
          500: '#E1D8BC',
          600: '#D4C9A8',
          700: '#B9AC85',
        },
        ink: {
          DEFAULT: '#0E1B2E',
          2: '#2C3E5C',
          3: '#4A5A77',
        },
        muted: {
          DEFAULT: '#6F7E97',
          2: '#94A0B7',
          faint: '#C7BFA9',
        },
        accent: {
          DEFAULT: '#F5B544',
          2: '#E89A1B',
          soft: '#FCE5AA',
        },
        primary: {
          DEFAULT: '#1F3A68',
          hover: '#16294A',
        },
        ok: {
          DEFAULT: '#2D7D5C',
          soft: '#D6EBDD',
        },
        warn: {
          DEFAULT: '#C2410C',
          soft: '#FBD8B5',
        },
        rose: { DEFAULT: '#C03E5C' },
        violet: { DEFAULT: '#7E4EC0' },
        teal: { DEFAULT: '#0E9488' },
      },
      borderRadius: {
        sm: '6px',
        DEFAULT: '10px',
        lg: '14px',
        xl: '20px',
        '2xl': '28px',
        pill: '999px',
      },
      boxShadow: {
        card: '0 1px 0 rgba(14,27,46,.04), 0 1px 2px rgba(14,27,46,.05)',
        card2: '0 1px 0 rgba(14,27,46,.04), 0 6px 16px -4px rgba(14,27,46,.10)',
        card3: '0 1px 0 rgba(14,27,46,.04), 0 18px 40px -10px rgba(14,27,46,.18)',
        pop: '0 1px 0 rgba(14,27,46,.04), 0 24px 60px -16px rgba(14,27,46,.30)',
        accent: '0 4px 10px -2px rgba(245,181,68,.5)',
      },
    },
  },
  plugins: [],
}
