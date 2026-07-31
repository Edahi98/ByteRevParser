import time


class TrainingStatusService:
    """Guarda en memoria el avance del entrenamiento en curso, para que la interfaz lo pueda consultar mientras corre.

    Singleton de una sola instancia por proceso. El entrenamiento real
    corre en un hilo aparte (ver `DetectorCambiosController`) porque
    tarda demasiado para una sola petición HTTP; este servicio es el
    punto de contacto entre ese hilo (que va reportando en qué época va)
    y las peticiones de estado que hace la interfaz mientras espera.
    """

    _instance: "TrainingStatusService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.estado = "inactivo"
        self.epoca_actual = 0
        self.epocas_totales = 0
        self.iniciado_en = None
        self.error = None
        self.archivo_zip = None
        self._initialized = True

    def esta_activo(self) -> bool:
        return self.estado == "entrenando"

    def iniciar(self, epocas_totales: int) -> None:
        self.estado = "entrenando"
        self.epoca_actual = 0
        self.epocas_totales = epocas_totales
        self.iniciado_en = time.time()
        self.error = None
        self.archivo_zip = None

    def actualizar_epoca(self, epoca: int, epocas_totales: int) -> None:
        self.epoca_actual = epoca
        self.epocas_totales = epocas_totales

    def completar(self, archivo_zip: bytes) -> None:
        self.estado = "listo"
        self.archivo_zip = archivo_zip

    def fallar(self, mensaje: str) -> None:
        self.estado = "error"
        self.error = mensaje

    def obtener_zip(self) -> bytes | None:
        return self.archivo_zip

    def obtener_estado(self) -> dict:
        segundos_transcurridos = int(time.time() - self.iniciado_en) if self.iniciado_en else 0
        return {
            "estado": self.estado,
            "epoca_actual": self.epoca_actual,
            "epocas_totales": self.epocas_totales,
            "segundos_transcurridos": segundos_transcurridos,
            "error": self.error,
        }
