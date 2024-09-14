import uuid

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..utils.role import create_role


def test_get_roles(session: Session, client: TestClient) -> None:
    create_role(session=session)
    create_role(session=session)

    response = client.get("/roles")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2


def test_get_role(session: Session, client: TestClient) -> None:
    role = create_role(session=session)

    response = client.get(f"/roles/{role.id}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == str(role.id)
    assert content["code"] == role.code
    assert content["description"] == role.description


def test_get_role_not_found(session: Session, client: TestClient) -> None:
    response = client.get(f"/roles/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_role(session: Session, client: TestClient) -> None:
    data = {"code": "DEV", "description": "Developer"}

    response = client.post("/roles", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id" in content
    assert content["code"] == data["code"]
    assert content["description"] == data["description"]


def test_create_role_conflict(session: Session, client: TestClient) -> None:
    role = create_role(session=session)
    data = {"code": role.code, "description": "Developer"}

    response = client.post("/roles", json=data)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_role(session: Session, client: TestClient) -> None:
    role = create_role(session=session)
    data = {"description": "Updated description"}

    response = client.patch(f"/roles/{role.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == str(role.id)
    assert content["code"] == role.code
    assert content["description"] == data["description"]


def test_update_role_not_found(session: Session, client: TestClient) -> None:
    data = {"description": "Updated description"}

    response = client.patch(f"/roles/{uuid.uuid4()}", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_role(session: Session, client: TestClient) -> None:
    role = create_role(session=session)

    response = client.delete(f"/roles/{role.id}")

    assert response.status_code == status.HTTP_200_OK


def test_delete_role_not_found(session: Session, client: TestClient) -> None:
    response = client.delete(f"/roles/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
