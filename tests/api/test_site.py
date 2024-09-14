import uuid

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..utils.site import create_site


def test_get_sites(session: Session, client: TestClient) -> None:
    create_site(session=session)
    create_site(session=session)

    response = client.get("/sites")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2


def test_get_site(session: Session, client: TestClient) -> None:
    site = create_site(session=session)

    response = client.get(f"/sites/{site.id}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == str(site.id)
    assert content["code"] == site.code
    assert content["name"] == site.name


def test_get_site_not_found(session: Session, client: TestClient) -> None:
    response = client.get(f"/sites/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_site(session: Session, client: TestClient) -> None:
    data = {"code": "SITE", "name": "Site"}

    response = client.post("/sites", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id" in content
    assert content["code"] == data["code"]
    assert content["name"] == data["name"]


def test_create_site_conflict(session: Session, client: TestClient) -> None:
    site = create_site(session=session)
    data = {"code": site.code, "name": "Site"}

    response = client.post("/sites", json=data)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_site(session: Session, client: TestClient) -> None:
    site = create_site(session=session)
    data = {"name": "Updated site"}

    response = client.patch(f"/sites/{site.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == str(site.id)
    assert content["code"] == site.code
    assert content["name"] == data["name"]


def test_update_site_not_found(session: Session, client: TestClient) -> None:
    data = {"name": "Updated site"}

    response = client.patch(f"/sites/{uuid.uuid4()}", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_site(session: Session, client: TestClient) -> None:
    site = create_site(session=session)

    response = client.delete(f"/sites/{site.id}")

    assert response.status_code == status.HTTP_200_OK


def test_delete_site_not_found(session: Session, client: TestClient) -> None:
    response = client.delete(f"/sites/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
