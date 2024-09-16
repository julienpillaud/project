import uuid

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..utils.site import create_site
from ..utils.user import create_user


def test_get_users(session: Session, client: TestClient) -> None:
    create_user(session=session)
    create_user(session=session)

    response = client.get("/users")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2


def test_get_user(session: Session, client: TestClient) -> None:
    user = create_user(session=session)

    response = client.get(f"/users/{user.id}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == str(user.id)
    assert content["upn"] == user.upn
    assert content["first_name"] == user.first_name
    assert content["last_name"] == user.last_name


def test_get_user_not_found(session: Session, client: TestClient) -> None:
    response = client.get(f"/users/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_user(session: Session, client: TestClient) -> None:
    data = {"upn": "dev@exemple.com", "first_name": "John", "last_name": "Doe"}

    response = client.post("/users", json=data)

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id" in content
    assert content["upn"] == data["upn"]
    assert content["first_name"] == data["first_name"]
    assert content["last_name"] == data["last_name"]


def test_create_user_conflict(session: Session, client: TestClient) -> None:
    user = create_user(session=session)
    data = {"upn": user.upn, "first_name": "John", "last_name": "Doe"}

    response = client.post("/users", json=data)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_user(session: Session, client: TestClient) -> None:
    user = create_user(session=session)

    response = client.delete(f"/users/{user.id}")

    assert response.status_code == status.HTTP_200_OK


def test_delete_user_not_found(session: Session, client: TestClient) -> None:
    response = client.delete(f"/users/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_site_to_user(session: Session, client: TestClient) -> None:
    user = create_user(session=session)
    site = create_site(session=session)

    response = client.post(f"/users/{user.id}/{site.id}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["sites"]
    assert content["sites"][0]["id"] == str(site.id)


def test_add_site_to_user_user_not_found(session: Session, client: TestClient) -> None:
    site = create_site(session=session)

    response = client.post(f"/users/{uuid.uuid4()}/{site.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_site_to_user_site_not_found(session: Session, client: TestClient) -> None:
    user = create_user(session=session)

    response = client.post(f"/users/{user.id}/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
