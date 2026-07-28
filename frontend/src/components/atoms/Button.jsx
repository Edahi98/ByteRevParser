const VARIANT_CLASSES = {
  primary:
    'bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg py-2.5 px-5 transition-all text-sm w-full cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600',
  secondary:
    'bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg py-2 px-4 transition-all text-sm border border-slate-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed',
  green:
    'bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 rounded-lg py-2.5 px-5 transition-all text-sm w-full cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-emerald-500 disabled:hover:to-teal-500',
}

export function Button({ children, onClick, type = 'button', variant = 'primary', disabled = false }) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${VARIANT_CLASSES[variant] || VARIANT_CLASSES.primary}`}
    >
      {children}
    </button>
  )
}

