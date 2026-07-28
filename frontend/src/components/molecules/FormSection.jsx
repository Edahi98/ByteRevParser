import { SectionTitle } from '../atoms/SectionTitle'

const STRIPE_BG_CLASSES = {
  blue: 'bg-white',
  indigo: 'bg-blue-50/60',
  sky: 'bg-white',
  cyan: 'bg-blue-50/40',
  purple: 'bg-purple-50/30',
  teal: 'bg-teal-50/30',
  emerald: 'bg-emerald-50/30',
}

export function FormSection({ title, icon, accent = 'blue', subtitle, children }) {
  const bgClass = STRIPE_BG_CLASSES[accent] || 'bg-white'

  return (
    <section className={`w-full py-12 md:py-16 ${bgClass}`}>
      <div className="max-w-4xl mx-auto px-4 md:px-6 flex flex-col gap-6">
        {title && (
          <div className="border-b border-slate-200/80 pb-4">
            <SectionTitle icon={icon} accent={accent}>
              {title}
            </SectionTitle>
            {subtitle && (
              <p className="text-xs md:text-sm text-slate-500 mt-1.5 font-normal leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>
        )}
        <div className="flex flex-col gap-5">{children}</div>
      </div>
    </section>
  )
}



