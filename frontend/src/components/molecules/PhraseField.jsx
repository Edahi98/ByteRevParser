import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCommentDots } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { TextInput } from '../atoms/TextInput'

const TEXT_ACCENT_CLASSES = {
  teal: 'text-teal-500',
  violet: 'text-violet-500',
  amber: 'text-amber-500',
}

export function PhraseField({ value, onChange, accent = 'teal' }) {
  const iconStyle = TEXT_ACCENT_CLASSES[accent] || TEXT_ACCENT_CLASSES.teal

  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="compare-phrase">
        <FontAwesomeIcon icon={faCommentDots} className={`mr-1.5 ${iconStyle}`} />
        Frase
      </Label>
      <TextInput
        id="compare-phrase"
        value={value}
        onChange={onChange}
        placeholder="ej. se cambia la redaccion del objetivo"
        accent={accent}
      />
    </div>
  )
}
