import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileLines } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'

const TEXT_ACCENT_CLASSES = {
  teal: 'text-teal-500',
  violet: 'text-violet-500',
  amber: 'text-amber-500',
}

const FILENAME_ACCENT_CLASSES = {
  teal: 'text-teal-700',
  violet: 'text-violet-700',
  amber: 'text-amber-700',
}

export function NewPhrasesFileField({ fileName, onChange, accent = 'teal' }) {
  const iconStyle = TEXT_ACCENT_CLASSES[accent] || TEXT_ACCENT_CLASSES.teal
  const fileNameStyle = FILENAME_ACCENT_CLASSES[accent] || FILENAME_ACCENT_CLASSES.teal

  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="new-phrases-file">
        <FontAwesomeIcon icon={faFileLines} className={`mr-1.5 ${iconStyle}`} />
        Frases a revisar
      </Label>
      <FileInput id="new-phrases-file" accept=".csv" onChange={onChange} accent={accent} />
      {fileName && <span className={`text-xs font-medium truncate ${fileNameStyle}`}>{fileName}</span>}
    </div>
  )
}
