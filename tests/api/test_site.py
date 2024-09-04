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

    response = client.get(f"/sites/{site.code}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["code"] == site.code
    assert content["name"] == site.name


def test_create_site(session: Session, client: TestClient) -> None:
    data = {"code": "SITE", "name": "Site"}

    response = client.post("/sites", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["code"] == data["code"]
    assert content["name"] == data["name"]


def test_update_site(session: Session, client: TestClient) -> None:
    site = create_site(session=session)
    data = {"name": "Updated site"}

    response = client.patch(f"/sites/{site.code}", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["code"] == site.code
    assert content["name"] == data["name"]


def test_delete_site(session: Session, client: TestClient) -> None:
    site = create_site(session=session)

    response = client.delete(f"/sites/{site.code}")

    assert response.status_code == status.HTTP_200_OK
