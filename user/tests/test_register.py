import pytest
from httpx import AsyncClient
from fastapi import status
from core.settings import settings


@pytest.mark.asyncio
async def test_successfully_register_user(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
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


async def test_failed_register_user_when_username_length_is_less_than_5(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new1",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_sub_directory_length_is_less_than_5(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "mal"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_sub_directory_length_is_more_than_25(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "qwertyhgfdsazxcvbnhgfdsawr"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_password_length_is_less_than_8(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "Test1",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_password_has_no_digits(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "TestCasetest",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_password_has_uppercase(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "testcasetest123",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_password_has_lowercase(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username",
        "password": "GSDFIKJDASRF123",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_register_user_when_sub_directory_exists(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "test_username",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "arash"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/register/"
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
