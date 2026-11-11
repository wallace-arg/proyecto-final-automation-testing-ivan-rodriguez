"""Pruebas de API REST sobre JSONPlaceholder usando requests + jsonschema."""
import pytest

from utils.schema_validator import POST_SCHEMA, USERS_LIST_SCHEMA, validate_schema

pytestmark = pytest.mark.api


def test_tc_api_1_get_listar_usuarios(api_client, test_data):
    """TC-API-1 (GET): status 200, tiempo de respuesta y estructura JSON."""
    response = api_client.get("/users")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < test_data["api"]["max_response_time_seconds"]
    assert "application/json" in response.headers["Content-Type"]

    users = response.json()
    assert len(users) == 10
    validate_schema(users, USERS_LIST_SCHEMA)


def test_tc_api_2_post_crear_recurso(api_client, test_data):
    """TC-API-2 (POST): status 201 y cuerpo de respuesta coherente."""
    payload = test_data["api"]["new_post"]
    response = api_client.post("/posts", payload)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() < test_data["api"]["max_response_time_seconds"]

    body = response.json()
    validate_schema(body, POST_SCHEMA)
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert body["id"] > 0


def test_tc_api_3_put_modificar_recurso(api_client, test_data):
    """TC-API-3 (PUT): status 200 y recurso actualizado."""
    payload = test_data["api"]["update_post"]
    response = api_client.put(f"/posts/{payload['id']}", payload)

    assert response.status_code == 200
    body = response.json()
    validate_schema(body, POST_SCHEMA)
    assert body["id"] == payload["id"]
    assert body["title"] == payload["title"]


def test_tc_api_4_delete_eliminar_recurso(api_client):
    """TC-API-4 (DELETE): status 200 y cuerpo vacío."""
    response = api_client.delete("/posts/1")

    assert response.status_code in (200, 204)
    assert response.json() == {}
