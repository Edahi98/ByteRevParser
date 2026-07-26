# Arquitectura de RedDragon

RedDragon es un servicio FastAPI que convierte documentos (`doc`, `docx`, `xls`, `xlsx`, `pdf`) a XML, extrae su contenido, ejecuta un pipeline de transformación de datos contra un motor externo (**Tsubasa**) y devuelve el resultado final ya sea como XML podado o como lista de strings.

## Estilo arquitectónico

El proyecto sigue una **arquitectura en capas estilo MVC**, con dos capas intermedias adicionales (**preservices** y **orchestrators**) entre el controller y los services de bajo nivel:

```
main.py                     → bootstrap: crea FastAPI(lifespan=...), incluye el router, arranca uvicorn
controllers/                → Controller: parsea el request, valida, arma la respuesta
preservices/                → prepara insumos (I/O de archivos temporales) antes del pipeline
orchestrators/               → coordinan varios services en un flujo de negocio, sin lógica propia de bajo nivel
services/                    → lógica atómica de bajo nivel, una responsabilidad por archivo
models/                      → Model: schemas Pydantic de request/response
views/                       → View: da forma a la respuesta final a partir de datos crudos
resources/                    → binarios externos que ejecutan los services (xmljava-docker, tsubasa)
```

### Regla de dependencia

Cada capa solo llama hacia abajo, nunca al revés:

```
controller → preservice, orchestrator, view, model
orchestrator → services
service → binarios externos (resources/*) o librerías (bs4, pdf2docx, requests)
```

## Capas

### `main.py` — bootstrap

- Crea la instancia `FastAPI(lifespan=lifespan)` e incluye el router de `controllers/pipeline_controller.py`.
- `lifespan` arranca `TsubasaService` (`start()`) al iniciar el servidor y lo detiene (`stop()`) al apagarlo.
- `main()` lee `REDDRAGON_HOST` / `REDDRAGON_PORT` (env vars, default `0.0.0.0:8000`) y levanta la app con `uvicorn.run`.

### `controllers/` — Controller

- **`pipeline_controller.py`**: expone `POST /execute_pipeline`.
  - Recibe `file` (UploadFile), `pipeline` (JSON como string), `mode` (`"pruned_xml"` | `"text_list"`) y opcionalmente `query`/`top_k` (reranking con `CrossEncoderService`) y `schema` (JSON como string, extracción estructurada con `NuExtractService`) vía `multipart/form-data`.
  - Valida extensión (`ALLOWED_EXTENSIONS`, importado de `xml_orchestrator`) y `mode` (`ALLOWED_MODES`, importado de `ocr_orchestrator`).
  - Usa `PreserviceFileManager` para materializar el archivo subido en disco, delega la orquestación a `OcrOrchestrator.run(...)` y arma la respuesta con `views.pipeline_view`.

### `preservices/` — preparación de insumos

- **`preservice_filemanager.py`**: `PreserviceFileManager.temp_input_file(contents, extension)` — context manager que escribe los bytes subidos en un `TemporaryDirectory` y limpia el archivo temporal al salir del `with`. Aísla el manejo de filesystem temporal fuera del controller.

### `orchestrators/` — coordinación de flujos de negocio

- **`xml_orchestrator.py`**: `XmlOrchestrator.get_xml(input_path) -> str`.
  Convierte `doc/docx/xls/xlsx/pdf` a XML: si la extensión es `.pdf`, primero pasa por `PdfService.convert_to_docx`; luego siempre pasa por `XmlJavaService.convert` (binario `resources/xmljava-docker`).

- **`ocr_orchestrator.py`**: `OcrOrchestrator.run(input_path, pipeline, mode, query=None, top_k=None, schema=None) -> str | list[str] | dict`.
  Flujo completo:
  1. `XmlOrchestrator.get_xml(input_path)` → `xml_path`.
  2. `XmlService.extract_tables(xml_path)` → datos extraídos del XML (lista plana).
  3. `PipelineService.replace_data(pipeline, extracted_data)` → reemplaza cada llave `"data"` del pipeline (en cualquier nivel de anidamiento) con `{"dato": extracted_data}` (columna `"dato"` con la lista extraída).
  4. `TsubasaService.execute(pipeline)` → envía el pipeline transformado al servidor Tsubasa y recibe una lista plana de valores.
  5. (Opcional) si se pasa `query`, `CrossEncoderService.rerank(query, result_data, top_k)` reordena/recorta `result_data` por relevancia semántica.
  6. Si se pasa `schema`, se **desvía del resto del flujo** e ignora `mode`: `XmlService.prune_xml(xml_path, result_data)` → XML podado, `MarkdownService.to_markdown(pruned_path)` lo renderiza en Markdown, `RedactorService.redact(markdown)` lo convierte en prosa y `NuExtractService.extract(prose, schema)` rellena el esquema JSON contra ella — **su resultado se devuelve de inmediato**.
  7. Si no hay `schema`, según `mode`:
     - `"pruned_xml"` → `XmlService.prune_xml(xml_path, result_data)`, devuelve la ruta del XML podado.
     - `"text_list"` → `XmlService.extract_text(xml_path, result_data)`, devuelve la lista de strings filtrada.

### `services/` — lógica atómica

| Servicio | Responsabilidad |
|---|---|
| `pdf_service.py` | `PdfService.convert_to_docx(pdf_path)` — convierte PDF a DOCX vía `pdf2docx`. |
| `xmljava_service.py` | `XmlJavaService.convert(input_path)` — ejecuta el binario `xmljava` (subprocess) para convertir un archivo a XML; la ruta y el nombre exacto del binario los resuelve `BinaryAdapterFactory` (ver [`services/adapters/`](#servicesadapters--adapter-de-binarios-por-plataforma)). |
| `xml_service.py` | Operaciones sobre árboles XML con BeautifulSoup: `extract_tables` (aplana `Paragraph`/`Table→Row→Col`), `prune_xml` (elimina nodos hoja cuyo texto no está en `valid_data`, limpia nodos vacíos, escribe un XML podado), `extract_text` (recorre `Paragraph`/`Table` y devuelve un string por bloque, filtrado por `valid_data`). |
| `markdown_service.py` | `MarkdownService.to_markdown(xml_path)` — renderiza como Markdown un XML **ya podado** (la salida de `XmlService.prune_xml`): `Paragraph` → línea de texto, `Table` → tabla `\| Columna N \|`. No filtra ni valida nada; asume que el XML recibido ya contiene solo lo relevante. Como `prune_xml` poda por celda y no por fila, las filas de una misma tabla pueden llegar con distinto número de `Col`: se normalizan al ancho de la fila más larga **rellenando por la derecha** con celdas vacías (ver [criterio de alineación](#alineación-de-columnas-tras-el-podado)). |
| `pipeline_service.py` | `PipelineService.replace_data(pipeline, extracted_data)` — recorre recursivamente un JSON (dicts/listas anidadas) y reemplaza cada llave `"data"` por `{"dato": extracted_data}` — Tsubasa espera que `data` en un nodo `scan` sea un dict columnar (`{columna: [valores]}`), no una lista plana. |
| `tsubasa_service.py` | `TsubasaService` — **singleton** que gestiona el ciclo de vida del binario `tsubasa` (`start`/`stop`, subprocess, resuelto vía `BinaryAdapterFactory`) y llama a su endpoint HTTP `/execute` (vía `requests`), aplanando la respuesta (`outputs`/`series`/`dataframe`) a una lista de valores puros. |
| `cross_encoder_service.py` | `CrossEncoderService` — **singleton** (una instancia por proceso) que carga el modelo `jina-reranker-v2-base-multilingual` (`models_ai/`, no versionado) **bajo demanda**: `rerank(query, candidates, top_k=None)` lo carga, reordena `candidates` por relevancia semántica contra `query`, opcionalmente los recorta a `top_k`, y libera el modelo de memoria antes de devolver el resultado. |
| `redactor_service.py` | `RedactorService` — **singleton** (una instancia por proceso) que carga el modelo `qwen2.5-0.5b-instruct-q8_0.gguf` (GGUF cuantizado, `models_ai/`, no versionado) **bajo demanda** vía `llama_cpp.Llama` (no `transformers`, ver nota abajo): `redact(markdown)` lo carga, reescribe el Markdown como prosa (una oración por fila) para que `NuExtractService` tenga menos ambigüedad al alinear columna y valor, y libera el modelo de memoria al terminar. |
| `nuextract_service.py` | `NuExtractService` — **singleton** (una instancia por proceso) que carga el modelo `NuExtract-1.5-tiny.Q8_0.gguf` (GGUF cuantizado, `models_ai/`, no versionado) **bajo demanda** vía `llama_cpp.Llama`: `extract(text, schema)` lo carga, arma el prompt `<|input|>/### Template/### Text/<|output|>`, genera con el modelo, libera el modelo de memoria y devuelve el `dict` resultante de parsear el JSON generado. |
| `text_normalizer_service.py` | `TextNormalizerService.strip_accents(text)` — quita diacríticos (tildes, `ñ`) vía normalización Unicode NFKD. `RedactorService` y `NuExtractService` lo usan en la entrada y la salida del modelo porque el vocabulario de sus `.gguf` corrompe esos caracteres al tokenizar (ver nota abajo). |

#### Por qué `llama_cpp` en vez de `transformers` para los modelos GGUF

`qwen2.5-0.5b-instruct-q8_0.gguf` y `NuExtract-1.5-tiny.Q8_0.gguf` tienen el vocabulario dañado: cualquier carácter UTF-8 multibyte (tildes, `ñ`) se corrompe al tokenizar, tanto cargándolos con `transformers.AutoModelForCausalLM(gguf_file=...)` como con `llama_cpp.Llama` (el loader nativo de GGUF) — se reprodujo igual en ambos, así que el defecto está en el archivo `.gguf` en sí, no en la librería de carga. Se optó por `llama_cpp` de todos modos porque evita la reconstrucción indirecta del tokenizer que hace `transformers` (más simple y rápido para cargar/descargar el modelo por request), y `TextNormalizerService.strip_accents` sanea la entrada y la salida del modelo para que la corrupción de caracteres no llegue al resultado final — al costo de perder el diacrítico original (`Núñez` → `Nunez`).

#### Alineación de columnas tras el podado

`prune_xml` poda **celda por celda**, no fila por fila: si el valor de una `Col` no está en `valid_data`, ese nodo se elimina y la fila queda más corta, sin dejar ningún rastro de en qué posición estaba el hueco. Una tabla de 3 columnas puede llegar a `MarkdownService` así:

```
Row 1 → FECHA | CONCEPTO | MONTO      (3 Col)
Row 2 → 2024-01-05 | 1500            (2 Col — se podó "Compra ruidosa", que estaba en medio)
Row 3 → 2024-02-10 | Venta | 800     (3 Col)
```

Markdown exige que todas las filas tengan el mismo ancho, así que hay que rellenar. **El criterio es rellenar por la derecha**, hasta el ancho de la fila más larga de esa tabla:

```
| Columna 1  | Columna 2 | Columna 3 |
| ---        | ---       | ---       |
| FECHA      | CONCEPTO  | MONTO     |
| 2024-01-05 | 1500      |           |
| 2024-02-10 | Venta     | 800       |
```

Por qué:

- **La posición original de cada celda no es recuperable.** Tras el podado, `[A, C]` y `[A, B]` son indistinguibles. Deducir dónde estaba el hueco sería inventarlo, y el consumidor de este Markdown es `RedactorService` → `NuExtractService`: una alineación inventada produce una extracción *confiadamente incorrecta*, peor que una visiblemente incompleta.
- **Lo único fiable que sobrevive es el orden relativo** de las celdas que quedaron. Rellenar por la derecha lo preserva intacto y concentra toda la incertidumbre al final de la fila, que es donde menos afirma: una celda vacía al final se lee como "aquí ya no hay dato", no como "el dato de esta columna es otro".
- **El ancho se toma del máximo, nunca del mínimo**, para no descartar celdas: recortar filas al ancho más corto sí perdería datos reales.

Consecuencia asumida: en filas podadas por el medio, un valor puede quedar bajo una etiqueta `Columna N` que no le corresponde. Se acepta a propósito — el encabezado es genérico (`Columna 1`, `Columna 2`…), no un nombre real del documento, y el prompt de `RedactorService` está escrito para tolerarlo (usa la primera fila como nombres si parece encabezado, y admite explícitamente filas de cualquier ancho). Si en el futuro hiciera falta alineación exacta, la solución no está en `MarkdownService` sino en que el podado deje un marcador de posición en lugar de eliminar la `Col`.

### `services/adapters/` — adapter de binarios por plataforma

`resources/` incluye dos artefactos por binario: el ELF de Linux (`tsubasa`, `xmljava-docker`) y su equivalente nativo de Windows (`tsubasa.exe`, `xmljava.exe`). Ni `TsubasaService` ni `XmlJavaService` conocen esa diferencia — ambos piden un binario lógico (`"tsubasa"` / `"xmljava"`) a un `BinaryAdapter` y reciben la ruta y el `argv` correctos para el sistema operativo actual (patrón **Adapter**):

- **`binary_adapter/base.py`** — `BinaryAdapter` (ABC): `resolve(name) -> str` (ruta absoluta dentro de `resources/`) e `invocation_args(name, *args) -> list[str]` (argv completo para `subprocess`).
- **`binary_adapter/linux_binary_adapter.py`** — `LinuxBinaryAdapter`: `tsubasa` → `tsubasa`, `xmljava` → `xmljava-docker`. Solo ejecutable dentro de Docker o WSL.
- **`binary_adapter/windows_binary_adapter.py`** — `WindowsBinaryAdapter`: `tsubasa` → `tsubasa.exe`, `xmljava` → `xmljava.exe`. Ejecutable nativamente en Windows, sin Docker ni WSL.
- **`binary_adapter/factory.py`** — `BinaryAdapterFactory.create()` (`staticmethod`, no una función suelta) elige el adapter según `platform.system()`.

`TsubasaService` y `XmlJavaService` llaman `BinaryAdapterFactory.create()` una sola vez en su `__init__` y reusan el adapter devuelto. Agregar soporte para otro sistema operativo o otro binario es agregar una entrada de nombre de archivo (o una subclase nueva de `BinaryAdapter`) aquí, nunca una rama `if platform.system() == ...` dentro de un service.

### `models/` y `views/`

- **`models/pipeline_models.py`**: `PipelineResponse` (Pydantic) — contrato de la respuesta: `filename`, `mode`, `result`.
- **`views/pipeline_view.py`**: `render_pipeline_response(...)` — construye el `PipelineResponse` a partir de los datos crudos devueltos por el orquestador.

### `resources/` — binarios externos

- `xmljava-docker` (Linux) / `xmljava.exe` (Windows) — convierte un documento a XML (`<binario> <archivo-entrada> [archivo-salida.xml]`).
- `tsubasa` (Linux) / `tsubasa.exe` (Windows) — servidor Flask (`polars_ast`) que ejecuta el grafo del pipeline (`POST /execute`) y devuelve `outputs`/`series`/`dataframe` según el tipo de resultado.

Los binarios Linux (`xmljava-docker`, `tsubasa`) solo son ejecutables dentro del contenedor Docker (o WSL). Sus contrapartes `.exe` corren nativamente en Windows. `services/adapters/binary_adapter/` (ver arriba) resuelve cuál usar según la plataforma detectada en runtime.

## Configuración por variables de entorno

| Variable | Usada por | Default |
|---|---|---|
| `REDDRAGON_HOST` | `main.py` (uvicorn) | `0.0.0.0` |
| `REDDRAGON_PORT` | `main.py` (uvicorn) | `8000` |
| `TSUBASA_HOST` | `TsubasaService` | `127.0.0.1` |
| `TSUBASA_PORT` | `TsubasaService` | `5000` |

Definidas en el [Dockerfile](../Dockerfile), junto con `EXPOSE 8000 5000`.

## Flujo end-to-end de `POST /execute_pipeline`

```
Cliente
  │  multipart/form-data: file, pipeline (json), mode [, query, top_k] [, schema]
  ▼
pipeline_controller.execute_pipeline
  │  valida extensión y mode
  │  file_manager.temp_input_file(contents, extension) → input_path
  ▼
ocr_orchestrator.run(input_path, pipeline, mode, query, top_k, schema)
  │
  ├─ xml_orchestrator.get_xml(input_path)
  │     └─ (si .pdf) pdf_service.convert_to_docx → xmljava_service.convert → xml_path
  │
  ├─ xml_service.extract_tables(xml_path) → extracted_data
  ├─ pipeline_service.replace_data(pipeline, extracted_data) → pipeline transformado
  ├─ tsubasa_service.execute(pipeline) → result_data (lista de valores)
  ├─ (si query) cross_encoder_service.rerank(query, result_data, top_k) → result_data
  │
  ├─ (si schema) xml_service.prune_xml(xml_path, result_data) → xml_path_podado
  │              markdown_service.to_markdown(xml_path_podado) → markdown
  │              redactor_service.redact(markdown) → prosa
  │              nuextract_service.extract(prosa, schema) → dict, devuelve directo
  │
  └─ (si no hay schema) mode == "pruned_xml"?
        sí → xml_service.prune_xml(xml_path, result_data) → xml_path_podado
        no → xml_service.extract_text(xml_path, result_data) → list[str]
  ▼
pipeline_view.render_pipeline_response(filename, mode, result) → PipelineResponse (JSON)
```
