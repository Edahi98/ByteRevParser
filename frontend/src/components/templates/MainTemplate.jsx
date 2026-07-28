export function MainTemplate({ header, children }) {
  return (
    <div className="min-h-screen bg-white text-slate-800 flex flex-col font-sans antialiased">
      {header}
      <main className="flex-1 w-full flex flex-col">
        {children}
      </main>
      <footer className="w-full py-6 text-center text-xs text-slate-500 border-t border-slate-200/60 bg-white">
        RedDragon &copy; {new Date().getFullYear()} OLAN Manufacturing Systems
      </footer>
    </div>
  )
}
