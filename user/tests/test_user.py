from unittest import TestCase
from core.settings import settings
from fastapi.testclient import TestClient
from main import app
import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_successfully_get_user_info(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username10",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki10"
    }
    register_response = await async_client.post(url=url, json=data)
    assert register_response.status_code == status.HTTP_200_OK
    register_response = register_response.json()

    access_token = register_response["access_token"]
    header = {"Authorization": access_token}

    url = f"{settings.API_V1_STR}/user/info/"
    user_info_response = await async_client.get(url, headers=header)
    assert user_info_response.status_code == status.HTTP_200_OK

    user_info_response = user_info_response.json()
    assert user_info_response["username"], data["username"]
    assert user_info_response["first_name"], data["first_name"]
    assert user_info_response["last_name"], data["last_name"]
    assert user_info_response["sub_directory"], data["sub_directory"]
    assert "password" not in user_info_response.keys()


@pytest.mark.asyncio
async def test_access_denied_get_user_info_without_token_register_user(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/user/info/"
    user_info_response = await async_client.get(url)
    assert user_info_response.status_code == status.HTTP_403_FORBIDDEN
