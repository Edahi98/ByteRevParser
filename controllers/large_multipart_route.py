import os
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

MAX_PART_MB = int(os.environ.get("REDDRAGON_MAX_PART_MB", 64))
MAX_PART_SIZE = MAX_PART_MB * 1024 * 1024


class LargeMultipartRoute(APIRoute):
    """Ruta que amplía el tope de 1MB por campo de texto que Starlette aplica al
    parsear `multipart/form-data`.

    Los archivos subidos no se ven afectados por ese tope (se vuelcan a un fichero
    temporal conforme llegan), pero los campos de texto se acumulan en memoria y
    Starlette los corta en 1MB con `Part exceeded maximum size of 1024KB.`. El
    `pipeline` y el `schema` viajan como campos de texto y superan ese tamaño con
    facilidad, así que aquí se pre-parsea el formulario con un tope mayor: el
    `FormData` queda cacheado en el `Request` y FastAPI lo reutiliza después.
    """

    def get_route_handler(self) -> Callable[[Request], Awaitable[Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            content_type = request.headers.get("content-type", "")
            if content_type.startswith("multipart/form-data"):
                await request.form(max_part_size=MAX_PART_SIZE)
            return await original_route_handler(request)

        return custom_route_handler
