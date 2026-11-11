"""Esquemas JSON y función de validación con jsonschema."""
from jsonschema import ValidationError, validate

from utils.logger import get_logger

log = get_logger(__name__)

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {"type": "object"},
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {"type": "object"},
    },
}

USERS_LIST_SCHEMA = {"type": "array", "minItems": 1, "items": USER_SCHEMA}

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
}


def validate_schema(data, schema: dict) -> None:
    """Valida `data` contra `schema`; lanza AssertionError si no cumple."""
    try:
        validate(instance=data, schema=schema)
        log.info("Validación de esquema JSON correcta")
    except ValidationError as exc:
        log.error("Esquema JSON inválido: %s", exc.message)
        raise AssertionError(f"Esquema JSON inválido: {exc.message}") from exc
