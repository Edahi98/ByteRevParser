import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBoxArchive, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons'
import { Label } from '../atoms/Label'
import { FileInput } from '../atoms/FileInput'
import { Button } from '../atoms/Button'

export function ArtifactsFileField({ fileName, onChange, quickArchive, onUseQuickArchive, accent = 'teal' }) {
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor="artifacts-file">Tu modelo entrenado</Label>
      <FileInput id="artifacts-file" accept=".zip" onChange={onChange} accent={accent} />
      <p className="text-xs text-slate-500">
        Sube el archivo que descargaste al entrenar tu modelo (el que termina en ".zip").
      </p>

      {quickArchive && (
        <div className="mt-1">
          <Button variant="secondary" onClick={onUseQuickArchive}>
            <span className="inline-flex items-center gap-1.5">
              <FontAwesomeIcon icon={faWandMagicSparkles} className="text-emerald-500" /> Usar el modelo que acabas de entrenar
            </span>
          </Button>
        </div>
      )}

      {fileName && (
        <div className="mt-1 inline-flex items-center gap-2 bg-teal-50 border border-teal-200/80 text-teal-800 text-xs font-medium px-3 py-1.5 rounded-md w-fit">
          <span><FontAwesomeIcon icon={faBoxArchive} /></span>
          <span>Modelo seleccionado: <strong className="font-semibold">{fileName}</strong></span>
        </div>
      )}
    </div>
  )
}
