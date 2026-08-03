import { pipelineFormRehydrated } from './pipelineFormSlice'

// IndexedDB y no localStorage porque el documento subido es un `File`:
// localStorage solo guarda strings, mientras que IndexedDB usa structured clone
// y conserva el `File` tal cual, sin volcarlo a base64 ni perder el handle.
const DB_NAME = 'reddragon'
const DB_VERSION = 1
const STORE_NAME = 'pipelineForm'
const STATE_KEY = 'state'
const SAVE_DELAY_MS = 300

function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)
    request.onupgradeneeded = () => request.result.createObjectStore(STORE_NAME)
    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error)
  })
}

function runTransaction(mode, run) {
  return openDatabase().then(
    (db) =>
      new Promise((resolve, reject) => {
        const transaction = db.transaction(STORE_NAME, mode)
        const request = run(transaction.objectStore(STORE_NAME))
        request.onsuccess = () => resolve(request.result)
        request.onerror = () => reject(request.error)
        transaction.oncomplete = () => db.close()
      }),
  )
}

// La persistencia es una comodidad, no parte del flujo: si IndexedDB falla
// (modo privado, cuota, esquema viejo) se sigue con el estado inicial.
export async function hydratePipelineForm(store) {
  try {
    const saved = await runTransaction('readonly', (objectStore) => objectStore.get(STATE_KEY))
    if (saved) store.dispatch(pipelineFormRehydrated(saved))
  } catch {
    // se arranca con el estado inicial
  }
}

export function startPipelineFormPersistence(store) {
  let timeoutId = null

  return store.subscribe(() => {
    clearTimeout(timeoutId)
    // Debounce: los campos del schema se escriben letra a letra y cada pulsación
    // dispara un dispatch; sin esto habría una escritura por tecla.
    timeoutId = setTimeout(() => {
      runTransaction('readwrite', (objectStore) =>
        objectStore.put(store.getState().pipelineForm, STATE_KEY),
      ).catch(() => {
        // se ignora: el estado en memoria sigue siendo la fuente de verdad
      })
    }, SAVE_DELAY_MS)
  })
}
