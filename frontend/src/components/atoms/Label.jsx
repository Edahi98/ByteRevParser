export function Label({ children, htmlFor }) {
  return (
    <label htmlFor={htmlFor} className="block text-sm font-semibold text-slate-800 mb-1.5">
      {children}
    </label>
  )
}

