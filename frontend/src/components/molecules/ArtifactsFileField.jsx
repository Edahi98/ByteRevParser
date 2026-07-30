import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faShieldHalved, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'
import { Button } from '../atoms/Button'

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

export function ArtifactsFileField({ fileName, onChange, quickArchive, onUseQuickArchive, accent = 'teal' }) {
  const iconStyle = TEXT_ACCENT_CLASSES[accent] || TEXT_ACCENT_CLASSES.teal
  const fileNameStyle = FILENAME_ACCENT_CLASSES[accent] || FILENAME_ACCENT_CLASSES.teal

  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor="artifacts-file">
        <FontAwesomeIcon icon={faShieldHalved} className={`mr-1.5 ${iconStyle}`} />
        Detector
      </Label>
      <FileInput id="artifacts-file" accept=".zip" onChange={onChange} accent={accent} />

      {quickArchive && (
        <Button variant="secondary" onClick={onUseQuickArchive}>
          <span className="inline-flex items-center gap-1.5">
            <FontAwesomeIcon icon={faWandMagicSparkles} className={iconStyle} /> Usar este
          </span>
        </Button>
      )}

      {fileName && (
        <span className={`text-xs font-medium truncate ${fileNameStyle}`}>{fileName}</span>
      )}
    </div>
  )
}
