const ACCENT_CLASSES = {
  blue: 'accent-blue-600',
  sky: 'accent-sky-600',
  cyan: 'accent-cyan-600',
  indigo: 'accent-indigo-600',
  purple: 'accent-purple-600',
  teal: 'accent-teal-600',
  emerald: 'accent-emerald-600',
}

export function RangeSlider({ id, value, onChange, min, max, step = 1, disabled = false, accent = 'emerald' }) {
  const accentStyle = ACCENT_CLASSES[accent] || ACCENT_CLASSES.emerald

  return (
    <input
      id={id}
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={onChange}
      disabled={disabled}
      className={`w-full h-2 cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 ${accentStyle}`}
    />
  )
}
