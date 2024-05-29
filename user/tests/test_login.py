from core.settings import settings
from fastapi import status
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_successfully_login_user(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username1",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki1"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/login/"
    login_data = {
        "username": data["username"],
        "password": data["password"]
    }
    response = await async_client.post(url=url, json=login_data)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert "access_token" in response.keys()
    assert len(response["access_token"]) > 7
    assert response["token_type"] == "bearer"

    assert "user" in response.keys()
    assert response["user"]["username"] == data["username"]
    assert response["user"]["first_name"] == data["first_name"]
    assert response["user"]["last_name"] == data["last_name"]
    assert response["user"]["sub_directory"] == data["sub_directory"]
    assert "password" not in response["user"].keys()


@pytest.mark.asyncio
async def test_failed_login_user_with_wrong_password(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username4",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki4"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/login/"
    data = {
        "username": data["username"],
        "password": "fake_pass1"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_failed_login_user_with_wrong_username(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username45",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleeki5"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/login/"
    data = {
        "username": "fake_username",
        "password": data["password"]
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_failed_login_user_with_wrong_username_and_password(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username36",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki36"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/login/"
    data = {
        "username": "fake_username",
        "password": "fake_pass"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
