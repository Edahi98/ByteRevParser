from pydantic import BaseModel


class DetectorCambiosConfig(BaseModel):
    random_seed: int = 42
