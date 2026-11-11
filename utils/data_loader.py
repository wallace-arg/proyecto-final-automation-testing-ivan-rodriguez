"""Carga de datos de prueba desde archivos JSON."""
import json
from pathlib import Path

from utils.logger import get_logger

log = get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str = "test_data.json") -> dict:
    """Lee un archivo JSON de la carpeta data/ y devuelve su contenido."""
    path = DATA_DIR / filename
    log.info("Cargando datos de prueba desde %s", path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_test_data() -> dict:
    return load_json("test_data.json")
